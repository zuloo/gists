#!/usr/bin/env python
from base64 import b64encode
from ConfigParser import ConfigParser
import requests
import urllib2
import os


class Result(object):
    """ Result class.

    To improve the mocking of tests, I created a 'result'
    class, always returned by the 'main()' method of the
    main module.
    """
    def __init__(self):
        self.success = False
        self.data = None


class GithubFacade(object):
    """ It executes all the calls to Github.

    Although it is a trivial class, it is useful to mock its behavior
    in tests and encapsulates the 'request' dependency
    """

    def __init__(self):
        """ Nothing to do. """

    def requestEntity(self, url, headers={}):
        return requests.get(url, headers=headers)


def format_table(table_gists):
    """ Print table using the max_width of each column.

    Seen on stackoverflow: http://goo.gl/h9yla
    """

    # Reorganize data by columns
    cols = zip(*table_gists)

    # Compute column widths by taking maximum lenght of values per column
    col_widths = [max(len(value) for value in col) for col in cols]

    # Create a suitable format string
    format_string = '  |  '.join(['%%%ds' % width for width in col_widths])

    string_table = ""
    # Print each row using the computed format
    for i in range(len(table_gists)):
        row = table_gists[i]
        row_string = format_string % (tuple(row))
        if i == 0:
            # print header
            string_table += row_string + "\n"
            string_table += "=" * len(row_string) + "\n"
        else:
            string_table += row_string + "\n"

    return string_table


def encode_auth(username, password):
    """ Return the encoded user:password. """

    # Here because is needed in all commands, and it is a way to don't
    # import b64encode function everywhere.
    return b64encode(username + ":" + password)


class GistsConfigurer(object):
    """ Justs handles data from the config file. """

    def __init__(self):
        """ Initializes the 'ConfigParser' instance. """
        self.config = ConfigParser()
        self.config.read([os.path.expanduser('~/.gists.rc')])

    def getFileConfigUser(self):
        """ Returns the user from the configuration file.

        If configuration instance con not load 'credentials' section,
        or user is not configured, it return none.
        """
        if not self.config.has_section('credentials'):
            print "Configuration file not found or not valid"
            return None
        username = self.config.get('credentials', 'user')
        return username

    def getConfigFilePassword(self):
        """ Loads the password from configuration instance.

        If configuration instance can not load the password returns None
        """
        if not self.config.has_section('credentials'):
            print "Configuration file not found or not valid"
            return None
        password = self.config.get('credentials', 'password')
        return password


def download(url, destination_dir, file_name, file_size):
    destination_path = os.path.join(destination_dir, file_name)
    print ("Downloading: %s\nTo: %s\nBytes: %s"
            % (url, destination_path, file_size))
    u = urllib2.urlopen(url)
    with open(destination_path, 'wb') as f:
        raw_file = u.read()
        f.write(raw_file)
