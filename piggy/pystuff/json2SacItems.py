import streamlit as st
import streamlit_antd_components as sac

# Sample JSON structure
json_structure = {
  "root": {
      "a": ["a1", {"a2": ["c1", "c2", "c3"]}]
  }
}

# Function to convert JSON to TreeItem format
def json_to_tree_items(data, parent_key=''):
  tree_items = []
  if isinstance(data, dict):
      for key, value in data.items():
          children = json_to_tree_items(value, key)
          tree_items.append(sac.TreeItem(label=key, children=children))
  elif isinstance(data, list):
      for item in data:
          if isinstance(item, dict):
              tree_items.extend(json_to_tree_items(item, parent_key))
          else:
              tree_items.append(sac.TreeItem(label=item))
  elif isinstance(data, str):
      tree_items.append(sac.TreeItem(label=data))
  return tree_items

# Convert JSON structure to TreeItem format
tree_items = json_to_tree_items(json_structure)

# Streamlit app
def main():
  st.title("JSON to Ant Tree Example")

  # Display the Ant Tree
  sac.tree(
      items=tree_items,
      label='Example Tree',
      index=0,
      align='center',
      size='md',
      icon='table',
      open_all=True,
      checkbox=True
  )

if __name__ == "__main__":
  main()
