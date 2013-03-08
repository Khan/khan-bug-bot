import json
import sys

import requests

import secrets

def gen_callback(route):
    return "http://azuresky.myazuresky.com:10277%s" % route

def print_pretty_json(obj):
    print json.dumps(obj, sort_keys=True, indent=4,
                     separators=(",", ": "))

def auth_headers():
    return {
        "Authorization": "token %s" %
            secrets.KHANBUGZ_GITHUB_OAUTH_TOKEN,
    }

def get_hooks(owner, repo):
    uri = "https://api.github.com/repos/%s/%s/hooks" % (owner, repo)
    r = requests.get(uri, headers=auth_headers())
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
    r = requests.post(uri, headers=auth_headers(), data=json.dumps(data))
    print_pretty_json(r.json())

if __name__ == "__main__":
    #add_hook("cbhl", "khan-bug-bot", "issue_comment")
    add_hook("Khan", "khan-exercises", "issue_comment")

    print "List of hooks:"
    get_hooks("Khan", "khan-exercises")

