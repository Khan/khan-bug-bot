import json
import sys
import requests

try:
  import secrets
except ImportError as e:
  sys.stderr.write("ERROR: %s\n" % e)
  sys.exit("Do you have a secrets.py?")

a = requests.auth.HTTPBasicAuth(secrets.KHANBUGZ_GITHUB_USER,
                                secrets.KHANBUGZ_GITHUB_PASS)

p = {
  'note': 'khan-bug-bot',
  'note_url': 'https://github.com/cbhl/khan-bug-bot',
  'client_id': secrets.KHANBUGZ_GITHUB_CLIENT_ID,
  'client_secret': secrets.KHANBUGZ_GITHUB_CLIENT_SECRET,
}

r = requests.post('https://api.github.com/authorizations', auth=a,
                  data=json.dumps(p))

print r.json()
print "Here's your OAuth Token:"
print
print "KHANBUGZ_GITHUB_OAUTH_TOKEN = \"%s\"" % (r.json()['token'])
print
print "Don't forget to add it to secrets.py!"
