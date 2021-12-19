import nmap

# initilize the scanner
a_scan = nmap.PortScanner()

a_scan.scan('127.0.0.1', '21-443')

for host in a_scan.all_hosts():
    # access host IP address & (hostname of host)
    print('Hostname: %s (%s)' % (host, a_scan[host].hostname()))
    # access host state (up/down)
    print('State: %s' %(a_scan[host].state()))
    print('=======================')

    for protocol in a_scan[host].all_protocols():
        print('Protocol: %s' % protocol)
        
        a_port = a_scan[host][protocol].keys()
        # a_port.sort()

        for ports in a_port:
            print('Port: %d    State: %s    ' % (ports, a_scan[host][protocol][ports]['name']))

            # other optoins of things to scan in 'state'
                # conf, name, method, reason, cpe, version, product

                # ie: print('Port: %d    Method: %s    ' % (ports, a_scan[host][protocol][ports]['method']))
            



