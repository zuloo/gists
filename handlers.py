#!/usr/bin/env python
import sys


def handle_list(config, args):
    """ Handle the arguments to call the 'list gists' functionality. """

    # Get the 'user' argument if exists, otherwise take it from configuration
    # file. If 'user' can not be loaded, raise an exception
    if args.user:
        username = args.user
    else:
        username = config.getFileConfigUser()
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
            password = config.getConfigFilePassword()
        # Check if we have actually a password
        if not password:
            print """Password should be informed via
                     configuration file or '-s' argument"""
            sys.exit()
    else:
        password = None

    return username, password


def handle_show(config, args):
    """ Handle the arguments to call the 'show' gists functionality. """
    return args.gist_id, args.filename


def handle_get(config, args):
    """ Handle the arguments to call the 'get' gists functionality. """
    return args.gist_id, args.filename, args.destination_dir
