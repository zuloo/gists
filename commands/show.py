#!/usr/bin/env python
import requests
import os
from clint.textui import colored

ENDPOINT = "https://api.github.com/gists/%s"


def __print_gist(file_gist):
    """ Pretty prints the gist. """
    rows, columns = os.popen('stty size', 'r').read().split()
    print colored.cyan('-' * int(columns))
    print colored.green("Language:"), colored.red(file_gist['language'])
    print colored.green("Filename:"), colored.red(file_gist['filename'])
    print colored.green("Size:"), colored.red(file_gist['size'])
    print colored.green("Content:\n\n") + file_gist['content'] + "\n\n"
    print colored.cyan('-' * int(columns))


def show(gist_id, filename):
    """ Retrieve a single gist . """

    url = ENDPOINT % (gist_id)

    response = requests.get(url)

    if response.ok:
        if len(response.json['files'].keys()) > 1:
            if not filename:
                print ("Gist has more than one file. "
                       "Specify file by '-f' option. Available values are {%s}"
                      ) % (", ".join(response.json['files'].keys()))
            else:
                for candidate_name in response.json['files'].keys():
                    if filename == candidate_name:
                        file_gist = response.json['files'][filename]
                        __print_gist(file_gist)
                        return
                print "File not found in gist"
        else:
            filename = response.json['files'].keys()[0]
            file_gist = response.json['files'][filename]
            __print_gist(file_gist)
    else:
        print "Can not show the gist."
        print "Github reason: '", response.json['message'], "'"
