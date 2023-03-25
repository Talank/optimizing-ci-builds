# Project	Job	Step	runtime diff in job	runtime diff in step	Runtime with fix	Runtime wo fix	step-runtime w fix	step-runtime wo fix	commit sha with fix	commit sha wo fix	build log with fix	build log wo fix

#!/bin/bash
# bash rerun_fixes.sh /home/jhilke/researh/ut-se/optimizing-ci-builds/log-analysis/analysis/temp.csv 1 /home/jhilke/researh/ut-se/optimizing-ci-builds/log-analysis/data/projects /home/jhilke/researh/ut-se/optimizing-ci-builds/log-analysis/analysis/runtime_rerun.csv
csv_file="$1"
iteration="$2"
main_dir="$3"
output_csv="$4"
IFS=$'\n'
cd $main_dir

echo "Project,Job,Step,Runtime_with_fix,Runtime_wo_fix,step-runtime_w_fix,step-runtime_wo_fix,commit_sha_with_fix,commit_sha_wo_fix,branch_w_fix,branch_wo_fix,iteration" > $output_csv

for i in $(seq 1 $iteration); do
    timestampt=$(date +%s%N | cut -b1-13)
    new_branch="fixes-${timestampt}"
    new_branch_wo_fix="wo-fixes-${timestampt}"
    echo "==== iteration: ${i}"
    for row in $(tail +2 $csv_file); do
        project_name="$(echo $row | cut -d',' -f1)"
        project_dir="${main_dir}/${project_name}"
        commit_sha_fix="$(echo $row | cut -d',' -f10)"
        commit_sha_wo_fix="$(echo $row | cut -d',' -f11)"
        job_name="$(echo $row | cut -d',' -f2)"
        step_name="$(echo $row | cut -d',' -f3)"

        echo "${project_name},${job_name},${step_name},,,,,${commit_sha_fix},${commit_sha_wo_fix},${new_branch},${new_branch_wo_fix},${i}" >> $output_csv
        echo "======== project: ${project_name}"

        cd $project_dir
        git fetch origin
        git checkout $commit_sha_fix
        git checkout -b $new_branch
        git push origin $new_branch

        git checkout $commit_sha_wo_fix
        git checkout -b $new_branch_wo_fix
        git push origin $new_branch_wo_fix
        
        cd -
    done

done
    