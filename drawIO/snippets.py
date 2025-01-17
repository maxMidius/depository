
import panel as pn

pn.extension()

#------- SNIP 1  (did not work) -----------
# Create a FileSelector widget
file_selector = pn.widgets.FileSelector('~')

# Read the selected file's contents (assuming it's a text file)
@pn.depends(file_selector.param.value)
def read_file_contents(file_value):
    if file_value:
        try:
            with open(file_value[0], 'r') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            return "File not found."
    return ""

# Display the file contents
file_contents = pn.pane.Str(read_file_contents, height=300)
app = pn.Column(file_selector, file_contents)

app.servable()

#-----  COP SNIP 2   UTF 8 converter ---------

import csv

# Input and output file names
input_file = 'spotify.csv'
output_file = 'output.csv'

# Read the original CSV file (assuming it's encoded in utf-8-sig)
with open(input_file, 'r', newline='', encoding='utf-8-sig') as infile:
    reader = csv.reader(infile)
    rows = list(reader)  # Read all rows

# Process the data (you can modify this part as needed)
# For example, let's add a prefix to each row
processed_rows = [['Prefix_' + row[0]] + row[1:] for row in rows]

# Write the processed data to a new CSV file with UTF-8 encoding
with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(processed_rows)

print(f"Converted and saved to {output_file}")

#------------- GEM SNIP2  ---------------------------
with open('spotify.csv', 'r', encoding='utf-8') as infile, 
     open('output.csv', 'w', encoding='utf-8') as outfile:
  # Read all lines from the input file
  rows = infile.readlines()

  # Write the lines to the output file
  outfile.writelines(rows)

print("Conversion complete! Check 'output.csv' for UTF-8 encoded data.")

#------------------ YAML to CSV ------------------
import csv
import yaml

# Read the YAML file
with open('input.yaml', 'r') as yaml_file:
    data = yaml.safe_load(yaml_file)

# Write the data to a CSV file
with open('output.csv', 'w', newline='') as csv_file:
    fieldnames = list(data[0].keys())
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

#------------------ YAML to CSV ------------------
import csv
import yaml

with open('input.yaml', 'r') as yaml_file:
    data = yaml.safe_load(yaml_file)

with open('output.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(data.keys())
    for item in data:
        writer.writerow(item.values())
