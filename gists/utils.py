#!/usr/bin/env python
from base64 import b64encode
from ConfigParser import ConfigParser
import json
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


ENDPOINT_LIST = "https://api.github.com/users/%s/gists"
ENDPOINT_GIST = "https://api.github.com/gists/%s"
ENDPOINT_CREATE = "https://api.github.com/gists"


class GithubFacade(object):
    """ It executes all the calls to Github.

    Although it is a trivial class, it is useful to mock its behavior
    in tests and encapsulates the 'request' dependency
    """
    # Endpoints to gists' github API

    def __init__(self):
        """ Nothing to do. """

    def request_list_of_gists(self, username, password=None):
        headers = {}
        url = ENDPOINT_LIST % (username)
        if password:
            headers = encode_auth_header(username, password)
        return requests.get(url, headers=headers)

    def request_gist(self, id_gist):
        url = ENDPOINT_GIST % (id_gist)
        return requests.get(url)

    def create_gist(self, payload, username, password):
        headers = encode_auth_header(username, password)
        url = ENDPOINT_CREATE
        data_json = json.dumps(payload, indent=2)
        return requests.post(url, data=data_json, headers=headers)

    def update_gist(self, payload, username, password):
        url = ENDPOINT_GIST % (payload.identifier)
        headers = encode_auth_header(username, password)
        data_json = json.dumps(payload, indent=2)
        return requests.patch(url, data=data_json, headers=headers)

    def delete_gist(self, id_gist, username, password):
        url = ENDPOINT_GIST % (id_gist)
        headers = encode_auth_header(username, password)
        return requests.delete(url, headers=headers)


def encode_auth_header(username, password):
    """ Return the encoded user:password. """

    # Here because is needed in all commands, and it is a way to don't
    # import b64encode function everywhere.
    headers = {}
    encoded_authentication_string = b64encode(username + ":" + password)
    headers["Authorization"] = "Basic " + encoded_authentication_string
    return headers


class GistsConfigurer(object):
    """ Justs handles data from the config file. """

    def __init__(self):
        """ Initializes the 'ConfigParser' instance. """
        self.config = ConfigParser()
        self.config.read([os.path.expanduser('~/.gistsrc')])

    def getConfigUser(self):
        """ Returns the user from the configuration file.

        If configuration instance con not load 'credentials' section,
        or user is not configured, it return none.
        """
        if not self.config.has_section('credentials'):
            print "Configuration file not found or not valid"
            return None
        username = self.config.get('credentials', 'user')
        return username

    def getConfigPassword(self):
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


def build_result(success, data, *args):
    result = Result()
    result.success = success
    if not args:
        result.data = data
    else:
        result.data = data % (args)
    return result
