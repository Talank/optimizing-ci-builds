# Example usage: python3 process_runtimes.py test.json yaml_path github_link sha ci-runtime.csv

from collections import OrderedDict
from datetime import datetime
import csv
import json
import sys
import time

logs=sys.argv[1].split(",")
yaml_path=sys.argv[2]
github_link=sys.argv[3]
sha=sys.argv[4]
runtimecsv=sys.argv[5]

csvdata=list()

def escape(s):
    return s.replace(',', ';')

# yaml_file_path,github_link,sha,jobname,runid,step_index_in_yaml,stepname,stepnum,runtime,
for log in logs:
    with open(log) as f:
        allData = json.load(f, object_pairs_hook=OrderedDict)
        jobs=allData['jobs']

        for job in jobs:
            jobinfo = list()
            jobinfo.append(escape(yaml_path))
            jobinfo.append(escape(github_link))
            jobinfo.append(escape(sha))
            jobinfo.append(escape(job['name']))
            jobinfo.append(job['run_id'])
            for step in job['steps']:
                stepinfo=jobinfo.copy()
                stepinfo.append(escape(step['name']))
                stepinfo.append(step['number'])
                starttime=datetime.strptime(step['started_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
                endtime=datetime.strptime(step['completed_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
                stepinfo.append(endtime-starttime)
                csvdata.append(stepinfo)

with open(runtimecsv, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    for i in csvdata:
        csvwriter.writerow(i)
