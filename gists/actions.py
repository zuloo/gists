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

# 'actions' module is the responsible to execute the business logic of each one
# of the available actions, call the GithubFacade to retrieve the
# Github API response, and handles errors and responses.

from utils import download, build_result, GistsConfigurer
import literals
import model
import os

"""

gists.actions
~~~~~~~~~~~~~~~~

Actions is the main module of the package. It receives data from the 'handlers'
module, call to GitHub Gists API and manage the response.


"""

def get_json(request):
    """ Retrieve JSON of from request

    :param request: the request
    """
    if callable(request.json):
        return request.json()
    else: 
        return request.json

def list_gists(username, facade, want_starred):
    """ Retrieve the list of gists for a concrete user.

    :param token: GitHub authentication token
    :param facade: instance of the object that actually performs the request
    :param want_starred: if we want the starred ones
    """

    if not want_starred:
        response = facade.request_list_of_gists(username)
    else:
        response = facade.request_list_starred_gists(username)

    if response.ok:
        # List of gists for the requested user found.
        list_gists = []
        for gist in get_json(response):
            list_gists.append(model.Gist(gist))

        return build_result(True, list_gists)
    else:
        # GitHub response error. Parse the response
        return build_result(False, literals.LISTS_ERROR,
                            get_json(response)['message'])


def get(gist_id, requested_file, destination_dir, facade):
    """ Download a gist file.

    Gists can have several files. This method searches for and downloads
    a single file from a gist.
    If the 'requested_file' is not informed, then it won't raise an error
    only if the gist have just a single file.

    :param gist_id: identifier of the gist to download
    :param requested_file: name of the Gist file to download
    :param destination_dir: destination directory after the download
    :param facade: instance of the object that actually perform the request
    """

    # Get the gist information
    response = facade.request_gist(gist_id)

    if response.ok:
        # Gist file found. Parse it into a 'model.Gist' class.
        gist_obj = model.Gist(get_json(response))
        list_names = [gistfile.filename for gistfile in gist_obj.files]

        if len(gist_obj.files) == 1 and not requested_file:
            # Download the only file in the gist
            gistfile = gist_obj.files[0]
            download(gistfile.raw_url, destination_dir,
                     gistfile.filename, gistfile.size)

            result = build_result(True, literals.DOWNLOAD_OK,
                                  gistfile.filename)
        else:
            # Gist have more than one file and filename not specified. Error
            if not requested_file:
                list_names = ", ".join(list_names)
                result = build_result(False, literals.DOWNLOAD_MORE_FILES,
                                      list_names)
            else:
                # Search for the Gist file
                gistfile = gist_obj.getFile(requested_file)
                if gistfile:

                    # Gist file found. Download it.
                    download(gistfile.raw_url, destination_dir,
                             gistfile.filename, gistfile.size)

                    result = build_result(True, literals.DOWNLOAD_OK,
                                          gistfile.filename)
                else:
                    # Requested file not found in Gist
                    list_of_names = ", ".join(list_names)
                    result = build_result(False, literals.FILE_NOT_FOUND,
                                          list_of_names)

    else:
        # Handle GitHub response error
        result = build_result(False, literals.DOWNLOAD_ERROR,
                              get_json(response)['message'])

    return result


def show(gist_id, requested_file, facade):
    """ Retrieve a single gist.

    If the 'requested_file' is None, then it will show the
    'metadata' of the Gist. This is: its description, urls, file names..

    If the 'requested_file' is informed, then it will show
    the content of the gist file.

    :param gist_id: identifier of the Gist to print
    :param requested_file: Gist File to show
    :param facade: instance of the object that actually performs the request
    """

    # get the gist information
    response = facade.request_gist(gist_id)

    if response.ok:
        # Gist found. Parse the json response into the 'model.Gist' class
        gist_obj = model.Gist(get_json(response))
        if not requested_file:
            # Fill the response with the metadata of the gist
            result = build_result(True, gist_obj)
        else:
            # We want to return the content of the file. Search for the content
            list_names = [gistfile.filename for gistfile in gist_obj.files]
            file_gist = gist_obj.getFile(requested_file)
            if file_gist:
                # Fill the response with the metadata of the gist
                result = build_result(True, file_gist)
            else:
                # File not found in Gist
                list_of_names = ", ".join(list_names)
                result = build_result(False, literals.FILE_NOT_FOUND,
                                      list_of_names)

    else:
        # GitHub response not ok. Parse the response
        result = build_result(False, literals.SHOW_ERROR,
                              get_json(response)['message'])

    return result


def post(public, upload_files, filepath, description, facade):
    """ Create a new Gist.

    Currently only support create Gist with single files. (Then you can
    'update' the gist and attach more files in it, but the creation only
    supports one file)

    You are able to specify if you want to create a public or private
    gist and set its description.

    :param public: whenever new Gist should be public or private
    :param upload_files: list with  input files to upload
    :param filepath: input parameter path
    :param description: brief description of the Gist
    :param facade: instance of the object that actually performs the request
    """

    # Prepare the Gist file object and set its description and 'public' value
    gist = model.Gist()
    if description:
        gist.description = description
    gist.public = public

    for upfile in upload_files:
        # Prepare the content reading the file
        gistFile = model.GistFile()
        gistFile.filename = upfile
        with open(os.path.join(filepath, upfile), 'r') as f:
            file_content = f.read()
            gistFile.content = file_content
        gist.addFile(gistFile)

    response = facade.create_gist(gist)
    # Parse the response
    if response.ok:
        result = build_result(True, model.Gist(get_json(response)))
    else:
        if get_json(response):
            result = build_result(False, get_json(response)['message'])
        else:
            result = build_result(False, literals.UNHANDLED_EXCEPTION)
    return result


def delete(gistid, facade):
    """ Just deletes a gist.

    :param gistid: identifier of the Gist to delete
    :param facade: instance of the object that actually performs the request
    """

    # First check if the gist exists
    response = facade.request_gist(gistid)

    if response.ok:

        # Gist Found. Ask for confirmation
        value_raw_input = (literals.DELETE_CONFIRMATION) % (gistid)
        value = raw_input(value_raw_input)
        accepted_values_for_yes = ["y", "yes", "ofcourse", "ye"]
        if value.lower() in accepted_values_for_yes:

            # Perform the deletion
            response = facade.delete_gist(gistid)
            if response.ok:
                result = build_result(True, literals.DELETE_OK, gistid)

            else:
                res_message = get_json(response)['message']
                result = build_result(False, literals.DELETE_NOK, res_message)
        else:
            # Aborted mission
            result = build_result(False, literals.DELETE_ABORTED)
    else:
        # Gist not retrieved.
        res_message = get_json(response)['message']
        result = build_result(False, literals.DELETE_NOK, res_message)

    return result


def update(gistid, description, filenames, filepath, new, remove, facade):
    """ Updates a gist.

    :param gistid: identifier of the Gist to update
    :param description: new description of the Gist. If 'None' it won't be
    updated
    :param filenames: list with names of the files to modify its contents
    :param filepath: input parameter path
    :param new: whenever the file is new or already exists
    :param remove: if the file should be deleted instead of modified
    :param facade: instance of the object that actually performs the request
    """

    # First get the result
    response = facade.request_gist(gistid)

    if response.ok:
        # Gist found.
        gist = model.Gist(get_json(response))
    else:
        result = build_result(False, literals.UPDATE_NOK,
                              get_json(response)['message'])
        return result

    if description:
        # Update the description of a Gist if requested
        gist.description = description

    if filenames:
        for filename in filenames:
            # File to update
            file_obj = gist.getFile(filename)
            if not file_obj:
                if remove:
                    return build_result(False, literals.UPDATE_RM_NF)
                if new:
                    # Upload a new file to gist
                    gistFile = model.GistFile()
                    gistFile.filename = filename
                    with open(os.path.join(filepath, filename), 'r') as f:
                        file_content = f.read()
                        gistFile.content = file_content
                    gist.addFile(gistFile)
                else:
                    # File not found and option --new it does not exist
                    return build_result(False, literals.UPDATE_NF)
            else:
                if new:
                    # File not found and option --new it does not exist
                    return build_result(False, literals.UPDATE_NEW_DUP)
                if remove:
                    # Remove a file
                    gist.setFile(filename, "null")
                else:
                    # Update the contents of the file
                    with open(os.path.join(filepath, filename), 'r') as f:
                        file_content = f.read()
                        file_obj.content = file_content
                    gist.setFile(filename, file_obj)

    # prepare the request
    response = facade.update_gist(gist)
    if response.ok:
        return build_result(True, gist)
    else:
        return build_result(False, literals.UPDATE_NOK,
                            get_json(response)['message'])

    return result


def authorize(facade):
    """ Configure the user and password of the GitHub user.

    :param facade: The Github interface
    """

    # check if there is already an authorization for the app
    response = facade.list_authorizations()
    if response.ok:
        for auth in get_json(response):
            authorization = model.Authorization(auth)
            if authorization.note == literals.APP_NAME:
                # write the token to the configuration file
                configurer = GistsConfigurer()
                configurer.setConfigUser(facade.username)
                configurer.setConfigToken(authorization.token)
                return build_result(True, authorization)
    else:
        return build_result(False, literals.AUTHORIZE_NOK,
                            get_json(response)['message'])

    # build the authorization request
    auth = model.Authorization()
    auth.note = literals.APP_NAME
    auth.note_url = literals.APP_URL
    auth.scopes = ["gist"]

    response = facade.authorize(auth)

    if response.ok:
        auth = model.Authorization(get_json(response))
        result = build_result(True, auth)

        # write the token to the configuration file
        configurer = GistsConfigurer()
        configurer.setConfigUser(facade.username)
        configurer.setConfigToken(auth.token)
    else:
        result = build_result(False, literals.AUTHORIZE_NOK,
                              get_json(response)['message'])

    return result


def fork(gist_id, facade):
    """ Forks a gist.

    :param gistid: identifier of the Gist to fork
    :param facade: instance of the object that actually performs the request
    """
    response = facade.fork_gist(gist_id)

    if response.ok:
        result = build_result(True, model.Gist(get_json(response)))
    else:
        if get_json(response):
            result = build_result(False, literals.FORK_ERROR, gist_id,
                                  get_json(response)['message'])
        else:
            result = build_result(False, literals.UNHANDLED_EXCEPTION)
    return result


def star(gist_id, facade):
    """ Stars a gist.

    :param gistid: identifier of the Gist to star
    :param facade: instance of the object that actually performs the request
    """
    response = facade.star_gist(gist_id)

    if response.ok:
        result = build_result(True, literals.STAR_OK, gist_id)

    else:
        res_message = get_json(response)['message']
        result = build_result(False, literals.STAR_NOK, res_message)

    return result


def unstar(gist_id, facade):
    """ Unstars a gist.

    :param gistid: identifier of the Gist to unstar
    :param facade: instance of the object that actually performs the request
    """
    response = facade.unstar_gist(gist_id)

    if response.ok:
        result = build_result(True, literals.UNSTAR_OK, gist_id)

    else:
        res_message = get_json(response)['message']
        result = build_result(False, literals.UNSTAR_NOK, res_message)

    return result
