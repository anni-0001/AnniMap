import nmap
import time

# not finding open hosts- not working
def ping(ip_address, port_values, scan_args):
    nm = nmap.PortScanner()

    x = nm.scan(hosts=ip_address, ports=port_values, arguments=str(scan_args), timeout=15)
    host_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    print(host_list)
    print(nm.scanstats())
    # print(nm[ip])


def main():
    ip_address = input("Enter ip address: ")
    port_values = input("Enter port range: ")
    scan_args = '-n -sP -PA21, 23, 90, 3389'

    ping(ip_address, port_values, scan_args)

main()