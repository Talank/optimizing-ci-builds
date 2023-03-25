#!/bin/bash
# bash /home/jhilke/researh/ut-se/optimizing-ci-builds/log-analysis/analysis/runtime_difference.sh "/home/jhilke/researh/ut-se/optimizing-ci-builds/log-analysis/runtime_comparision.csv" /home/jhilke/researh/ut-se/optimizing-ci-builds/log-analysis/analysis/compare_runtime.py 
# bash /home/jhilke/researh/ut-se/optimizing-ci-builds/log-analysis/analysis/runtime_difference.sh /home/jhilke/researh/ut-se/optimizing-ci-builds/log-analysis/analysis/runtime_rerun.csv /home/jhilke/researh/ut-se/optimizing-ci-builds/log-analysis/analysis/compare_runtime.py
# old
# bash /home/jhilke/researh/ut-se/optimizing-ci-builds/log-analysis/analysis/runtime_difference.sh /home/jhilke/researh/ut-se/optimizing-ci-builds/log-analysis/analysis/runtime_comparision.csv /home/jhilke/researh/ut-se/optimizing-ci-builds/log-analysis/analysis/compare_runtime.py
# Define the Python script to run
PYTHON_SCRIPT="$2"

# Read the CSV file and loop through each row
{
  read # discard the first line (header)
  # while IFS=',' read -r project job step runtime_fix1 runtime_wo_fix step_runtime_w_fix step_runtime_wo_fix commit_sha_fix commit_sha_wo_fix,branch_w_fix,branch_wo_fix; do

  # Read rerun_fixes.sh output
  while IFS=',' read -r project job step runtime_fix1 runtime_wo_fix step_runtime_w_fix step_runtime_wo_fix commit_sha_fix commit_sha_wo_fix branch_w_fix branch_wo_fix iteration; do

  # Read from runtime_comparision.csv with header
  # Project,Job,Step,runtime diff in job,runtime diff in step,Runtime with fix,Runtime wo fix,step-runtime w fix,step-runtime wo fix,commit sha with fix,commit sha wo fix,build log with fix,build log wo fix
  # while IFS=',' read -r project job step runtime_diff_job runtime_diff_step runtime_fix1 runtime_wo_fix step_runtime_w_fix step_runtime_wo_fix commit_sha_fix commit_sha_wo_fix build_log_w_fix build_log_wo_fix; do
    # Export the variables
    export commit_sha_fix="${commit_sha_fix}"
    export commit_sha_wo_fix="${commit_sha_wo_fix}"
    export job="${job}"
    export step="${step}"
    export project="${project}"
    export branch_w_fix="${branch_w_fix}"
    export branch_wo_fix="${branch_wo_fix}"

    echo "==== project: ${project}"
    echo "==== job: ${job}"
    echo "==== step: ${step}"
    echo "==== commit_sha_fix: ${commit_sha_fix}"
    echo "==== commit_sha_wo_fix: ${commit_sha_wo_fix}"
    echo "==== branch_w_fix: ${branch_w_fix}"
    echo "==== branch_wo_fix: ${branch_wo_fix}"


    python3 "${PYTHON_SCRIPT}" "${commit_sha_fix}" "${commit_sha_wo_fix}" "${job}" "${step}" "${project} ${branch_w_fix}" "${project} ${branch_wo_fix}"
    echo "+------------------------------------------+"
  done
} < "$1"