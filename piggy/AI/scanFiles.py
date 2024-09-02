import os
import json

def get_json_files_in_scenario_p1_recursively(root_dir):
  """
  Recursively searches for JSON files located in the 'scenarioP1' subdirectory (or any subdirectory) of the specified root directory.

  Args:
    root_dir: The root directory to search.

  Returns:
    A list of JSON file paths.
  """

  json_files = []

  def search_dir(dir_path):
    for file in os.listdir(dir_path):
      file_path = os.path.join(dir_path, file)
      if os.path.isdir(file_path):
        search_dir(file_path)
      elif file.endswith('.json') and 'scenarioP1' in file_path:
        json_files.append(file_path)

  search_dir(root_dir)
  return json_files

# Example usage:
root_dir = "/path/to/your/root/directory"
json_files = get_json_files_in_scenario_p1_recursively(root_dir)
print(json_files)
