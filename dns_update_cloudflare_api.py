# IMPORT MODULES
import json
import requests
from json import load
from urllib2 import urlopen

# VARIABLES
# Load in private creds. - not in github.
conf_file = "/Users/srance/Devops/public-ip/config.json"
with open(conf_file) as c:
  data = json.load(c)
  zoneid = data['zoneid']
  api_key = data['api_key']
  api_email = data['api_email']
  apiurl = "https://api.cloudflare.com/client/v4/zones/"
  ip_file = "/Users/srance/Devops/public-ip/public-ip.json"
headers = {}
headers['Content-Type'] = "application/json"
headers['X-Auth-Key'] = api_key
headers['X-Auth-Email'] = api_email

# FUNCTIONS
def get_live_ip():
  global liveip
  liveip = load(urlopen('http://jsonip.com'))['ip']
  return liveip

def get_current_ip():
  global currentip
  with open(ip_file) as f:
      data = json.load(f)
      currentip = data['ip']
      return currentip

def update_current_ip():
  ip = {}
  ip['ip'] = liveip
  with open(ip_file, 'w') as outfile:
    json.dump(ip, outfile)

def updateapi():
  print apiurl + "/dns_records?type=A"
  r = requests.get(apiurl + zoneid + "/dns_records?type=A&content="+currentip, headers=headers)
  json_data = json.loads(r.text)
  for result in json_data['result']:
    dns_id = result['id']
    print(dns_id)
    record_update = {}
    record_update['type'] = result['type']
    record_update['name'] = result['name']
    record_update['content'] = liveip
    record_update = json.dumps(record_update)
    s = requests.post(apiurl + zoneid + "/dns_records/" + dns_id, headers=headers, data=record_update)
    response = json.loads(s.text)
    #try:
    #  if response['success'] != true:
    #      raise ValueError('Record update failed')
    #  Print "Record updated successfully for: " + result['name']
    #except (ValueError, IndexError):
    #  exit('Record update failed for: ' + result['name'])

# MAIN SCRIPT
get_live_ip()
get_current_ip()
if currentip != liveip :
  print "IP's don't match need to update"
  #updateapi()
  update_current_ip()
else:
  print "IP's match, exiting"
