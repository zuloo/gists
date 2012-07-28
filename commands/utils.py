#!/usr/bin/env python
from base64 import b64encode
from clint.textui import colored


class Result(object):
    """ Result class.

    To improve the mocking of tests, I created a 'result'
    class, always returned by the 'main()' method of the
    main module.
    """
    def __init__(self):
        self.result_code = None
        self.data = colored.blue('Result: ')  # Data to print to specify
                                      # the result explanation


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
