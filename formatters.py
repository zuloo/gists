#!/usr/bin/env python
import os
from clint.textui import colored


def format_file(result):

    if result.success:
        file_gist = result.data
        """ Pretty prints the gist. """
        rows, columns = os.popen('stty size', 'r').read().split()
        gist_string = ""
        gist_string += colored.cyan('-' * int(columns)) + "\n"
        gist_string += colored.red("[" + file_gist.filename + "]\n")
        gist_string += colored.cyan('-' * int(columns)) + "\n"
        gist_string += (colored.green("Language:") + " " +
                colored.red(file_gist.language) + "\n")
        gist_string += (colored.green("Size:") + " " +
             colored.red(file_gist.size) + "\n")
        gist_string += (colored.green("Raw Url:") + " " +
                colored.red(file_gist.raw_url + "\n"))
        gist_string += (colored.green("Content:\n\n")
                + file_gist.content + "\n\n")
        gist_string += colored.cyan('-' * int(columns)) + "\n"
        return gist_string
    else:
        return __format_error(result.data)


def format_get(result):

    if result.success:
        return "File downloaded!"
    else:
        return __format_error(result.data)


def format_list(result):
    if result.success is True:
        list_of_gists = result.data
        rows, columns = os.popen('stty size', 'r').read().split()
        gists_string = colored.cyan('-' * int(columns)) + "\n"
        gists_string += "List of gists\n"
        gists_string += colored.cyan('-' * int(columns)) + "\n"
        for gist in list_of_gists:
            gists_string += colored.green(gist.identifier + ": ")
            description = "(no desc)"
            if gist.description and gist.description != "":
                description = gist.description
            gists_string += description
            gist_names = [gistfile.filename for
                    gistfile in gist.files]
            stringfiles = " [" + ", ".join(gist_names) + "]"
            gists_string += colored.red(stringfiles)
            if not gist.public:
                gists_string += " (Private) "
            gists_string += '\n'

        gists_string += colored.cyan('-' * int(columns)) + "\n"
        return gists_string
    else:
        return __format_error(result.data)


def format_gist(result):
    if result.success:
        gist = result.data
        rows, columns = os.popen('stty size', 'r').read().split()
        gists_string = colored.cyan('-' * int(columns)) + "\n"
        gists_string += colored.red("[" + gist.identifier + "]") + '\n'
        gists_string += colored.cyan('-' * int(columns)) + "\n"
        gists_string += colored.green('Description:\t')
        gists_string += gist.description + '\n'
        gists_string += colored.green('Url:\t\t')
        gists_string += gist.url + '\n'
        gists_string += colored.green('Html Url:\t')
        gists_string += gist.html_url + '\n'
        gists_string += colored.green('Private:\t')
        gists_string += str(not gist.public) + '\n'

        gists_string += colored.cyan('-' * int(columns)) + "\n"
        return gists_string
    else:
        return __format_error(result.data)


def __format_error(data):
    return colored.red("Error: ") + data
