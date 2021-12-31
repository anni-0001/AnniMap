#!usr/bin/env python

# a little simple network scanner ... in progress

import nmap
import argparse
import colors


def base_scan(target_h, target_p):
    # initialize scan
    nmscan_ = nmap.PortScanner()
    nmscan_.scan(target_h, target_p)

    reason = nmscan_[target_h]['tcp'][int(target_p)]['reason']
    # method = nmscan_[target_h]['tcp'][int(target_p)]['method']
    state = nmscan_[target_h]['tcp'][int(target_p)]['state']
    name = nmscan_[target_h]['tcp'][int(target_p)]['name']
    

    # itital state that if not changed by function below, indicates an error w/ the state
    print_state = '***state ERROR'


    # adding in color to the command line interface
    if state == 'open':
        print_state = colors.color.YELLOW +'<OPEN>'+ colors.color.END
    elif state == 'closed':
        print_state = colors.color.RED +'<CLOSED>'+ colors.color.END
        


    print('------->' + ' tcp/'+ target_p+ ' '+ print_state )




def main():

    parser = argparse.ArgumentParser(description='Nmap network scanner')

    parser.add_argument('-H', action = 'store', dest = 'host', required=True)
    parser.add_argument('-p', action = 'store', type =int, dest = 'port', required=True)

    found_args = parser.parse_args()
    # print(found_args.host)
    target_h  = found_args.host
    target_p_new = str(found_args.port)
    '''    
    re writing cuz optarse is old...

    # the general cookie cutter for optparser, make a script guide, make options, and assign vars
    my_parse = OptionParser('Script Guide:'+'-H <target host> -p <target port>')

    my_parse.add_option('-H', dest = 'target_h', type = 'string', help = 'specify a target host')
    my_parse.add_option('-p', dest = 'target_p', type = 'string', help = 'specify a target port')

    (options, args) = my_parse.parse_args()

    # defining info
    target_h = options.target_h
    # make it easier to parse as a string
    target_p_str = str(options.target_p)
    '''


    print('\n:::::::::scan starting on ' + target_h + ':::::::::')
    print()


    # if either option is empty, print the script guide and exit
    if (target_h == None) or (target_p_new[0] == None):
        print(parser.usage)
        # somethigns a bit wacky: doesnt quit if ports arent there, only if host is missing
        print('Err... somethings missing')
        exit(0)

    

    ports = target_p_new.strip("'").split(',')

    # loop through all available ports and call the scan for the individual ports
    for target_port in ports:
        print()
        print('--> port' , str(target_port), '-----------')
        base_scan(target_h, target_port)
        


if __name__ == '__main__':
    main()

# argparse limitts the amount of input to 1 port

# options parse gives ability to search many ports in a string