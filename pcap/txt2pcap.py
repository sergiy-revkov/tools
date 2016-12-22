#! /usr/bin/env python

import sys
import re
import struct
import argparse


def txt2pcap(sys_argv):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-o','--output')
    argparser.add_argument('-i','--input')
    args = argparser.parse_args(sys.argv[1:])


    ifile = sys.stdin
    if args.input != None:
        ifile = open(args.input)

    ofname = 'out.pcap'
    if args.output != None:
        ofname = args.output
    ofile = open(ofname, 'wb')

    head_re = re.compile('HEAD MagicNum\(0x([0-9a-f]+)\) VersionMaj\(([0-9]+)\) VersionMin\(([0-9]+)\) TimeZone\(([0-9]+)\) SigFigs\(([0-9]+)\) SnapLen\(0x([0-9a-f]+)\) Network\(([0-9]+)\)')
    pkt_re = re.compile('PKT timestamp\(([0-9\.]+)\)\s+payload\(([0-9A-F]+)\)')

    is_header_found = False


    for line in ifile.readlines() :
        if is_header_found == False:
            mo = re.match(head_re, line)
            if mo == None :
                print('Error: HEAD spec is not found yes. ignored: '+line)
            else:
                is_header_found = True
                header_bin = struct.pack('<IHHIIII', 
                                         0xa1b2c3d4, 
                                         # int(mo.group(1), 16), - we are not saving tcpdump extended format
                                         int(mo.group(2), 10),
                                         int(mo.group(3), 10),
                                         int(mo.group(4), 10),
                                         int(mo.group(5), 10),
                                         int(mo.group(6), 16),
                                         int(mo.group(7), 10))
                ofile.write(header_bin)


        else :
            mo = re.match(pkt_re, line)
            if mo == None:
                print ('Error: PKT spec accepted only. ignored: '+line)
            else:
                timestamp_re = re.compile('([0-9]+)\.([0-9]+)')
                m_ts = re.match(timestamp_re, mo.group(1))
                if m_ts != None:
                    packet_header_bin = struct.pack('<IIII',
                                                    int(m_ts.group(1), 10),
                                                    int(m_ts.group(2), 10),
                                                    len(mo.group(2))/2,
                                                    len(mo.group(2))/2)
                    packet_payload = ''
                    for i in range(0, len(mo.group(2)), 2) :
                        packet_payload += ( chr( int( mo.group(2)[i:i+2], 16) ) )

                    ofile.write(packet_header_bin)
                    ofile.write(packet_payload)


def main():
  if len(sys.argv) > 1:
    txt2pcap(sys.argv)

if __name__=='__main__':
  main()
