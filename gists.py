#!/usr/bin/env python

import requests
import sys
import json
import argparse
import base64
import os
import ConfigParser
from clint.textui import colored
import logging

def list_gists(private=False, username=None, password=None):
    url = "https://api.github.com/users/%s/gists" % (username)

    headers = {}
    if private: # if private, set the 'Authentication' header
        encoded_authentication_string = base64.b64encode(username + ":" + password)
        headers["Authorization"] = "Basic " + encoded_authentication_string

    gists = requests.get(url, headers = headers)

    # put into a table the gists
    table_gists = []
    header = []
    header.append("id")
    header.append("description")
    header.append("files")
    table_gists.append(header)
    if gists.ok:
        for gist in gists.json:
            row = []
            row.append(gist['id'].encode("utf8"))
            row.append(gist['description'].encode("utf8"))
            row.append(str(len(gist['files'])))
            table_gists.append(row)

    _print_table(table_gists)

def _print_table(table_gists):
    """ Print table using the max_width of each column.

    Seen on http://stackoverflow.com/questions/3685195/line-up-columns-of-numbers-print-output-in-table-format.
    """

    # Reorganize data by columns
    cols = zip(*table_gists)

    # Compute column widths by taking maximum lenght of values per column
    col_widths = [ max(len(value) for value in col) for col in cols]

    # Create a suitable format string
    format_string = '  |  '.join(['%%%ds' % width for width in col_widths])

    # Print each row using the computed format
    for i in range(len(table_gists)):
        row = table_gists[i]
        row_string = format_string % (tuple(row))
        if i == 0:
            # print header
            print row_string
            print "="*len(row_string)
        else:
            print row_string

def load_credentials():
    """ Loads the user and password credentials from configuration file.

    Loads the user credentials, using the configuration file.
    If configuration file not found, returns None, None
    """
    home_directory = os.path.expanduser('~')
    config_file = '.gists.rc'
    config = ConfigParser.ConfigParser()
    config.read([os.path.expanduser('~/.gists.rc')])
    if not config.has_section('credentials'):
        print "Configuration file not found or not valid"
        return None, None
    username = config.get('credentials', 'user')
    password = config.get('credentials', 'password')
    return username, password


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manage Github gists from CLI')
    parser.add_argument("-p", "--private", 
            help="Return the private gists besides the public ones", action="store_true") 
    parser.add_argument("-u", "--user", 
            help="Specify the user to retrieve his gists. Overrides the default 'user' in configuration file")
    parser.add_argument("-s", "--secret", 
            help="Specify the password to retrieve private gists. Overrides the default 'secret' in configuration file")
    args = parser.parse_args()

    # load the credentials from the configuration file
    username, password = load_credentials()

    # Get the 'user' argument if exists
    if args.user:
        if args.user != username:
            # In this case, we are trying to retrieve the gists from another
            # user. We reset the password because we want to avoid return
            # nothing if we do something like this:
            # $ gists -u another_user --private
            # in this case, the policy is to return only the public ones and 
            # avoid the 'Unauthorized' exception
            username = args.user
            password = None

    # Check if we have to retrieve private gists.
    private_gists = False
    if args.private:
        private_gists = True
        # Check if we have to override password
        if args.secret:
            password = args.secret
        # Check if we have actually a password
        if not password:
            print "Password should be informed via configuration file or '-s' argument"
            sys.exit()

    list_gists(private=private_gists, username=username, password=password)
