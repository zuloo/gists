#!/usr/bin/env python

import sys
import argparse
import os
import ConfigParser
from commands import list_gists, show


def __getUser(config):
    """ Loads the user from configuration instance.

    If configuration instance can not load user returns None
    """
    if not config.has_section('credentials'):
        print "Configuration file not found or not valid"
        return None
    username = config.get('credentials', 'user')
    return username


def __getPassword(config):
    """ Loads the password from configuration instance.

    If configuration instance can not load the password returns None
    """
    if not config.has_section('credentials'):
        print "Configuration file not found or not valid"
        return None
    password = config.get('credentials', 'password')
    return password


def __config_instance():
    """ Gets the config instance loading the configuration file. """
    config = ConfigParser.ConfigParser()
    config.read([os.path.expanduser('~/.gists.rc')])
    return config


def __handle_list(config, args):
    """ Handle the arguments to call the 'list gists' functionality. """

    # Get the 'user' argument if exists, otherwise take it from configuration
    # file. If 'user' can not be loaded, raise an exception
    if args.user:
        username = args.user
    else:
        username = __getUser(config)
    if not username:
        print """Can not load github username neither from '--user (-u)'
                parameter nor configuration file.  """
        sys.exit()

    # If '--private' option, password becomes mandatory. Load it. """
    if args.private:
        # Get it from argument line
        if args.secret:
            password = args.secret
        else:
            password = __getPassword(config)
        # Check if we have actually a password
        if not password:
            print """Password should be informed via
                     configuration file or '-s' argument"""
            sys.exit()
    else:
        password = None

    list_gists(username=username, password=password)


def __handle_show(config, args):
    """ Handle the arguments to call the 'show' gists functionality. """
    show(args.gist_id, args.filename)


def main(*args, **kwargs):

    # Load the configuration instance
    config = __config_instance()

    parser = argparse.ArgumentParser(
            description='Manage Github gists from CLI',
            epilog="Happy Gisting!")

    subparsers = parser.add_subparsers(help="Available actions. ")

    # Add the subparser to handle the list of gists
    parser_list = subparsers.add_parser("list", help="List gists ")
    parser_list.add_argument("-s", "--secret",
            help="""Specify the password to retrieve private gists.
                        Overrides the default 'secret' in configuration
                        file""")
    parser_list.add_argument("-p", "--private",
            help="Return the private gists besides the public ones",
            action="store_true")
    parser_list.add_argument("-u", "--user",
            help="""Specify the user to retrieve his gists.
                        Overrides the default 'user' in configuration file""")
    parser_list.set_defaults(func=__handle_list)

    # Add the subparser to handle the 'show' action
    parser_get = subparsers.add_parser("show", help="Show a single gist file")
    parser_get.add_argument("gist_id",
            help="Identifier of the gist to retrieve")
    parser_get.add_argument("-f", "--filename",
            help="Specify gist file to show. Useful when gist has more than one file")
    parser_get.set_defaults(func=__handle_show)

    args = parser.parse_args()
    args.func(config, args)

if __name__ == '__main__':
    main()
