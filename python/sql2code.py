#! /usr/bin/python -d

import sys
import re



def sql_definition_to_csharp(lines):
    sql2csharp = {
        'varchar' : 'string',
        'money' : 'decimal',
        'decimal' : 'decimal',
        'int' : 'int',
        'float' : 'decimal',
        'bit' : 'bool',
        'datetime' : 'DateTime'
    }
    
    spec_re_with_len = re.compile('\[(.*)\] \[(.*)\](\((.*)\)).*')
    spec_re_no_len = re.compile('\[(.*)\] \[(.*)\].*')

    for line in lines:
        field_name = ''
        field_type = ''
        field_len = -1
        is_not_null = False
        
        if line.find('NOT NULL') != -1:
            is_not_null = True
        mo = re.match(spec_re_with_len, line)
        if mo != None:
            field_name = mo.group(1)
            field_type = mo.group(2)
            if field_type == 'varchar':
                field_len = int(mo.group(4))
        else:
            mo=re.match(spec_re_no_len, line)
            if mo != None:
                field_name = mo.group(1)
                field_type = mo.group(2)
        
        if is_not_null == True:
            print('[Required]')

        if field_type == 'varchar' and field_len != -1:
            print('[MaxLength(%d)]'%field_len)

        print('public %s %s { get; set; }\n'%(sql2csharp[field_type], field_name))


def test_harness():
    #todo: add tests

def main():
    if len(sys.argv) < 2:
        print('usage: sql2code.py file1 file2 ....')
    else:
        for file in sys.argv[1:]:
            f = open(file, 'r')
            sql_definition_to_csharp(f.readlines())

if __name__=='__main__':
    main()

