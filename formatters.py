#!/usr/bin/env python
import os
from clint.textui import colored


def format_show(result):

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
            stringfiles = " [" + ", ".join([gistfile.filename
                for gistfile in gist.files]) + "]"
            gists_string += colored.red(stringfiles) + "\n"
        gists_string += colored.cyan('-' * int(columns)) + "\n"
        return gists_string
    else:
        return __format_error(result.data)


def __format_error(data):
    return colored.red("Error: ") + data
