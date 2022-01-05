
# ability to pick specific options
# - OS detection
# - Aggressive scan -A, -Pn
# - SYN ACK scan ... more




# inputs:
# - ip address
# - mode/scan type
# - port(s)



import nmap
import time


scanner = nmap.PortScanner()
nmap_version = scanner.nmap_version()
local_time = time.localtime()

print()


target_ip = input("Target IP address: ")
target_ports = input('Target port(s)/ range: ')

print('Running scans on ', target_ip, 'on ports ', target_ports)

scanner.scan(target_ip, target_ports, '-v -sU')
print(scanner.scaninfo())

# scan_mode = input("Scan Mode: ")


