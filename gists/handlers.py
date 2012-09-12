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

"""

gists.handlers
~~~~~~~~~~~~~~

Handlers module contain all the fuctions that hanlde the input arguments from
the command line, looking for incompatible arguments, and filling configuration
data for the functions in 'actions' module.

"""

import sys
import os
import utils
import literals


# Load the configuration instance once the module is imported
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
        print literals.USER_NOT_FOUND
        sys.exit()

    # If '--private' option, password becomes mandatory. Load it. """
    if args.private:
        token = config.getConfigToken()
        if not token:
            print literals.AUTH_TOKEN_NOT_FOUND
            sys.exit()
    else:
        token = None

    return username, token


def handle_update(args):
    """ Handle the arguments to call the 'update gist' functionality. """

    # get the authentication token from the configuration file
    # If it can not be loaded, raise an exception
    token = config.getConfigToken()
    if not token:
        print literals.AUTH_TOKEN_NOT_FOUND
        sys.exit()

    # Define the source file
    if args.filename:
        if args.input_dir:
            source_file = os.path.join(args.input_dir, args.filename)
        else:
            source_file = os.path.join("./", args.filename)
    else:
        source_file = None

    return (args.gist_id, token, args.description, args.filename,
        source_file, args.new, args.remove)


def handle_post(args):
    """ Handle the arguments to call the 'create gist' functionality. """

    # get the authentication token from the configuration file
    # If it can not be loaded, raise an exception
    token = config.getConfigToken()
    if not token:
        print literals.AUTH_TOKEN_NOT_FOUND
        sys.exit()

    # Define public or private
    if args.private:
        public = False
    else:
        public = True

    # Define the source file
    if args.filename:
        if args.input_dir:
            source_file = os.path.join(args.input_dir, args.filename)
        else:
            source_file = os.path.join("./", args.filename)
    else:
        source_file = None

    return (token, public, args.filename, source_file, args.description)


def handle_show(args):
    """ Handle the arguments to call the 'show' gists functionality. """

    return args.gist_id, args.filename


def handle_get(args):
    """ Handle the arguments to call the 'get' gists functionality. """

    return args.gist_id, args.filename, args.output_dir


def handle_delete(args):
    """ Handle the arguments to call the 'delete' gists functionality. """

    # get the authentication token from the configuration file
    # If it can not be loaded, raise an exception
    token = config.getConfigToken()
    if not token:
        print literals.AUTH_TOKEN_NOT_FOUND
        sys.exit()

    return args.gist_id, token


def handle_authorize(args):
    """ Handle the arguments to call the 'authorize' gists functionality. """
    return args.user, args.secret
