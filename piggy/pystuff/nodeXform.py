def transform_structure(input_data, parent_key=None):
  def transform_node(key, value):
      node = {"label": key, "value": key}
      if isinstance(value, dict):
          node["children"] = [transform_node(k, v) for k, v in value.items()]
      elif isinstance(value, list):
          node["children"] = [transform_node(v, None) if isinstance(v, str) else transform_node(k, v) for k, v in enumerate(value)]
      return node

  if isinstance(input_data, dict):
      return [transform_node(k, v) for k, v in input_data.items()]
  elif isinstance(input_data, list):
      return [transform_node(v, None) if isinstance(v, str) else transform_node(k, v) for k, v in enumerate(input_data)]
  else:
      return [{"label": parent_key, "value": input_data}]

# Example input JSON structure
input_json = {
  "a": {
      "b": [
          "b1",
          {"b2": ["c1", "c2", "c3"]},
          "b3"
      ]
  }
}

# Transform the input JSON structure
output_structure = transform_structure(input_json)

# Print the transformed structure
import json
print(json.dumps(output_structure, indent=2))
