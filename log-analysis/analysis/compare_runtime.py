import requests
import datetime
import sys
import csv
import os

# read from command line
# commit_sha_w_fix = sys.argv[1]
# # commit_sha_w_fix = "053aa2cb70d2a939e6858d5629015a16c3401a90"
# commit_sha_wo_fix = sys.argv[2]
# # commit_sha_wo_fix = "cc80f4451dcc6852279792da858820acf246f440"
# job_name = sys.argv[3]
# # job_name = "Build and Test with java 8"
# step_name = sys.argv[4]
# step_name = "Build and Test Java 8"
base_api_url = 'https://api.github.com'
OWNER = 'optimizing-ci-builds'
# project = sys.argv[5]
# project = "soot"
headers = {'Authorization': ''}
# branch_w_fix = 'run-w-fix'
# branch_wo_fix = 'run-wo-fix'
csv_file = 'runtime_w_wo_fix.csv'
failed = ""

# Create cariables, I am running command ${commit_sha_fix} ${commit_sha_wo_fix} ${job} ${step} ${project} python compare_runtime.py Read appropriate variables from environment variables
commit_sha_w_fix = os.environ['commit_sha_fix']
commit_sha_wo_fix = os.environ['commit_sha_wo_fix']
job_name = os.environ['job']
step_name = os.environ['step']
project = os.environ['project']
branch_w_fix = os.environ['branch_w_fix']
branch_wo_fix = os.environ['branch_wo_fix']

# Trim spaces at the end and beginning of the strings above
commit_sha_w_fix = commit_sha_w_fix.strip()
commit_sha_wo_fix = commit_sha_wo_fix.strip()
job_name = job_name.strip()
step_name = step_name.strip()
project = project.strip()

print(f"commit_sha_w_fix: {commit_sha_w_fix}")
print(f"commit_sha_wo_fix: {commit_sha_wo_fix}")
print(f"job_name: {job_name}")
print(f"step_name: {step_name}")
print(f"project: {project}")

# Step 1: Get the workflow ID for branch with fix
workflow_url = f"{base_api_url}/repos/{OWNER}/{project}/actions/workflows?commit={commit_sha_w_fix}"
# print(f"workflow_url: {workflow_url}")
workflow_response = requests.get(workflow_url, headers=headers).json()
# print(workflow_response)
workflow_id = workflow_response['workflows'][0]['id']

# making an exception for fabric-sdk-java
if project == "fabric-sdk-java":
    for workflow in workflow_response['workflows']:
        if workflow['name'] == "Build":
            workflow_id = workflow['id']

# Step 2: Get the workflow run ID for branch with fix
workflow_run_url = f"{base_api_url}/repos/{OWNER}/{project}/actions/workflows/{workflow_id}/runs?status=completed&branch={branch_w_fix}"
workflow_run_response = requests.get(workflow_run_url, headers=headers).json()
workflow_run_id = workflow_run_response['workflow_runs'][0]['id']

# Step 3: Get the list of jobs for branch with fix
workflow_jobs_url = f"{base_api_url}/repos/{OWNER}/{project}/actions/runs/{workflow_run_id}/jobs"
workflow_jobs_response = requests.get(workflow_jobs_url, headers=headers).json()

# Step 4: Extract the relevant information for branch with fix
for job in workflow_jobs_response['jobs']:
    if job['head_sha'] == commit_sha_w_fix and job['name'] == job_name:
        build_log_w_fix=job['html_url']            
        job_runtime_start = datetime.datetime.strptime(job['started_at'][:-1], '%Y-%m-%dT%H:%M:%S')
        job_runtime_end = datetime.datetime.strptime(job['completed_at'][:-1], '%Y-%m-%dT%H:%M:%S')
        job_runtime_w_fix = (job_runtime_end - job_runtime_start).total_seconds()
        for step in job['steps']:
            if step['name'].lower() == step_name.lower():
                step_name = step['name']
                step_index = job['steps'].index(step)
                # started at and completed at of step
                started_at = datetime.datetime.strptime(job['steps'][step_index]['started_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
                completed_at = datetime.datetime.strptime(job['steps'][step_index]['completed_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
                if job['conclusion'] != "success":
                    failed = failed + "with_fix" 
                runtime_w_fix = (completed_at - started_at).total_seconds()
        
                # output the build log for the commit with fix
                print(f"Build log for commit with fix: {commit_sha_w_fix} is : {job['html_url']}")

# Step 5: Get the workflow ID for branch without fix
workflow_url = f"{base_api_url}/repos/{OWNER}/{project}/actions/workflows?branch={branch_wo_fix}"
workflow_response = requests.get(workflow_url, headers=headers).json()
workflow_id = workflow_response['workflows'][0]['id']

# making an exception for fabric-sdk-java
if project == "fabric-sdk-java":
    for workflow in workflow_response['workflows']:
        if workflow['name'] == "Build":
            workflow_id = workflow['id']

# Step 6: Get the workflow run ID for branch without fix
workflow_run_url = f"{base_api_url}/repos/{OWNER}/{project}/actions/workflows/{workflow_id}/runs?status=completed&branch={branch_wo_fix}"
workflow_run_response = requests.get(workflow_run_url, headers=headers).json()
workflow_run_id = workflow_run_response['workflow_runs'][0]['id']

# Step 7: Get the list of jobs for branch without fix
workflow_jobs_url = f"{base_api_url}/repos/{OWNER}/{project}/actions/runs/{workflow_run_id}/jobs"
workflow_jobs_response = requests.get(workflow_jobs_url, headers=headers).json()
print(workflow_jobs_response)

# Step 8: Extract the relevant information for branch without fix
for job in workflow_jobs_response['jobs']:
    if job['head_sha'] == commit_sha_wo_fix and job['name'] == job_name:
        job_runtime_start = datetime.datetime.strptime(job['started_at'][:-1], '%Y-%m-%dT%H:%M:%S')
        job_runtime_end = datetime.datetime.strptime(job['completed_at'][:-1], '%Y-%m-%dT%H:%M:%S')
        job_runtime_wo_fix = (job_runtime_end - job_runtime_start).total_seconds()
        build_log_wo_fix = job['html_url']
        workflow_name = job['workflow_name']
        for step in job['steps']:
            # print(step['name'] in lower case)
            # print(step['name'].lower())
            if step['name'].lower() == step_name.lower():
                step_name = step['name']
                step_index = job['steps'].index(step)
                # started at and completed at of step
                started_at = datetime.datetime.strptime(job['steps'][step_index]['started_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
                completed_at = datetime.datetime.strptime(job['steps'][step_index]['completed_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
                
                if job['conclusion'] != "success":
                    failed = failed + " without_fix"
                runtime_wo_fix = (completed_at - started_at).total_seconds()
        
                # output the build log for the commit without fix
                print(f"Build log for commit without fix: {commit_sha_wo_fix} is : {job['html_url']}")
                
    
# Step 9: Calculate the runtime difference
runtime_diff_job = job_runtime_wo_fix - runtime_w_fix
print(f"Runtime difference in job: {runtime_diff_job}")

runtime_diff_step = runtime_wo_fix - runtime_w_fix
print(f"Runtime difference in step: {runtime_diff_step}")

# print (workflow_jobs_response)
# enter the data into a csv file with headers Project,Job,Step,runtime diff in job, runtime diff in step,Runtime with fix,Runtime wo fix,step-runtime w fix,step-runtime wo fix,commit sha with fix,commit sha wo fix,build log with fix,build log wo fix
with open(csv_file, 'a') as f:
    writer = csv.writer(f)
    writer.writerow([project,workflow_name,job_name,step_name,failed,runtime_diff_job,runtime_diff_step,job_runtime_w_fix,job_runtime_wo_fix,runtime_w_fix,runtime_wo_fix,commit_sha_w_fix,commit_sha_wo_fix,build_log_w_fix,build_log_wo_fix])