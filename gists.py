#!/usr/bin/env python

import requests
import json

USERNAME = "jdevesa"
PASSWORD = "jdg1982jdg"

def list_gists(username=USERNAME, password=PASSWORD):
    url = "https://api.github.com/users/%s/gists" % (username)
    gists = requests.get(url)
    if gists.ok:
        print "Id\tNo Files\tDescription\t\t"
        print "================================================================================"
        for gist in gists.json:
            print "%s\t\t%d\t%s" % (gist['id'], len(gist['files']), gist['description'])

if __name__ == "__main__":
    list_gists()
    
