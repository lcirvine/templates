import csv

results_file = 'file.csv'

# list of lists
column_headers = ['col 1', 'col 2', 'col 3']
all_data = [column_headers]
all_data.append(['row 1, col 1', 'row 1, col 2', 'row 1, col 3'])
with open(results_file, 'w', newline='') as f:
    writer = csv.writer(f)
    for r in all_data:
        writer.writerow(r)

# dict of lists
example_dict = {'a': [1, 2, 3], 'b': [4, 5, 6], 'c': [7, 8, 9]}
with open(results_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(example_dict.keys())
    writer.writerows(zip(*example_dict.values()))

