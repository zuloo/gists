#!/usr/bin/env python

import sys
import argparse
import os
import ConfigParser
from commands import list_gists


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


parser = argparse.ArgumentParser(
        description='Manage Github gists from CLI',
        epilog="Happy Gisting!")
parser.add_argument("-p", "--private",
        help="Return the private gists besides the public ones",
        action="store_true")
parser.add_argument("-u", "--user",
        help="""Specify the user to retrieve his gists.
                    Overrides the default 'user' in configuration file""")
parser.add_argument("-s", "--secret",
        help="""Specify the password to retrieve private gists.
                    Overrides the default 'secret' in configuration file""")
parser.add_argument("action",
        help="""Action to execute. Accepted values are [list|get|show].
                    Default is 'list'""",
                    )
args = parser.parse_args()

# Load the configuration file
config = __config_instance()

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

# Execute the action
try:

    {
            'list': lambda: list_gists(username=username, password=password)
    }[args.action]()

except KeyError:
    print """Undefined action. Expected values are [list|get|show]"""
    sys.exit()
