#! /usr/bin/python -tt

import sys

def dump_file_as_c_array(filename):
    f = open(filename, 'rb')
    alldata = f.read()
    width = 8
    result = '{\n'
    offset = 0
    for b in alldata:
        result += ("0x%02X" % ord(b)) + ', '
        offset += 1
        if offset == width:
            result += '\n'
            offset = 0
    result += '\n}'
    
    return result

def main():
  if len(sys.argv) < 2:
      print('Usage: bin2c.py /path/to/bin/file')
  else:
      for file in sys.argv[1:]:
          dump = dump_file_as_c_array(file)
          print
          print(dump)


if __name__ == '__main__':
    main()

