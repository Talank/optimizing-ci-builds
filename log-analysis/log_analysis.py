import json
import sys
import os
import glob
from collections import defaultdict

log_directory=sys.argv[1]
proj_list = os.listdir(log_directory)
failure_type=[]
first_failure_name_count={}
first_failure_name_projName=defaultdict(list)

all_failure_name_count={}
all_failure_name_projName=defaultdict(list)
#print(proj_list)
for proj in proj_list:
    for file in glob.glob(log_directory+proj+"/*.json"):
        json_file=file
        #print('json_file='+json_file)
        with open(json_file) as user_file:
            file_contents = user_file.read()
            parsed_json = json.loads(file_contents)
            for i in range(len(parsed_json)-1): # This one is for each job
                jobs=parsed_json['jobs']
                #print('job len='+str(len(job_len)))
                for k in range(len(jobs)):
                    build_name=jobs[k]['name']
                    build_conclusion=jobs[k]['conclusion']
                    #print(build_name)
                    if build_conclusion=="failure" :
                        #print('proj_name='+proj)
                        steps_content=jobs[k]['steps']
                        #print('len='+str(len(steps_content)))

                        for j in range(len(steps_content)):
                            if (steps_content[j]['conclusion'] == "failure"):
                                if not steps_content[j]['name'] in first_failure_name_count: 
                                    first_failure_name_count[steps_content[j]['name']]=1
                                    first_failure_name_projName[steps_content[j]['name']].append(proj)
                                else:
                                    count=first_failure_name_count[steps_content[j]['name']]
                                    first_failure_name_count[ steps_content[j]['name'] ] = count + 1
                                    first_failure_name_projName[steps_content[j]['name']].append(proj)
                                break
                        
                        for l in range(len(steps_content)):
                            if (steps_content[l]['conclusion'] == "failure"):
                                if not steps_content[l]['name'] in all_failure_name_count: 
                                    all_failure_name_count[steps_content[l]['name']]=1
                                    all_failure_name_projName[steps_content[l]['name']].append(proj)
                                else:
                                    count=all_failure_name_count[steps_content[l]['name']]
                                    all_failure_name_count[ steps_content[l]['name'] ] = count + 1
                                    all_failure_name_projName[steps_content[l]['name']].append(proj)


print('======Result for first fialure in each job=======')
for x, y in first_failure_name_count.items():
  print(x,":",y) 
print("************Project name and each failure step*********")
for x, y in first_failure_name_projName.items():
  print(x,":",y) 
#print(first_failure_name_projName)
                #elif build_conclusion=="skipped" :


print()
print()
print()
print('=========Result for all fialures in each job=========')
print()
for x, y in all_failure_name_count.items():
  print(x,":",y) 
print("************Project name and each failure step*********")
for x, y in all_failure_name_projName.items():
  print(x,":",y) 

#print(all_failure_name_count)
#print(all_failure_name_projName)