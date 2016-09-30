import urllib2
import json
import csv
from optparse import OptionParser
#from __future__ import print

parser = OptionParser(usage="usage: %prog [options] filename")
parser.add_option("-f","--file",
		type="string",
		dest="filename",
		default="result.csv",
		help="csvFile to write the result",metavar="File"
		)
parser.add_option(
		"-c","--component",
		type="string",
		dest="component",
		help="Component name for which information is needed",metavar="component"
		)
parser.add_option(
		"-d","--dump",
		dest="is_dump",
		action='store_true',
		default=False,
		help="dump the testcases in csv files"	
		)
(options, args) = parser.parse_args()

dashboard_host = "dashboard.qe.hortonworks.com"
#dashboard_host = "172.22.111.19"
dashboard_port = "5000"
base_url = "http://"+dashboard_host+":"+dashboard_port

def execute_api(query) :
        req = urllib2.Request(query)
        req.add_header('Content-Type', 'application/json')
        resp = urllib2.urlopen(req)
        content = resp.read()
        json_res = json.loads(content)
        return json_res


lcomponent=options.component
lfile=options.filename
isdump=options.is_dump
total_test_per_file=20000

component_query="%s/hwqe-dashboard-api/v1/components?name=%s" % (base_url,lcomponent)
json_content = execute_api(component_query)
component_id=""
if len(json_content["components"]) > 0:
	print("%s found" %(lcomponent))
	component_id=json_content["components"][0]["id"]
else:
	print("No components found")
	exit()

# Found component id get  the count of test-cases for the component
sql = "select count(*) as total from test_cases where component_id=%s" %(component_id)
count_query = "%s/hwqe-dashboard-api/v1/querydb?sql=%s" %(base_url,urllib2.quote(sql))
json_content = execute_api(count_query)
total_testcases = json_content["result"][0]["total"]

print("Total Tests for %s : %s " %(lcomponent,total_testcases))


if isdump :
	number_files = (total_testcases/total_test_per_file) + 1
	rowcount=1
	for cnt in range(0,number_files):
		start=rowcount + (cnt *total_test_per_file)
		end=total_test_per_file
		sql="select id,suite,name from test_cases where component_id=%s limit %s,%s" %(component_id,start,end)
		test_query = "%s/hwqe-dashboard-api/v1/querydb?sql=%s" %(base_url,urllib2.quote(sql))
		print("Executing %s"% (test_query))
		json_content = execute_api(test_query)
		test_arr = json_content["result"]
		tempfile ="%s_%s.csv"%(lfile,cnt)
		testdata = open(tempfile, 'w')
		csvwriter = csv.writer(testdata)
		count=0
		for test_row in test_arr:
      			if count == 0:
             			header = test_row.keys()
				csvwriter.writerow(header)
				count += 1

      			csvwriter.writerow(test_row.values())
		testdata.close()	


