def transform_structure(input_data):
  def parse_key(key):
      parts = key.split("::")
      value = parts[0]
      label = parts[1] if len(parts) > 1 else value
      return value, label

  def transform_node(key, value):
      node_value, node_label = parse_key(key)
      node = {"label": node_label, "value": node_value}
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
      return [{"label": input_data, "value": input_data}]

# Example input JSON structure
input_json = {
  "a::Label A": {
      "b::Label B": [
          "c::Label C",
          "d"
      ]
  }
}

# Transform the input JSON structure
output_structure = transform_structure(input_json)

# Print the transformed structure
import json
print(json.dumps(output_structure, indent=2))
