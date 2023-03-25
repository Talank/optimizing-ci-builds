import csv
import datetime

with open('1678940360-bbc60b2.csv', 'r') as input_file, open('output.csv', 'w', newline='') as output_file:
    reader = csv.DictReader(input_file)
    writer = csv.writer(output_file)

    # Write the headers to the output file
    writer.writerow(['Project', 'Sha', 'Workflow', 'Job', 'Avg Runtime Diff', 'Result_with_instrumentation', 'Result_without_instrumentation', 'Runtime_with_instrumentation', 'Runtime_without_instrumentation', 'path_to_pass_fail_log_with_instrumentation', 'path_to_pass_fail_log_without_instrumentation', 'path_to_inotify_log', 'category'])

    # Loop through each row in the input file
    for row in reader:
        try:
            # Parse the time columns into datetime objects
            time1 = datetime.datetime.strptime(row['Runtime_with_instrumentation'], '%H:%M:%S')
            time2 = datetime.datetime.strptime(row['Runtime_without_instrumentation'], '%H:%M:%S')

            # Calculate the difference between the times and convert to seconds
            diff_seconds = abs((time2 - time1).total_seconds())

            # Calculate the average difference between the times
            avg_diff = diff_seconds / 2

            # Write the row to the output file
            writer.writerow([row['Project'], row['Sha'], row['Workflow'], row['Job'], '{:.2f}'.format(avg_diff), row['Result_with_instrumentation'], row['Result_without_instrumentation'], row['Runtime_with_instrumentation'], row['Runtime_without_instrumentation'], row['path_to_pass_fail_log_with_instrumentation'], row['path_to_pass_fail_log_without_instrumentation'], row['path_to_inotify_log'], row['category']])
        except ValueError:
            pass
