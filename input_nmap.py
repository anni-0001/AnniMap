import nmap
from optparse import OptionParser
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
    print_state = 'State ERR'


    # adding in color to the command line interface
    if state == 'open':
        print_state = colors.color.YELLOW +'<OPEN>'+ colors.color.END
    elif state == 'closed':
        print_state = colors.color.RED +'<CLOSED>'+ colors.color.END
        


    print('------->' + ' tcp/'+ target_p+ ' '+ print_state )




def main():
    # the general cookie cutter for optparser, make a script guide, make options, and assign vars
    my_parse = OptionParser('Script Guide:'+'-H <target host> -p <target port>')

    my_parse.add_option('-H', dest = 'target_h', type = 'string', help = 'specify a target host')
    my_parse.add_option('-p', dest = 'target_p', type = 'string', help = 'specify a target port')

    (options, args) = my_parse.parse_args()

    # defining info
    target_h = options.target_h
    # make it easier to parse as a string
    target_p_str = str(options.target_p)


    print('\n:::::::::scan starting on ' + target_h + ':::::::::')
    print()


    # if either option is empty, print the script guide and exit
    if (target_h == None) or (target_p_str[0] == None):
        print(my_parse.usage)
        # somethigns a bit wacky: doesnt quit if ports arent there, only if host is missing
        print('Err... somethings missing')
        exit(0)

    

    ports = target_p_str.strip("'").split(',')

    # loop through all available ports and call the scan for the individual ports
    for target_port in ports:
        print()
        print('--> port' , str(target_port), '-----------')
        base_scan(target_h, target_port)
        


if __name__ == '__main__':
    main()

