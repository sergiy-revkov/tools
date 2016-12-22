#! /usr/bin/env python

import struct
import os.path
import sys
import signal



def render_pcap_file(filename):
    with open(filename, "rb") as f:
        # add here check for proper size
        offset = 0
        data = f.read()
        gl_h = struct.unpack('<IHHIIII', data[offset:offset+24]); offset+=24
        m_n, v_mag, v_min, thiszone, sigfigs, snaplen, network = gl_h

        if (m_n != 0xa1b2c3d4) and \
                (m_n != 0xa1b2cd34) :
            print filename+" is not a pcap capture file. Proper magic number is not found. "
            return

        s = "HEAD MagicNum(0x"+('%8x' % m_n)+ \
            ") VersionMaj("+str(v_mag)+ \
            ") VersionMin("+str(v_min)+ \
            ") TimeZone(" +str(thiszone)+ \
            ") SigFigs(" +str(sigfigs)+ \
            ") SnapLen(" +str(hex(snaplen))+ \
            ") Network(" +str(network)+")"
        print s

        while offset < len(data):
            p_h = struct.unpack('<IIII', data[offset:offset+16]); offset+=16
            sec, usec, slen, rlen = p_h

            s = "PKT timestamp("+str(sec)+ \
                "."+("%06d" % (usec)) + \
                ") payload("

            if m_n == 0xa1b2cd34 :
                offset += 8

            for b in data[offset:offset+slen] :
                s = s + ('%02X' % ord(b))

            s = s + ")"

            print s

            offset+=slen


def get_flags(flags):
  out = ''
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
  return out

def get_tcp_header_len(flags):
    return (flags >> 12) * 4

def load(filename):
  ret = []
  with open(filename, 'rb') as f:
    offset = 0
    data = f.read()
    f_h = struct.unpack('<IHHIIII', data[offset:offset+24])
    offset+=24
    magic, v_maj, v_min, thiszone, sigfigs, snaplen, network = f_h
    if magic == 0xa1b2c3d4 or magic == 0xa1b2cd34:
      while offset < len(data):
        p_h = struct.unpack('<IIII', data[offset:offset+16])
        offset += 16
        pkt = []
        sec, usec, slen, rlen = p_h
        pkt.append(sec)
        pkt.append(usec)
        if magic == 0xa1b2cd34:
          offset += 8
        ethh = struct.unpack('>BBBBBBBBBBBBH', data[offset:offset+14])
        pkt_off = offset+14
        ip_parsed = False
        if ethh[12] == 0x86dd: #IPv6
          pkt.append('ipv6')
          ipv6h = struct.unpack('>IHBBHHHHHHHHHHHHHHHH', data[pkt_off:pkt_off+40])
          pkt.append('%04x:%04x:%04x:%04x:%04x' % (ipv6h[4], ipv6h[8], ipv6h[9], \
                                                        ipv6h[10], ipv6h[11]))
          pkt.append('%04x:%04x:%04x:%04x:%04x' % (ipv6h[12], ipv6h[16], ipv6h[17], \
                                                        ipv6h[18], ipv6h[19]))
          if ipv6h[2] == 0x06:
            pkt.append('tcp')
          pkt_off += 40
          ip_parsed = True
        elif ethh[12] == 0x0800: #IPv4
          pkt.append('ipv4')
          ipv4h = struct.unpack('>IIBBHBBBBBBBB', data[pkt_off:pkt_off+20])
          pkt.append('%d.%d.%d.%d' % (ipv4h[5], ipv4h[6], ipv4h[7], ipv4h[8]))
          pkt.append('%d.%d.%d.%d' % (ipv4h[9], ipv4h[10], ipv4h[11], ipv4h[12]))
          if ipv4h[3] == 0x06:
            pkt.append('tcp')
          pkt_off += 20
          ip_parsed = True
        else:
          pkt.append('unsupported %x' % ethh[12])

        tcph = struct.unpack('>HHIIH', data[pkt_off:pkt_off+14])
        pkt.extend([tcph[0], tcph[1], tcph[2], tcph[3], get_flags(tcph[4])])
        pkt.append(data[pkt_off+get_tcp_header_len(tcph[4]):offset+slen]) #payload

        ret.append(pkt)
        offset += slen
    else:
      print 'Error: can not find proper magic number.'

  return ret


def get_end_points(pkt_lst):
  end_points = {}
  for pkt in pkt_lst:
    print pkt[:-1]
    if len(pkt)>11:
      if (pkt[2] == 'ipv4' or pkt[2] == 'ipv6') and pkt[5] == 'tcp':
        print pkt[:-1]
        end_points[pkt[3]+':'+str(pkt[6])] = [pkt[3], pkt[6]]
        end_points[pkt[4]+':'+str(pkt[7])] = [pkt[4], pkt[7]]

  return end_points.values()

def main():
  if len(sys.argv) > 1:
    for file in sys.argv[1:]:
      render_pcap_file(file)
      all = load(file)
      #for ep in get_end_points(all):
      #    print ep


if __name__=='__main__':
  main()
