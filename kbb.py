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
    #print uri
    data = {
        "state": state
    }
    r = requests.patch(uri, headers=auth_headers(), data=json.dumps(data))
    print_pretty_json(r.json())

def create_comment(owner, repo, number, body):
    uri = "https://api.github.com/repos/%s/%s/issues/%s/comments" % (owner, repo, number)
    #print uri
    data = {
        "body": body
    }
    r = requests.post(uri, headers=auth_headers(), data=json.dumps(data))
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
  #pretty_print_json(request.json)

  result = {
      u"message": "OK"
  }

  owner = request.json["repository"]["owner"]["login"]
  repo = request.json["repository"]["name"]
  number = request.json["issue"]["number"]
  
  print "%s/%s: #%s" % (owner, repo, number)

  comment_body = request.json["comment"]["body"].lower()
  reverse_comment_body = comment_body[::-1]

  if "fixedit" in comment_body or "fixedit" in reverse_comment_body:
      print "fixedit"
      create_comment(owner, repo, number,
          """
We think the problem you reported is fixed.

If you're still having trouble, please let us know.

KhanBugz - Your Friendly Khan Academy Problem Robot""")
      change_issue_state(owner, repo, number, "closed")
  elif "dupeof" in comment_body or "dupeof" in reverse_comment_body:
      print "dupeof"
      create_comment(owner, repo, number,
          """
Thanks for reporting a problem on Khan Academy. We think you have a problem that is similar to one that someone else reported, and we ask that you look at their report to keep track of updates to this problem.

Please continue to report problems that you experience on the site, as we use the number of reports to prioritize which exercises to investigate first. Thanks!

KhanBugz - Your Friendly Khan Academy Problem Robot""")
      change_issue_state(owner, repo, number, "closed")
  elif "notabug" in comment_body or "notabug" in reverse_comment_body:
      print "notabug"
      if "open" in request.json["issue"]["state"];
          change_issue_state(owner, repo, number, "closed")
  elif "realbug" in comment_body or "realbug" in reverse_comment_body:
      print "realbug"
      if "closed" in request.json["issue"]["state"];
          change_issue_state(owner, repo, number, "open")

  return json.dumps(result)

if __name__ == "__main__":
    app.run(host="::0", port=10277)
