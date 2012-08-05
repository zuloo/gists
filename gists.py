#!/usr/bin/env python
import argparse
import utils
from actions import list_gists, show, get, post, delete, update
from handlers import handle_list, handle_show, handle_update
from handlers import handle_get, handle_post, handle_delete
from formatters import format_list, format_post, format_update
from formatters import format_get, format_show, format_delete


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
    parser_show = subparsers.add_parser("show", help="Show a single gist file")
    parser_show.add_argument("gist_id",
            help="Identifier of the gist to retrieve")
    parser_show.add_argument("-f", "--filename",
            help=("Specify gist file to show. "))
    parser_show.add_argument("-m", "--metadata", action="store_true")
    parser_show.set_defaults(handle_args=handle_show, func=show,
            formatter=format_show)

    # Add the subparser to handle the 'get' action
    parser_get = subparsers.add_parser("get",
            help="Download a single gist file")
    parser_get.add_argument("gist_id",
            help="Identifier of the gist to retrieve")
    parser_get.add_argument("-f", "--filename",
            help=("Specify gist file to show. "
                "Useful when gist has more than one file"))
    parser_get.add_argument("-t", "--target_dir",
            help=("Specify the destination directory"),
            default=".")
    parser_get.set_defaults(handle_args=handle_get, func=get,
            formatter=format_get)

    # Add the subparser to handle the 'create' action
    parser_post = subparsers.add_parser("create",
            help="Create a new gist")
    parser_post.add_argument("-f", "--file",
            help=("Specify gist file to upload."), required=True)
    parser_post.add_argument("-u", "--user",
            help="""Github user.
                        Overrides the default 'user' in configuration file""")
    parser_post.add_argument("-s", "--secret",
            help="""Github password.
                        Overrides the default 'secret' in configuration
                        file""")
    parser_post.add_argument("-p", "--private",
            help="""Specify you want to create a private gist
            (public by default)""",
            action="store_true")
    parser_post.add_argument("-d", "--description",
            help="Specify a description for the gist to create")
    parser_post.set_defaults(handle_args=handle_post, func=post,
            formatter=format_post)

    # Add the subparser to handle the 'update' action
    parser_update = subparsers.add_parser("update",
            help="Update a gist")
    parser_update.add_argument("gist_id",
            help="Identifier of the gist to update")
    parser_update.add_argument("-u", "--user",
            help="""Github user. Overrides the default
            'user' in configuration file""")
    parser_update.add_argument("-s", "--secret",
            help="""Github password.
                        Overrides the default 'secret' in configuration
                        file""")
    group1 = parser_update.add_argument_group('file options',
            'Update Gist files')
    group1.add_argument("-f", "--filename",
             help=("Specify gist file to update."))
    group11 = group1.add_mutually_exclusive_group()
    group11.add_argument("-n", "--new", action="store_true", parents=:w)
    group11.add_argument("-r", "--remove", action="store_true")
    group2 = parser_update.add_argument_group('metadata options',
            'Update Gist General Data')
    group2.add_argument("-d", "--description", action="store_true",
            help="Set the gist description")
    group2.add_argument("-p", "--private", choices=["true", "false"],
            help="Set the gist private or public")
    parser_update.set_defaults(handle_args=handle_update, func=update,
            formatter=format_update)

    # Add the subparser to handle the 'delete' action
    parser_delete = subparsers.add_parser("delete", help="Delete a gist")
    parser_delete.add_argument("gist_id",
            help="Identifier of the gist to delete")
    parser_delete.add_argument("-u", "--user",
            help="""User to perform the action.
                        Overrides the default 'user' in configuration file""")
    parser_delete.add_argument("-s", "--secret",
            help="""Password to authenticate.
                        Overrides the default 'secret' in configuration
                        file""")
    parser_delete.set_defaults(handle_args=handle_delete, func=delete,
            formatter=format_delete)

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
