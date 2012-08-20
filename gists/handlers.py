# Copyright (c) 2012 <Jaume Devesa (jaumedevesa@gmail.com)>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import os
import utils

config = utils.GistsConfigurer()


def handle_list(args):
    """ Handle the arguments to call the 'list gists' functionality. """

    # Get the 'user' argument if exists, otherwise take it from configuration
    # file. If 'user' can not be loaded, raise an exception
    if args.user:
        username = args.user
    else:
        username = config.getConfigUser()
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
            password = config.getConfigPassword()
        # Check if we have actually a password
        if not password:
            print """Password should be informed via
                     configuration file or '-s' argument"""
            sys.exit()
    else:
        password = None

    return username, password


def handle_update(args):
    # Get the 'user' argument if exists, otherwise take it from configuration
    # file. If 'user' can not be loaded, raise an exception
    if args.user:
        username = args.user
    else:
        username = config.getConfigUser()
    if not username:
        print """Can not load github username neither from '--user (-u)'
                parameter nor configuration file.  """
        sys.exit()

    # Get the 'secret' argument if exists, otherwise take it from configuration
    # file. If 'secret' can not be loaded, raise an exception
    if args.secret:
        password = args.secret
    else:
        password = config.getConfigPassword()
    if not password:
        print """Can not load github password neither from '--secret (-s)'
                parameter nor configuration file.  """
        sys.exit()

    if args.filename:
        if args.input_dir:
            source_file = os.path.join(args.input_dir, args.filename)
        else:
            source_file = os.path.join("./", args.filename)
    else:
        source_file = None

    return (args.gist_id, username, password, args.description,
            args.filename, source_file, args.new, args.remove)


def handle_post(args):
    # Get the 'user' argument if exists, otherwise take it from configuration
    # file. If 'user' can not be loaded, raise an exception
    if args.user:
        username = args.user
    else:
        username = config.getConfigUser()
    if not username:
        print """Can not load github username neither from '--user (-u)'
                parameter nor configuration file.  """
        sys.exit()

    # Get the 'secret' argument if exists, otherwise take it from configuration
    # file. If 'secret' can not be loaded, raise an exception
    if args.secret:
        password = args.secret
    else:
        password = config.getConfigPassword()
    if not password:
        print """Can not load github password neither from '--secret (-s)'
                parameter nor configuration file.  """
        sys.exit()

    if args.private:
        public = False
    else:
        public = True

    return username, password, public, args.file, args.description


def handle_show(args):
    """ Handle the arguments to call the 'show' gists functionality. """
    return args.gist_id, args.filename


def handle_get(args):
    """ Handle the arguments to call the 'get' gists functionality. """
    return args.gist_id, args.filename, args.target_dir


def handle_delete(args):
    # Get the 'user' argument if exists, otherwise take it from configuration
    # file. If 'user' can not be loaded, raise an exception
    if args.user:
        username = args.user
    else:
        username = config.getConfigUser()
    if not username:
        print ("Can not load github username neither from '--user (-u)'"
               "parameter nor configuration file.")
        sys.exit()

    # Get the 'secret' argument if exists, otherwise take it from configuration
    # file. If 'secret' can not be loaded, raise an exception
    if args.secret:
        password = args.secret
    else:
        password = config.getConfigPassword()
    if not password:
        print """Can not load github password neither from '--secret (-s)'
                parameter nor configuration file.  """
        sys.exit()

    return args.gist_id, username, password


def handle_configure(args):
    return args.user, args.secret
