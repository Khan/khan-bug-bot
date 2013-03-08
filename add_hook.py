import json
import getpass
import sys

import requests

def gen_callback(route):
    return "http://azuresky.myazuresky.com:10277%s" % route

def print_pretty_json(obj):
    print json.dumps(obj, sort_keys=True, indent=4,
                     separators=(",", ": "))

def auth_method():
    print "Username:",
    user = raw_input()
    password = getpass.getpass()
    return requests.auth.HTTPBasicAuth(user, password)

def get_hooks(owner, repo):
    uri = "https://api.github.com/repos/%s/%s/hooks" % (owner, repo)
    r = requests.get(uri, auth=auth_method())
    print_pretty_json(r.json())

def add_hook(owner, repo, event):
    uri = "https://api.github.com/repos/%s/%s/hooks" % (owner, repo)
    data = {
        "name": "web",
        "config": {
            "url": gen_callback("/callback/%s" % event),
            "content_type": "json",
        },
        "events": [event],
    }
    r = requests.post(uri, auth=auth_method(), data=json.dumps(data))
    print_pretty_json(r.json())

if __name__ == "__main__":
    add_hook("Khan", "khan-exercises", "issue_comment")

    #print "List of hooks:"
    #get_hooks("Khan", "khan-exercises")

