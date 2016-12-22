#! /usr/bin/env python

import sys
import signal
import load_pcap

def get_sap_endpoints(file):
  result = []
  for ep in load_pcap.get_end_points(load_pcap.load(file)):
    if ep[1] >= 3200 and ep[1] < 3300:
      result.append(ep)
  return result
    

def main():
  if len(sys.argv) > 1:
    for file in sys.argv[1:]:
      for endp in get_sap_endpoints(file):
        print endp



if __name__=='__main__':
  main()
