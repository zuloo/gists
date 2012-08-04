#!/usr/env/bin python

from utils import GithubFacade, encode_auth, Result, download
import gistobj

# Endpoints to gists' github API
ENDPOINT_LIST = "https://api.github.com/users/%s/gists"
ENDPOINT_GIST = "https://api.github.com/gists/%s"


# def list_gists(username=None, password=None):
def list_gists(username=None, password=None):
    """ Retrieve the list of gists. """

    url = ENDPOINT_LIST % (username)

    headers = {}
    if password:
        # if private, set the 'Authentication' header
        encoded_authentication_string = encode_auth(username, password)
        headers["Authorization"] = "Basic " + encoded_authentication_string

    response = GithubFacade().requestEntity(url, headers=headers)

    # put into a table the gists
    if response.ok:
        list_gists = []
        for gist in response.json:
            list_gists.append(gistobj.Gist(gist))

        result = Result()
        result.success = True
        result.data = list_gists
    else:
        result = Result()
        result.success = False
        result.data = ("Can not return the list of gists."
                        " Github reason: '%s'""") % (response.json['message'])
    return result


def get(gist_id, requested_file, destination_dir):

    url = ENDPOINT_GIST % (gist_id)

    response = GithubFacade().requestEntity(url)
    result = Result()

    if response.ok:
        gist_obj = gistobj.Gist(response.json)
        list_names = [gistfile.filename for gistfile in gist_obj.files]
        if len(gist_obj.files) == 1 and not requested_file:
            gistfile = gist_obj.files[0]
            download(gistfile.raw_url, destination_dir,
                    gistfile.filename, gistfile.size)
            result.success = True
            result.data = "File " + gistfile.filename
            result.data += " download successfully."
        else:
            if not requested_file:
                result.success = False
                result.data = ("Gist has more than one file. "
                       "Specify file by '-f' option. Available values are {%s}"
                      ) % (", ".join(list_names))
            else:
                gistfile = gist_obj.getFile(requested_file)
                if gistfile:
                    download(gistfile.raw_url, destination_dir,
                            gistfile.filename, gistfile.size)
                    result.success = True
                    result.data = "File " + gistfile.filename
                    result.data += " download successfully."
                else:
                    result.success = False
                    result.data = ("File not found in gist. "
                         " Available values are {%s}"
                         ) % (", ".join(list_names))

    else:
        result.success = False
        result.data = ("Can not download the gist."
                        " Github reason: '%s'""") % (response.json['message'])

    return result


def show(gist_id, requested_file):
    """ Retrieve a single gist . """

    url = ENDPOINT_GIST % (gist_id)

    response = GithubFacade().requestEntity(url)
    result = Result()

    if response.ok:
        gist_obj = gistobj.Gist(response.json)
        list_names = [gistfile.filename for gistfile in gist_obj.files]
        if len(gist_obj.files) == 1 and not requested_file:
            result.success = True
            result.data = gist_obj.files[0]
        else:
            if not requested_file:
                result.success = False
                result.data = ("Gist has more than one file. "
                       "Specify file by '-f' option. Available values are {%s}"
                      ) % (", ".join(list_names))
            else:
                file_gist = gist_obj.getFile(requested_file)
                if file_gist:
                    result.success = True
                    result.data = file_gist
                else:
                    result.success = False
                    result.data = ("File not found in gist. "
                         " Available values are {%s}"
                         ) % (", ".join(list_names))

    else:
        result.success = False
        result.data = ("Can not show the gist."
                        " Github reason: '%s'""") % (response.json['message'])

    return result
