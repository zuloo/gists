#!/usr/bin/env python

import argparse
import utils
from actions import list_gists, show, get
from handlers import handle_list, handle_show, handle_get
from formatters import format_list, format_show, format_get


def main(*args, **kwargs):

    # Load the configuration instance
    config = utils.GistsConfigurer()

    parser = argparse.ArgumentParser(
            description='Manage Github gists from CLI',
            epilog="Happy Gisting!")

    # define subparsers to handle each action
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
    parser_list.set_defaults(handle_args=handle_list,
            func=list_gists, formatter=format_list)

    # Add the subparser to handle the 'show' action
    parser_get = subparsers.add_parser("show", help="Show a single gist file")
    parser_get.add_argument("gist_id",
            help="Identifier of the gist to retrieve")
    parser_get.add_argument("-f", "--filename",
            help=("Specify gist file to show. "
                "Useful when gist has more than one file"))
    parser_get.set_defaults(handle_args=handle_show, func=show,
            formatter=format_show)

    # Add the subparser to handle the 'get' action
    parser_get = subparsers.add_parser("get",
            help="Download a single gist file")
    parser_get.add_argument("gist_id",
            help="Identifier of the gist to retrieve")
    parser_get.add_argument("-f", "--filename",
            help=("Specify gist file to show. "
                "Useful when gist has more than one file"))
    parser_get.add_argument("-d", "--destination_dir",
            help=("Specify the destination directory"),
            default=".")
    parser_get.set_defaults(handle_args=handle_get, func=get,
            formatter=format_get)

    # parse the arguments
    args = parser.parse_args()

    # calling the handle_args function defined, parsing the args and return
    # and object with the needed values to execute the function
    parameters = args.handle_args(config, args)

    # passing the 'parameters' object as array of parameters
    result = args.func(*parameters)

    # parsing the 'result' object to be output formatted.
    # (that must be a single object)
    result_formatted = args.formatter(result)
    print result_formatted


if __name__ == '__main__':
    main()
