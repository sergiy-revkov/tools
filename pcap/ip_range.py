#!/usr/bin/python -tt


import sys


def str_2_ip_list(ip):
    retv = None
    sp = ip.split('.')

    if len(sp) == 4: #ipv4 only :(
        retv = []
        for i in sp:
            try:
                retv.append(int(i))
            except ValueError:
                return None

    return retv


def str_2_ip_list_ut():
    if str_2_ip_list('1.1.1.1') == [1, 1, 1, 1]: print 'x'
    else: print 'F'
    if str_2_ip_list('abcd') == None: print 'x'
    else: print 'F'
    if str_2_ip_list('1.1.1.1.1') == None: print 'x'
    else: print 'F'
    if str_2_ip_list('') == None: print 'x'
    else: print 'F'
    if str_2_ip_list('1.1.1') == None: print 'x'
    else: print 'F'
    #todo: add tests for ipv6


def is_in_range(ip1, port1, ip2, port2, ip, port):
    """ return true if ip:port belongs to range [ip1:port1, ip2:port2] """
    ret = False

    ip_1 = str_2_ip_list(ip1)
    ip_2 = str_2_ip_list(ip2)
    ip_x = str_2_ip_list(ip)

    try:
        port_1 = int(port1)
        port_2 = int(port2)
        port_x = int(port)
    except ValueError:
        return False


    if ip_1 and ip_2 and ip_x:
        if ip_x >= ip_1 and ip_x <= ip_2:
            if port_x >= port_1 and port_x <= port_2:
                ret = True
    return ret

def ip_range_ut():
    if not is_in_range('abcd', 'abcd', 'abcd', 'abcd', 'abcd', 'abcd'): print 'x'
    else: print 'F'
    if is_in_range('1.1.1.1', '1', '255.255.255.255', '65535', '11.11.11.11', '11'): print 'x'
    else: print 'F'
    if is_in_range('1.1.1.1', '1', '1.1.1.1', '100', '1.1.1.1', '50'): print 'x'
    else: print 'F'
    if is_in_range('1.1.1.1', '1', '1.1.1.100', '1', '1.1.1.50', '1'): print 'x'
    else: print 'F'
    if not is_in_range('1.1.1.1', '1', '1.1.1.100', '1', '1.1.1.101', '1'): print 'x'
    else: print 'F'
    if not is_in_range('1.1.1.1', 'b', '1.1.1.100', '1', '1.1.1.101', '1'): print 'x'
    else: print 'F'
    if is_in_range('1.2.3.4', '100', '4.3.2.1', '100', '3.3.3.3', '100'): print 'x'
    else: print 'F'

    #todo: add tests for ipv6


def main():
    str_2_ip_list_ut()
    ip_range_ut()

if __name__ == '__main__':
    main()
