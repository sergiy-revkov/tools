#! /usr/bin/env python

import sys
import re
import hashlib

print("test\n")

re_exp = re.compile(sys.argv[1]+'\(([0-9A-Fa-f]+)\)')

s = ''
for line in sys.stdin.readlines() :
    i = 0
    print line.strip()
    mo = re.search(re_exp, line)
    if mo != None :
        s = 'SHA256 field: '+sys.argv[1]+'\n'
        hexdata_str = mo.group(1)
        data_str = ''
        for i in range(0, len(hexdata_str), 2) :
            data_str += ( chr( int( hexdata_str[i:i+2], 16) ) )
        s += 'input buffer lenght: '+('%d' % len(data_str)) + '\n'
        h = hashlib.sha256()
        h.update(data_str)
        s += 'SHA256('+h.hexdigest()+')\n'
    print s
    s = ''
