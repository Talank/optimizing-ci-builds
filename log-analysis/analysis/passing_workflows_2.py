import pandas as pd

# Read input.csv and yamls.csv into pandas dataframes
input_df = pd.read_csv('/home/jhilke/researh/ut-se/optimizing-ci-builds/log-analysis/analysis/input.csv')
yamls_df = pd.read_csv('/home/jhilke/researh/ut-se/optimizing-ci-builds/job_analyzer/yamls.csv')

# Initialize an empty dataframe to store the passing workflows
passing_workflows_df = pd.DataFrame(columns=yamls_df.columns)

# Loop through each row in input_df and check if the project and workflow match with any row in yamls_df
for index, row in input_df.iterrows():
    matching_row = yamls_df.loc[(yamls_df['repo'] == row['Project']) & (yamls_df['workflow_name'] == row['Workflow'])]
    
    # If a matching row is found, add it to the passing_workflows_df
    if not matching_row.empty:
        passing_workflows_df = passing_workflows_df.append(matching_row)
        
# Save the passing_workflows_df to a csv file
passing_workflows_df.to_csv('passing_workflows.csv', index=False)
