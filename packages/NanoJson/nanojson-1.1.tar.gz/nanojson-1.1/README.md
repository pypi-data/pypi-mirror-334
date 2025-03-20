
# NanoJson library provided by Mohammed Ghanam.

![PyPI - Version](https://img.shields.io/pypi/v/NanoJson?color=blue&label=version)  
![Python](https://img.shields.io/badge/python-3.6%2B-blue)  
![License](https://img.shields.io/badge/license-MIT-green)  
![Status](https://img.shields.io/badge/status-active-success)  

**NanoJson** is a simple, efficient, and feature-rich Python library for working with JSON files. It provides methods for reading, writing, updating, and manipulating JSON data. Whether you're working with simple JSON files or deeply nested structures, NanoJson makes it easy to work with your data.

## Installation

You can install **NanoJson** from PyPi using `pip`:

```bash
pip install NanoJson==1.1

Usage

Importing the Library

To use NanoJson, simply import it like this:

import NanoJson

Creating a NanoJson Object

To work with a JSON file, create an instance of NanoJson by providing the file path and optional indentation level:

json_handler = NanoJson('data.json', indent=4)

Methods

Read JSON Data

You can read the data from the JSON file either as a dictionary or in a pretty-printed format:

```
data = json_handler.read_json()  # Returns the data as a dictionary
pretty_data = json_handler.read_json(pretty=True)  # Pretty-printed JSON string
```

Write JSON Data

To write data to the JSON file:

```
json_handler.write_json({"name": "John", "age": 30})
```

Update JSON Data

You can update an existing key or add a new key to the JSON file:

```
json_handler.update_json("city", "New York")
```

Delete a Key

To delete a key from the JSON file:

```
json_handler.delete_key("age")
```

Search for a Key

Search for a key and get its value:

```
value = json_handler.search_key("name")
```

Deep Search for Nested Keys

Perform a deep search for a key even if it's nested inside other objects or lists:

```
value = json_handler.deep_search("address.street")
```

Append to a List

You can append an element to an existing list inside the JSON file:

```
json_handler.append_to_list("hobbies", "reading")
```

Remove from a List

To remove an element from a list:

```
json_handler.remove_from_list("hobbies", "reading")
```

Merge JSON Data

Merge new data into the existing JSON file:

```
json_handler.merge_json({"country": "USA", "state": "California"})
```

Clear JSON Data

To clear all data in the JSON file:

```
json_handler.clear_json()
```

Backup and Restore

You can back up your JSON file and restore it from a backup:

```
json_handler.backup_json("backup.json")
json_handler.restore_backup("backup.json")
```

Example

Here’s a complete example of how to use NanoJson:

```
import NanoJson

# Initialize NanoJson
json_handler = NanoJson('data.json')

# Write data
json_handler.write_json({'name': 'John', 'age': 25})

# Update data
json_handler.update_json('city', 'New York')

# Search for a value
print(json_handler.search_key('name'))

# Append to a list
json_handler.append_to_list('hobbies', 'reading')

# Remove from a list
json_handler.remove_from_list('hobbies', 'reading')

# Deep search
print(json_handler.deep_search('city'))

# Merge new data
json_handler.merge_json({'country': 'USA'})

# Rename a key
json_handler.rename_key('city', 'location')

# Backup and restore
json_handler.backup_json('backup.json')
json_handler.restore_backup('backup.json')

# Get file size
print(json_handler.get_size())
```

**Features**

- Read, write, and update JSON files easily.

- Deep search for nested keys.

- Append and remove elements from lists inside JSON.

- Backup and restore your JSON data.

- Efficient error handling with descriptive error messages.

- Supports nested structures and complex data types.

- Works with pretty-printed JSON strings.

- File size information and other utility functions.

- Backup and restore capabilities.


**Error Handling**

In case of errors, NanoJson will return detailed error messages including the type of error and the line number where it occurred. This helps developers easily identify and resolve issues in their code.

For example, if a file is not found:

```
data = json_handler.read_json()
if isinstance(data, str) and "Error" in data:
  print(f"Error: {data}")
```

**License**

This project is licensed under the MIT License. See the LICENSE file for more details.

-----

**Support**

If you encounter any issues or have questions, feel free to open an issue on the repository or contact the author.


---

Author: [Mohamed Ahmed Ghanam](https://t.me/midoghanam)


---

NanoJson – A simple and powerful JSON handler for Python.
