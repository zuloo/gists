#!/usr/env/bin python
from utils import GithubFacade, Result, download, build_result
import literals
import gistobj


# def list_gists(username=None, password=None):
def list_gists(username, password, facade=GithubFacade()):
    """ Retrieve the list of gists. """

    response = facade.request_list_of_gists(username, password)

    # put into a table the gists
    if response.ok:
        list_gists = []
        for gist in response.json:
            list_gists.append(gistobj.Gist(gist))

        return build_result(True, list_gists)
    else:
        return build_result(False, literals.LISTS_ERROR,
                response.json['message'])


def get(gist_id, requested_file, destination_dir, facade=GithubFacade()):

    response = facade.request_gist(gist_id)
    result = Result()

    if response.ok:
        gist_obj = gistobj.Gist(response.json)
        list_names = [gistfile.filename for gistfile in gist_obj.files]
        if len(gist_obj.files) == 1 and not requested_file:
            gistfile = gist_obj.files[0]
            download(gistfile.raw_url, destination_dir,
                    gistfile.filename, gistfile.size)
            return build_result(True, literals.DOWNLOAD_OK, gistfile.filename)
        else:
            if not requested_file:
                list_names = ", ".join(list_names)
                return build_result(False, literals.DOWNLOAD_MORE_FILES,
                        list_names)
            else:
                gistfile = gist_obj.getFile(requested_file)
                if gistfile:
                    download(gistfile.raw_url, destination_dir,
                            gistfile.filename, gistfile.size)
                    build_result(True, literals.DOWNLOAD_OK, gistfile.filename)
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


def show(gist_id, requested_file, facade=GithubFacade()):
    """ Retrieve a single gist . """

    response = facade.request_gist(gist_id)
    result = Result()

    if response.ok:
        gist_obj = gistobj.Gist(response.json)
        list_names = [gistfile.filename for gistfile in gist_obj.files]
        if not requested_file:
            result.success = True
            result.data = gist_obj
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


def post(username, password, public, upload_file, description,
        facade=GithubFacade()):

    # prepare the content
    gistFile = gistobj.GistFile()
    gistFile.filename = upload_file
    with open(upload_file, 'r') as f:
        file_content = f.read()
        gistFile.content = file_content

    # prepare the gist file object
    gist = gistobj.Gist()
    if description:
        gist.description = description
    gist.public = public
    gist.addFile(gistFile)

    # parse the response
    print "Uploading gist....",
    response = facade.create_gist(gist, username, password)
    result = Result()
    if response.ok:
        print "Done!"
        gist = gistobj.Gist(response.json)
        result.success = True
        result.data = gistobj.Gist(response.json)
    else:
        print "Fail!"
        result.success = False
        if response.json:
            result.data = response.json['message']
        else:
            result.data = "Unhandled exception"
    return result


def delete(gistid, username, password, facade=GithubFacade()):

    response = facade.request_gist(gistid)
    result = Result()

    if response.ok:
        value_raw_input = (("Are you sure you want to delete gist %s [yN]: ")
            % (gistid))
        value = raw_input(value_raw_input)
        accepted_values_for_yes = ["y", "yes", "ofcourse", "ye"]
        if value.lower() in accepted_values_for_yes:

            # prepare the request
            response = facade.delete_gist(gistid, username, password)
            if response.ok:
                result.success = True
                result.data = "Gist %s deleted successfully" % (gistid)
            else:
                result.success = False
                result.data = ("Can not delete the gist."
                        " Github reason: '%s'""") % (response.json['message'])
        else:
            result.success = False
            result.data = "Delete aborted"
    else:
        result.success = False
        result.data = ("Can not delete the gist."
                        " Github reason: '%s'""") % (response.json['message'])

    return result


def update(gistid, username, password, description, filename,
        new, remove, facade=GithubFacade()):

    gist = facade.request_gist(gistid)

    # prepare the request
    response = facade.updateEntity(gist, username, password)
    print response.json
