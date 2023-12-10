# flrigs-coordinator.py
# Authors: Steve, N8IFQ.  Sean, W8FU
# Organization: Flying Beers International Radio Club
# Description: A script to coordinate multiple radios controlled by flrig.

import xmlrpc.client
import configparser
import sys
import argparse

version = "1.0"
config_file = 'flrigs_coordinator.ini'


def flrigs_init(config_file):
    cfg = configparser.ConfigParser()
    cfg.read(config_file)
    return cfg


def connect(radio, cfg):
    try:
        if not cfg.has_section(radio):
            raise Exception(f'No configuration defined for {radio}')

        server = cfg[radio]['server']
        port = cfg[radio]['port']
        server_url = f'http://{server}:{port}'

        # Connect to the flrig server
        flrig = xmlrpc.client.ServerProxy(server_url)
        version = flrig.main.get_version()

        try:
            if args.debug:
                print(f'{radio}: Connected to flrig version {version} at {server_url}')

        except NameError:
            pass


        return flrig

    except Exception as e:
        print(str(e))
        sys.exit()


def show(args):
    if args.debug:
        print(f'{args.radio}: {config[args.radio]["description"]}')

    show_radio(args.radio, config)


def show_radio(radio, cfg):
    flrig = connect(radio, cfg)

    power = flrig.rig.get_power()
    frequency = flrig.rig.get_vfo()
    mode = flrig.rig.get_mode()

    print(f'{radio}: "{cfg[radio]["description"]}" {frequency}Hz {mode} {power}W')
    return


def save(args):
    save_radio(args.radio, config)


def save_radio(radio, cfg):
    flrig = connect(radio, cfg)
    if args.debug:
        print(f'{radio}: {cfg[radio]["description"]}')

    frequency = flrig.rig.get_vfo()
    mode = flrig.rig.get_mode()

    cfg[args.radio]['frequency'] = frequency
    cfg[args.radio]['mode'] = mode

    try:
        with open(args.config, 'w') as configfile:
            config.write(configfile)

        print(f'Saving {radio} settings of {frequency} {mode}')

    except Exception as e:
        print(str(e))
        sys.exit()


def restore(args):
    if args.debug:
        print(f'{args.radio}: {config[args.radio]["description"]}')

    restore_radio(args.radio, config)


def restore_radio(radio, cfg):
    flrig = connect(radio, cfg)
    frequency = cfg[radio]['frequency']
    mode = cfg[radio]['mode']

    print(f'Resorting {radio} to {frequency} {mode}')
    flrig.rig.set_vfo(float(frequency))
    flrig.rig.set_mode(mode)


def set(args):
    if args.debug:
        print(f'In Set Function. src={args.src_radio} dest={args.dest_radio}')

    set_radio(args.src_radio, args.dest_radio, config)


def set_radio(src_radio, dest_radio, cfg):
    src_flrig = connect(src_radio, cfg)
    dest_flrig = connect(dest_radio, cfg)

    # Get the Source values
    src_frequency = src_flrig.rig.get_vfo()
    src_mode = src_flrig.rig.get_mode()

    # Set the Destination Location
    dest_flrig.rig.set_vfo(float(src_frequency))
    dest_flrig.rig.set_mode(src_mode)

    print(f'Copy settings from {src_radio} to {dest_radio} : {src_frequency} {src_mode}')


def swap(args):
    if args.debug:
        print(f'In Swap Function. src={args.src_radio} dest={args.dest_radio}')
    swap_radio(args.src_radio, args.dest_radio, config)


def swap_radio(src_radio, dest_radio, cfg):
    src_flrig = connect(src_radio, cfg)
    dest_flrig = connect(dest_radio, cfg)

    # Temp store the values
    tmp_frequency = dest_flrig.rig.get_vfo()
    tmp_mode = dest_flrig.rig.get_mode()

    # Set Dest Radio to Src Radio Values
    dest_flrig.rig.set_vfo(float(src_flrig.rig.get_vfo()))
    dest_flrig.rig.set_mode(src_flrig.rig.get_mode())

    # Set Src Radio to saved values
    src_flrig.rig.set_vfo(float(tmp_frequency))
    src_flrig.rig.set_mode(tmp_mode)

    print(f'Swap settings from {args.src_radio} to {args.dest_radio}')


if __name__ == "__main__":
    # Argument Handling
    parser = argparse.ArgumentParser(
        prog="flrigs_coordinator",
        description="Coordinate settings across multiple flrig instances",
        argument_default=argparse.SUPPRESS
    )
    subparsers = parser.add_subparsers()

    parser_show = subparsers.add_parser('show', help="Display current radio settings")
    parser_show.add_argument('radio')
    parser_show.set_defaults(func=show)

    parser_save = subparsers.add_parser('save', help="Store the current radio settings")
    parser_save.add_argument('radio')
    parser_save.set_defaults(func=save)

    parser_restore = subparsers.add_parser('restore', help="Restore the radio settings from saved values")
    parser_restore.add_argument('radio')
    parser_restore.set_defaults(func=restore)

    parser_set = subparsers.add_parser('set', help="Set destination radio to match the source radio settings")
    parser_set.add_argument("src_radio")
    parser_set.add_argument("dest_radio")
    parser_set.set_defaults(func=set)

    parser_swap = subparsers.add_parser('swap', help="Swap the settings between two radios")
    parser_swap.add_argument("src_radio")
    parser_swap.add_argument("dest_radio")
    parser_swap.set_defaults(func=swap)

    parser.add_argument("-v", "--version", action="version", version="%(prog)s " + version)
    parser.add_argument("-c", "--config", action="store", default=config_file)
    parser.add_argument("-d", "--debug", action="store_true", default=False)

    # If not options, print help and exit.
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    args = parser.parse_args()
    config = flrigs_init(args.config)

    # Argparser handles dispatch to CLI options.
    args.func(args)
