#! /usr/bin/env python

import sys
import re
import struct


def eth_ip_tcp(lines):
    pkt_re = re.compile('PKT timestamp\(([0-9\.]+)\)\s+payload\(([0-9A-F]+)\)')
    for line in lines :
        mo = re.match(pkt_re, line)
        if mo != None :
            out = ''
            data_str = mo.group(2)
            out = 'PKT timestamp('+mo.group(1)+') payload('+mo.group(2)+') '
            payload = ''

            for i in range(0, len(data_str), 2) :
                payload += ( chr( int( data_str[i:i+2], 16) ) )

            ethh = struct.unpack('>BBBBBBBBBBBBH', payload[0:14])

            if ethh[12] == 0x86dd: #it is ipv6 packet
                offset = 14
                # ipv6 header parsing 
                ipv6h = struct.unpack('>IHBBHHHHHHHHHHHHHHHH', payload[offset:offset+40])
                out += 'sip(%04x:%04x:%04x:%04x:%04x) ' % (ipv6h[4], ipv6h[8], ipv6h[9], ipv6h[10], ipv6h[11])
                out += 'dip(%04x:%04x:%04x:%04x:%04x) ' % (ipv6h[12], ipv6h[16], ipv6h[17], ipv6h[18], ipv6h[19])

                offset += 40
                # tcp header parsing
                tcph = struct.unpack('>HHIIH', payload[offset:offset+14])
                out += 'sp(%d) dp(%d) seq(%d) ack(%d) ' % (tcph[0], tcph[1], tcph[2], tcph[3])
                flags = tcph[4]
                hlen = (flags >> 12) * 4
                # out += 'hlen(%d) f(' % hlen
                out += 'f('
                if (flags & 0x1) > 0 :
                    out += 'F'
                if (flags & 0x2) > 0 :
                    out += 'S'
                if (flags & 0x4) > 0 :
                    out += 'R'
                if (flags & 0x8) > 0 :
                    out += 'P'
                if (flags & 0x10) > 0 :
                    out += 'A'
                out += ') data('

                offset += hlen

                #output payload
                for b in payload[offset:len(payload)] :
                    out += '%02X' % ord(b)

                out += ')'


            else:
                out += 'Not a ipv6 packet'

            print out

    #print line

def main():
  eth_ip_tcp(sys.stdin.readlines())


if __name__=='__main__':
  main()
