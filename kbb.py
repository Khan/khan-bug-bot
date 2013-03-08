import json
import sys

from flask import Flask
from flask import request
import requests

import secrets

app = Flask(__name__)

def print_pretty_json(obj):
    print json.dumps(obj, sort_keys=True, indent=4, 
                     separators=(", ", ": "))

def auth_headers():
    return {
        "Authorization": "token %s" %
            secrets.KHANBUGZ_GITHUB_OAUTH_TOKEN, 
    }

def change_issue_state(owner, repo, number, state):
    uri = "https://api.github.com/repos/%s/%s/issues/%s" % (owner, repo, number)
    print uri
    data = {
        "state": state
    }
    r = requests.patch(uri, headers=auth_headers(), data=json.dumps(data))
    print_pretty_json(r.json())

@app.route("/")
def hello():
  return "Hello, World!"

@app.route("/callback")
def callback():
  result = {
      u"message": "OK"
  }
  return json.dumps(result)

@app.route("/callback/issue_comment", methods=["GET", "POST"])
def callback():

  print json.dumps(request.json, sort_keys=True, indent=4, 
                   separators=(",", ": "))

  result = {
      u"message": "OK"
  }

  owner = request.json["repository"]["owner"]["login"]
  repo = request.json["repository"]["name"]
  number = request.json["issue"]["number"]

  if ("notabug" in request.json["comment"]["body"]):
      if ("open" in request.json["issue"]["state"]):
          change_issue_state(owner, repo, number, "closed")
  elif ("realbug" in request.json["comment"]["body"]):
      if ("closed" in request.json["issue"]["state"]):
          change_issue_state(owner, repo, number, "open")

  return json.dumps(result)

if __name__ == "__main__":
    app.debug = True
    app.run(host="::0", port=10277)
