#!/usr/bin/env python
import utils
import requests


# Endpoint to gists' github API
ENDPOINT = "https://api.github.com/users/%s/gists"


def list_gists(username=None, password=None):
    """ Retrieve the list of gists. """

    url = ENDPOINT % (username)

    headers = {}
    if password:
        # if private, set the 'Authentication' header
        encoded_authentication_string = utils.encode_auth(username, password)
        headers["Authorization"] = "Basic " + encoded_authentication_string

    response = requests.get(url, headers=headers)

    # put into a table the gists
    table_gists = []
    header = []
    header.append("id")
    header.append("description")
    header.append("files")
    table_gists.append(header)
    if response.ok:
        for gist in response.json:
            row = []
            row.append(gist['id'].encode("utf8"))
            row.append(gist['description'].encode("utf8"))
            stringfiles = ""
            for filegist in gist['files']:
                if stringfiles != "":
                    stringfiles += ", "
                stringfiles += filegist
            row.append(stringfiles)
            table_gists.append(row)
        result = utils.Result()
        result.result_code = 'OK'
        result.data = utils.format_table(table_gists)
    else:
        result = utils.Result()
        result.result_code = 'NOK'
        result.data += ("Can not return the list of gists."
                        " Github reason: '%s '""") % (response.json['message'])
    return result
