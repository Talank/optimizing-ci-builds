import utils
import os
import time
import subprocess

def main():
    # with open("yamls.csv", "w") as text_file:
    #     print(f"repo,workflow_name,workflow_path,workflow_link", file=text_file)
    
    # GET THE PROJECTS
    os.chdir("..")
    repositories = utils.get_filtered_repos()
    os.chdir("job_analyzer")
    time1 = int(time.time())
    commit=subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
    for index, repository in enumerate(repositories):
        try:
            # PHASE-1: COLLECTION
            """FORKING THE PROJECT (VIA GITHUB API)"""
            """PARSING THE YAML FILE"""
            """CHANGING THE YAML FILE"""
            forked_owner: str = "optimizing-ci-builds"
            analyzer_owner: str = "UT-SE-Research"
            repo: str = repository["name"].split("/")[1]
            print(f"\nRunning tests on {forked_owner}/{repo}")
            default_branch: str = repository["default_branch"]

            try:
                sha: str = utils.retrieve_sha(owner=forked_owner, repo=repo, default_branch=default_branch)
            except ValueError as error:
                print(error)
                pass

            # utils.add_secret(owner=forked_owner, repo=repo)

            yml_files_path = repository["Github Actions"].split(";")
            yml_files_path = [i for i in yml_files_path if i]

            configured_yaml_files = []
            yaml_shas = []

            for file_path in yml_files_path:
                # with open("yamls.csv", "a") as text_file:
                #     print(f"{repo},{file_path},https://github.com/{forked_owner}/{repo}/blob/{default_branch}/{file_path}", file=text_file)
                try:
                    yaml_file, yaml_sha = utils.get_yaml_file("optimizing-ci-builds", repo, file_path)
                except ValueError as error:
                    print(error)
                    # continue
                    pass
                loaded_yaml = utils.load_yaml(yaml_file)
                # workflow_name = loaded_yaml["name"]
                # with open("yamls.csv", "a") as text_file:
                #     print(f"{repo},{workflow_name},{file_path},https://github.com/{forked_owner}/{repo}/blob/{default_branch}/{file_path}", file=text_file)
                job_with_matrix = utils.get_job_with_matrix(loaded_yaml)   
                default_python_version = utils.get_python_version(loaded_yaml)             
                branch_name=str(time1)+'-'+commit
                configured_yaml = utils.configure_yaml_file(yaml_file, repo, file_path, branch_name, job_with_matrix, default_python_version)
                # with open("Output.yml", "w") as text_file:
                #     print(f"{configured_yaml}", file=text_file)
                configured_yaml_files.append(configured_yaml)
                yaml_shas.append(yaml_sha)
            utils.retrieve_sha_ci_analyzes(analyzer_owner, repo, branch_name)
            commit_sha = utils.execute(forked_owner, repo, sha, default_branch, yml_files_path, configured_yaml_files, yaml_shas)
            # utils.check_runs(forked_owner, repo, commit_sha)

        except Exception as e:
            print(e)
            print("There was an error don't ask me what it is.")

if __name__ == "__main__":
    main()
