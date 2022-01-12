#!/usr/bin/env python3

import nmap
import re
import time


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
    make it a bash script/more efficient
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


def scanner(ip_address, port_values,scan_args):
    timer_start = time.perf_counter()

    nm = nmap.PortScanner()
    x = nm.scan(hosts=ip_address, ports=port_values, arguments=str(scan_args), timeout=15)
    port_begin, port_end = port_values.split('-')

    # prints the status of the host - up/down
    status_addr = nm[ip_address]['status']['state']
    hostname = nm[ip_address].hostname()
    # lastboot = x['scan'][ip_address]['uptime']['lastboot']
    print('\n----------------Host info----------------\n')

    # print('\n|------------------------------------------|')
    print(f'  host @ {ip_address} ----> {status_addr}        ')
    # print(f'Last system boot : {lastboot}')
    # print('|-----------------------------------------|')

    print()

    # print(f'Last system boot : {lastboot}')

    open_ports = 0
    total_ports = 0

    print('\n----------------Port scan----------------\n')

    # loops through all the found tcp ports
    for a_port in nm[ip_address].all_tcp():
        total_ports +=1

        

        state = nm[ip_address]['tcp'][a_port]['state']
        service = nm[ip_address]['tcp'][a_port]['product']
        reason = nm[ip_address]['tcp'][a_port]['reason']

        # this is redundant hunny - if theyre in the list then its open ... right?
        if state == 'open':
            open_ports +=1
            print(f'Port {a_port} : {state}')
            print(f'    --> service : {service}')
            print(f'    --> reason : {reason}')
            print('    --> protocol : tcp')

            try:
                # if the -sV option is present
                if x['scan'][ip_address]['tcp'][a_port]['version']:
                    version = x['scan'][ip_address]['tcp'][a_port]['version']
                    print(f'    --> version :  {version}')

            except KeyError:
                print(f'ERR... use -sV for version detection')
                
            print()
        else:
            print(f'port {total_ports} : {state}')
            continue

    '''
    identical functions above & below - quickest sol to look at tcp & udp 
        - implement recursions? not v code efficient - BUT runs plenty fast
        actually - make a combined list for tcp& udp then parse the data in the same function
    '''

    # loops through all found udp ports
    for a_port in nm[ip_address].all_udp():
        total_ports +=1

        state = nm[ip_address]['udp'][a_port]['state']
        name = nm[ip_address]['udp'][a_port]['name']
        reason = nm[ip_address]['udp'][a_port]['reason']
        # print(f'port #{total_ports}: {state}')
        if state == 'open':
            open_ports +=1
            print(f'Port {a_port} : open')
            print(f'    --> service : {name}')
            print(f'    --> reason : {reason}')
            print('     --> protocol : udp')
            print()

    # print(x['scan'][ip_address])
    # print(x['scan'])

    
    
    # if the user put in -O option
    try: 
        if x['scan'][ip_address]['osmatch']:
            # print(x['scan'][ip_address]['osmatch'])

            operating_sys = x['scan'][ip_address]['osmatch'][0]['name']
            accuracy = x['scan'][ip_address]['osmatch'][0]['accuracy']
            lastboot = x['scan'][ip_address]['uptime']['lastboot']
            devtype =x['scan'][ip_address]['osmatch'][0]['osclass'][0]['type']

            # devtype = x['scan'][ip_address]['osmatch']['osclass']['type']
            # devtype = x

   
            print('\n+++ OS: DETECTED')
            print(f'Last system boot: {lastboot}')

            '''with the scan values set to static comprehensive all these should work
            no problem, but will need seperate programs for when more custom
            input options are available'''

            print(f'    --> OS & version: {operating_sys}')
            # print(f'    --> Last system boot: {lastboot}')
            print(f'    --> Type : {devtype}')
            print(f'    --> Accuracy : {accuracy} %\n')
            # print('')
    except KeyError:
        print('-- OS: NOT DETECTED')




    timer_stop = time.perf_counter()


    total_ports = (int(port_end)+1) - int(port_begin)

    print('\n------Scan Summary------')
    print(f'OPEN PORTS: {open_ports}/{total_ports} ports')


    print(f'{total_ports} ports scanned in {round(timer_stop- timer_start, 3)} seconds')



def main():
    # ipaddr = '127.0.0.1'
    # port = '21'

    ipaddr = input('Enter ip address: ')
    port_range = input('Enter port(s)/port range: ')

    if valid_ip(ipaddr) & valid_port(port_range) == True:
        print('ip address & ports: valid')
        # scanner(ipaddr, port)

    else: 
        print('Either ip address, ports, or both are incorrect')
        return
    args = '-sV -sX -O -'#input('Enter arguments: ')
    # args to work on adding: -sP
    # args = '-sP'

    print()
    print(f':::::::::::::::::scan initiated on {ipaddr}::::::::::::::::')
    print()
    
    scanner(ipaddr, port_range, args)
    

 

main()