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

def test_hook(owner, repo, hook_id):
    uri = "https://api.github.com/repos/%s/%s/hooks/%s/test" % (owner, repo, hook_id)
    r = requests.get(uri, headers=auth_headers())
    print_pretty_json(r.json())

if __name__ == "__main__":
    owner = "cbhl"
    repo = "khan-bug-bot"
    hook_id = 767660
    test_hook(owner, repo, hook_id)

