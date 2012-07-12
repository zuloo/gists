#!/usr/bin/env python
from base64 import b64encode


def print_table(table_gists):
    """ Print table using the max_width of each column.

    Seen on stackoverflow: http://goo.gl/h9yla
    """

    # Reorganize data by columns
    cols = zip(*table_gists)

    # Compute column widths by taking maximum lenght of values per column
    col_widths = [max(len(value) for value in col) for col in cols]

    # Create a suitable format string
    format_string = '  |  '.join(['%%%ds' % width for width in col_widths])

    # Print each row using the computed format
    for i in range(len(table_gists)):
        row = table_gists[i]
        row_string = format_string % (tuple(row))
        if i == 0:
            # print header
            print row_string
            print "=" * len(row_string)
        else:
            print row_string


def encode_auth(username, password):
    """ Return the encoded user:password. """

    # Here because is needed in all commands, and it is a way to don't
    # import b64encode function everywhere.
    return b64encode(username + ":" + password)

