#!/usr/bin/env python3

import nmap
import re


'''

inputs: ip address, port/port range, type of scan  - ability to just input known flags & gives example commands/ link to nmap scan manpage

initial goals:
    allows single port, multiple ports, and range of port inputs ✔
    verifies that the ip address is valid ipv4 address input ✔
    verify that the ports are valid inputs ✔
    prints hostname, ip address and state of host ✔

    next step:
    give the user options of types of scans instead of putting in args via cmd
    ability to do a wide range of scans & process multiple arugments/flags - halfway


down the road:
    make it a bash script
    has banner grabbing & more indepth information
    looks cute with colors and unique interface
    has cute pixel art in the beginning
    learn how to make animated terminal art for beginning
'''



def valid_ip(targ_ip_address):
    valid_ip_re =  re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")

    # ensures that the ip input matches the correct pattern format
    if valid_ip_re.search(targ_ip_address):
        # print(f'{targ_ip_address} : valid address found!')
        return True
    else:
        print(f'{targ_ip_address}: errr address not found')
        return False


def valid_port(targ_port):
    valid_port_re = re.compile("([0-9]+)-([0-9]+)")

    # ensures that the ip input matches the correct pattern format
    if valid_port_re.search(targ_port):
        # print(f'{targ_port} : valid port(s) found!')
        return True
    else:
        print(f'{targ_port}: errr port(s) not found')
        return False


def scanner(ip_address, port_values, scan_args):
    nm = nmap.PortScanner()
    x = nm.scan(hosts=ip_address, ports=port_values, arguments=str(scan_args))

    # print(x)
    port_begin, port_end = port_values.split('-')


    # prints the status of the host - up/down
    status_addr = nm[ip_address]['status']['state']
    print(f'{nm[ip_address].hostname()} @ {ip_address} ----> {status_addr}')
    print()


    open_ports = 0
    total_ports = 0
    # loops through all the given range of ports
    for port in range(int(port_begin), int(port_end )-1):
        total_ports += 1

        # allows for a UDP or TCP protocols to find state of port
        for protocol in nm[ip_address].all_protocols():
            # print(protocol)

            indv_port_state = nm[ip_address]['tcp'][int(port)]['state']
            indv_port_name = nm[ip_address]['tcp'][int(port)]['name']
            # print(f'port #{total_ports}')
            # print(indv_port_state)



            if indv_port_state == 'open':
                open_ports +=1
                print(f'Port {port} : open')
                print(f'    --> service : {indv_port_name}')
            else:
                continue
                # print(indv_port_name, ' is down')
        

    # # OS detection
    # if 'osclass' in nm[ip_address]:
    #     print('OS detected')
    #     for operating in nm[ip_address]['osclass']:
    #         print(f'osclass.type : {operating.type}')
    #         print(f'osclass.vendor : {operating.vendor}')


    # working OS detection - develop this next - have as default for all scans at bottom
    print(x['scan'][ip_address]['osmatch'])

    closed_ports = total_ports - open_ports 
    print()
    print(f'Ports closed: {closed_ports}/{total_ports}')







def main():
    # ipaddr = '127.0.0.1'
    # port = '21'

    ipaddr = input('Enter ip address: ')
    port = input('Enter port(s)/port range: ')
    if valid_ip(ipaddr) & valid_port(port) == True:
        print('ip address & ports: valid')
        # scanner(ipaddr, port)

    else: 
        print('Either ip address, ports, or both are incorrect')
        return
    args = input('Enter arguments: ')

    print()
    print(f':::::::::::::::::scan initiated on {ipaddr}::::::::::::::::')
    print()
    scanner(ipaddr, port, args)
    

 

main()