Gists
=====

CLI interface for managing GitHub gists

Configure
---------

First time you run 'gists', execute the command

``
$ gists credentials -u your_github_user -s your_github_password
``

And the file ~/.gistsrc (which stores the 'gists' configuration) will be written.
You can live without this config file using the '-u (--user)' argument every
time you perform an action, and '-s (--secret)' argument every time you perform an 
action that needs authentication.


Disclaimer
----------

This package is currently in 'Beta' relase. This means that even is quite stable and it is
not going to break your gists, some exceptions may be not handled in the proper way and some
functionality is not completely tested.

Fork it
-------

Fork it, download, follow it or whatever here: (http://github.com/jdevesa/gists)

