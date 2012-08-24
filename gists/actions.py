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

from utils import GithubFacade, download, build_result, GistsConfigurer
import literals
import gistobj


def list_gists(username, password, facade=GithubFacade()):
    """ Retrieve the list of gists for a concrete user. """

    response = facade.request_list_of_gists(username, password)

    if response.ok:
        # List of gists for the requested user found.
        list_gists = []
        for gist in response.json:
            list_gists.append(gistobj.Gist(gist))

        return build_result(True, list_gists)
    else:
        # GitHub response error. Parse the response
        return build_result(False, literals.LISTS_ERROR,
                response.json['message'])


def get(gist_id, requested_file, destination_dir, facade=GithubFacade()):
    """ Download a gist file.

    Gists can have several files. This method searches for and downloads
    a single file from a gist.
    If the 'requested_file' is not informed, then it won't raise an error
    only if the gist have just a single file.
    """

    # Get the gist information
    response = facade.request_gist(gist_id)

    if response.ok:
        # Gist file found. Parse it into a 'gistobj.Gist' class.
        gist_obj = gistobj.Gist(response.json)
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
                    result = build_result(False,
                            literals.FILE_NOT_FOUND, list_of_names)

    else:
        # Handle GitHub response error
        result = build_result(False, literals.DOWNLOAD_ERROR,
                response.json['message'])

    return result


def show(gist_id, requested_file, facade=GithubFacade()):
    """ Retrieve a single gist.

    If the 'requested_file' is None, then it will show the
    'metadata' of the Gist. This is: its description, urls, file names..

    If the 'requested_file' is informed, then it will show
    the content of the gist file.
    """

    # get the gist information
    response = facade.request_gist(gist_id)

    if response.ok:
        # Gist found. Parse the json response into the 'gistobj.Gist' class
        gist_obj = gistobj.Gist(response.json)
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
                result = build_result(False,
                        literals.FILE_NOT_FOUND, list_of_names)

    else:
        # GitHub response not ok. Parse the response
        result = build_result(False, literals.SHOW_ERROR,
                response.json['message'])

    return result


def post(username, password, public, upload_file, description,
        facade=GithubFacade()):
    """ Create a new Gist.

    Currently only support create Gist with single files. (Then you can
    'update' the gist and attach more files in it, but the creation only
    supports one file)

    You are able to specify if you want to create a public or private
    gist and set its description.
    """

    # Prepare the content reading the file
    gistFile = gistobj.GistFile()
    gistFile.filename = upload_file
    with open(upload_file, 'r') as f:
        file_content = f.read()
        gistFile.content = file_content

    # Prepare the Gist file object and set its description and 'public' value
    gist = gistobj.Gist()
    if description:
        gist.description = description
    gist.public = public
    gist.addFile(gistFile)

    print "Uploading gist....",
    response = facade.create_gist(gist, username, password)
    # Parse the response
    if response.ok:
        print "Done!"
        gist = gistobj.Gist(response.json)
        result = build_result(True, gistobj.Gist(response.json))
    else:
        print "Fail!"
        print response.status_code
        if response.json:
            result = build_result(False, response.json['message'])
        else:
            result = build_result(False, literals.UNHANDLED_EXCEPTION)
    return result


def delete(gistid, username, password, facade=GithubFacade()):
    """ Just deletes a gist. """

    # First check if the gist exists
    response = facade.request_gist(gistid)

    if response.ok:

        # Gist Found. Ask for confirmation
        value_raw_input = (literals.DELETE_CONFIRMATION) % (gistid)
        value = raw_input(value_raw_input)
        accepted_values_for_yes = ["y", "yes", "ofcourse", "ye"]
        if value.lower() in accepted_values_for_yes:

            # Perform the deletion
            response = facade.delete_gist(gistid, username, password)
            if response.ok:
                result = build_result(True, literals.DELETE_OK, gistid)

            else:
                res_message = response.json['message']
                result = build_result(False, literals.DELETE_NOK, res_message)
        else:
            # Aborted mission
            result = build_result(False, literals.DELETE_ABORTED)
    else:
        # Gist not retrieved.
        res_message = response.json['message']
        result = build_result(False, literals.DELETE_NOK, res_message)

    return result


def update(gistid, username, password, description, filename,
        filepath, new, remove, facade=GithubFacade()):
    """ Updates a gist. """

    # First get the result
    response = facade.request_gist(gistid)

    if response.ok:
        # Gist found.
        gist = gistobj.Gist(response.json)
    else:
        result = build_result(False, literals.UPDATE_NOK,
                response.json['message'])
        return result

    if description:
        # Update the description of a Gist if requested
        gist.description = description

    if filename:
        # File to update
        file_obj = gist.getFile(filename)
        if not file_obj:
            if remove:
                return build_result(False, literals.UPDATE_RM_NF)
            if new:
                # Upload a new file to gist
                gistFile = gistobj.GistFile()
                gistFile.filename = filename
                with open(filepath, 'r') as f:
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
                with open(filepath, 'r') as f:
                    file_content = f.read()
                    file_obj.content = file_content
                gist.setFile(filename, file_obj)

    # prepare the request
    response = facade.update_gist(gist, username, password)
    if response.ok:
        return build_result(True, gist)
    else:
        return build_result(False, literals.UPDATE_NOK,
                response.json['message'])

    return result


def configure(username, password):
    """ Configure the user and password of the GitHub user. """

    configurer = GistsConfigurer()
    configurer.setConfigUser(username)
    configurer.setConfigPassword(password)
    return
