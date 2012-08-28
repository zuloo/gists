Gists
=====

CLI interface for managing GitHub gists

Install
-------

Two ways of installation:

* [Download](https://github.com/jdevesa/gists/zipball/master) the source code, extract it, and execute `python setup.py install`
* pip install gists (not yet!)

Configure
---------

First time you run 'gists', execute the command


    $ gists credentials -u your_github_user -s your_github_password


And the file ~/.gistsrc (which stores the 'gists' configuration) will be written
with your GitHub username and its password.

You can live without this config file using the '-u (--user)' argument every
time you perform an action, and '-s (--secret)' argument every time you perform an 
action that needs authentication (create, update, delete gists, and view private gists
as well).

Use it!
-------

### List of Gists ###

Return a list of gists. Basic usage is:

    $ gists list

That will return a list of Gists from the configured user in your (~/.gistsrc) file. 

More:

* __-u__ argument you specifies from which user you want to retrieve his/her gists.
* __--private__ argument retrieves the private gists of the user besides the public ones. (Needs authentication)
* __-s__ argument overrides the password from the (~/.gistsrc) file
