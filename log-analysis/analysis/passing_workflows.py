import pandas as pd

# Read input.csv and yamls.csv into pandas dataframes
input_df = pd.read_csv('/home/jhilke/researh/ut-se/optimizing-ci-builds/log-analysis/analysis/input.csv')
yamls_df = pd.read_csv('/home/jhilke/researh/ut-se/optimizing-ci-builds/job_analyzer/yamls.csv')

# Extract the unique workflow names from input_df
workflows = input_df['Workflow'].unique()

# Filter yamls_df to include only the rows with workflow names that are in workflows
passing_workflows_df = yamls_df[yamls_df['workflow_name'].isin(workflows)]

# Write passing_workflows_df to a new CSV file
passing_workflows_df.to_csv('passing_workflows.csv', index=False)
