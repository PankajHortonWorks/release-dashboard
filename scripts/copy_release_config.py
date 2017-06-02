import urllib2
import json
import csv
from optparse import OptionParser
#from __future__ import print

parser = OptionParser(usage="usage: %prog [options] filename")

parser.add_option(
        "-i","--release_config_id",
        type="string",
        dest="rel_config_id",
        help="release config id which you want to copy"
        )

parser.add_option("-c","--copyto",
        type="string",
        dest="to_release",
        default="",
        help="release id  where you want to copy"
        )


(options, args) = parser.parse_args()


#dashboard_host = "dashboard.qe.hortonworks.com"
dashboard_host = "172.22.111.19"
dashboard_port = "5000"
base_url = "http://"+dashboard_host+":"+dashboard_port

def get(query) :
    req = urllib2.Request(query)
    req.add_header('Content-Type', 'application/json')
    resp = urllib2.urlopen(req)
    content = resp.read()
    json_res = json.loads(content)
    return json_res

def post(query,data):
    req = urllib2.Request(query)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))    
    return response

_rel_to=options.to_release
_rel_config_id=options.rel_config_id

release_config_query="%s/hwqe-dashboard-api/v1/releaseconfigs?id=%s" % (base_url,_rel_config_id)
json_content = get(release_config_query)

post_query="%s/hwqe-dashboard-api/v1/releaseconfigs" % (base_url)

rel_config_details={}

if (len(json_content['release_configs'])) > 0:
    print("%s found" % (_rel_config_id))
    rel_config = json_content['release_configs'][0]
    rel_config_details['config_id']=rel_config['config']['id']
    rel_config_details['release_id']= _rel_to
    rel_config_details['name'] = rel_config['name']
    rel_config_details['custom_attributes'] = rel_config['custom_attributes']
    print(rel_config_details)
    res = post(post_query,rel_config_details)
    print("Response Code %s" % (res.getcode()))
    
else:
	print("No data found")
	exit()

