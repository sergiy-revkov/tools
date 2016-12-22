#!/usr/bin/python -tt

import sys
import re

def prepare_line(line, header):
    result = {}
    for field in header.keys():
        result[field] = line[header[field]]
    return result


def is_summary(line):
    return (line['c-ip:ip'] == '-')


def process_line(line):
    """process one line from vdata or zdata files.
    
    Args:
        line - property map. column name -> value

    Returns:
        nothing.
    """

    print line
    print
    print
    return

    if line['type'] == 'SA' and not is_summary(line):
        try:
            reqEndDT = int(line['reqEndDT:uint'])
            resBegDT = int(line['resBegDT:uint'])
            time_taken = int(line['time-taken:uint'])
            sPkt = int(line['sPkt:uint'])
        except ValueError:
            return

        if sPkt > 3 and (resBegDT - reqEndDT == 0 or time_taken/(resBegDT-reqEndDT) < 0.1):
            print line['c-ip:ip'] \
                + ':' + line['c-port:uint'] \
                + ' ' +line['begT:ulong'] \
                + ' ' + line['time-taken:uint'] \
                + ' ' + line['reqEndDT:uint'] \
                + ' ' + line['resBegDT:uint'] \
                + ' ' + line['sPkt:uint'] 


def prepare_fields_dict(fields):
    typeid = None
    fields_dict = {}
    if fields[1] == 'type':
        typeid = 'default'
    else:
        typeid = fields[1][len('type='):]

    index = 1
    fields_dict['type'] = 0
    for field in fields[2:]:
        fields_dict[field] = index
        index += 1
    return typeid, fields_dict

def process_file(filename):
    print '[MSG] processing file: '+filename
    f = open(filename, 'r')
    headers = {}
    for line in f:
        line_fields = line.split()
        if line_fields[0] == '#Fields:':
            typeid, fields = prepare_fields_dict(line_fields)
            headers[typeid] = fields
        elif line_fields[0][0] != '#': #process normal line
            header = headers.get(line_fields[0])
            if header == None:
                header = headers['default']

            if len(line_fields) == len(header):
                process_line(prepare_line(line_fields, header))
            else:
                print '[ERROR] header does not match data:' + line

def main():
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            process_file(file)

if __name__ == '__main__':
    main()
