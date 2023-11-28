import xmlrpc.client
import time
import configparser
import getopt, sys

# Default config file.
config_file = 'flrigs-coordinator.ini'

def display_help():
    print('W8FU Radio Interface Coordinator')
    print('Config File is: {config_file}')

    print('-h or --Help    Display this message')
    print('-c or --config  Specify config file')

    print('Radio A Options')
    print('-a or --show_a   Display Radio A settings')
    print('--save_a         Save Radio A settings')
    print('--restore_a      Restore Radio A settings')

    print('Radio B Options')
    print('-b or --show_b   Display Radio B settings')
    print('--save_b         Save Radio B settings')
    print('--restore_b      Restore Radio B settings')
    
    print('Functions')
    print('--set_a_b        Copy settings from Radio A to Radio B [A->B]')
    print('--set_b_a        Copy settings from Radio B to Radio A [B->A]')

    print('Configuration')
    print('Radio A is ', display_radio(config, 'A'))
    print('Radio B is ', display_radio(config, 'B'))


def display_radio(config, radio):
    section = f'RADIO{radio}'

    # Connect to the flrig server
    name = config[section]['name']
    server = config[section]['server']
    port = config[section]['port']
    server_url = f'http://{server}:{port}'

    flrig = xmlrpc.client.ServerProxy(server_url)
    #version = flrig.main.get_version()
    #print(f'Connected to flrig version {version} at {server_url}')

    power = flrig.rig.get_power()
    frequency = flrig.rig.get_vfo()
    mode = flrig.rig.get_mode()
    return f'{name} {frequency}Hz {mode} {power}W'

def save_radio(config, radio):
    section = f'RADIO{radio}'

    # Connect to the flrig server
    name = config[section]['name']
    server = config[section]['server']
    port = config[section]['port']
    server_url = f'http://{server}:{port}'

    flrig = xmlrpc.client.ServerProxy(server_url)
    frequency = flrig.rig.get_vfo()
    mode = flrig.rig.get_mode()

    config[section]['frequency'] = frequency
    config[section]['mode'] = mode
    with open(config_file, 'w') as configfile:
        config.write(configfile)

def restore_radio(config, radio):
    section = f'RADIO{radio}'

    frequency = config[section]['frequency']
    mode = config[section]['mode']
    
    # Connect to the flrig server
    name = config[section]['name']
    server = config[section]['server']
    port = config[section]['port']
    server_url = f'http://{server}:{port}'

    print(f'Resorting {name} to {frequency} {mode}')
    flrig = xmlrpc.client.ServerProxy(server_url)
    flrig.rig.set_vfo(float(frequency))
    flrig.rig.set_mode(mode)

def cross_set(config, src, dest):
    src_section = f'RADIO{src}'
    dest_section = f'RADIO{dest}'

    # Get the Source values
    src_name = config[src_section]['name']
    src_server = config[src_section]['server']
    src_port = config[src_section]['port']

    src_flrig = xmlrpc.client.ServerProxy(f'http://{src_server}:{src_port}')
    src_frequency = src_flrig.rig.get_vfo()
    src_mode = src_flrig.rig.get_mode()

    # Get the Destination Location
    dest_name = config[dest_section]['name']
    dest_server = config[dest_section]['server']
    dest_port = config[dest_section]['port']

    dest_flrig =  xmlrpc.client.ServerProxy(f'http://{dest_server}:{dest_port}')
    dest_flrig.rig.set_vfo(float(src_frequency))
    dest_flrig.rig.set_mode(src_mode)

    print(f'Copy settings from  {src_name} to {dest_name}: {src_frequency} {src_mode}')


# Get Configuration 
config = configparser.ConfigParser()

argumentList = sys.argv[1:]
options = "habc"
long_options = ["help", "config", "show_a", "show_b", "set_b_a", "set_a_b", "save_a", "save_b", "restore_a","restore_b"]

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # Check for config file specification
    for currentArgument, currentValue in arguments:
         if currentArgument in ("-c", "--config"):
            config_file = currentValue

    # Get config data
    config.read(config_file)

    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-h", "--help"):
            display_help()

        elif currentArgument in ("-a", "--show_a"):
            print ("Radio A: ", display_radio(config, 'A'))
        
        elif currentArgument in ("-b", "--show_b"):
            print ("Radio B: ", display_radio(config, 'B'))
             
        elif currentArgument in ("--save_a"):
            print ("Saving Radio A state")
            save_radio(config, 'A')

        elif currentArgument in ("--save_b"):
            print ("Saving Radio B state")
            save_radio(config, 'B')

        elif currentArgument in ("--restore_a"):
            print ("Restoring Radio A state")
            restore_radio(config, 'A')

        elif currentArgument in ("--restore_b"):
            print ("Restoring Radio B state")
            restore_radio(config, 'B')

        elif currentArgument in ("--set_a_b"):
            print ("Setting Radio A to match Radio B")
            cross_set(config, 'A', 'B')

        elif currentArgument in ("--set_b_a"):
            print ("Setting Radio B to match Radio A")
            cross_set(config, 'B', 'A')
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))

sys.exit()