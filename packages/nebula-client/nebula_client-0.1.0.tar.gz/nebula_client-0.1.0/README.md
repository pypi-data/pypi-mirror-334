# Nebula Python Client

A Python client library for interacting with the Nebula file system API.

## Installation

```bash
pip install nebula-client
```

## Usage

```python
from nebula_client import NebulaClient

# Initialize the client with your API key
client = NebulaClient(api_key="your_api_key")

# List files in a cluster
files = client.list_files(cluster_id="your_cluster_id")

# Upload a file
result = client.upload_file(
    cluster_id="your_cluster_id",
    file_path="path/to/your/file.txt"
)

# Download a file
client.download_file(
    cluster_id="your_cluster_id", 
    file_id="file_id", 
    output_path="path/to/save"
)

# Create a folder
folder = client.create_folder(
    cluster_id="your_cluster_id",
    folder_name="New Folder"
)

# Delete files or folders
client.delete_files(
    cluster_id="your_cluster_id",
    file_ids=["file_id_1", "file_id_2"]
)

# Move files to a different folder
client.move_files(
    cluster_id="your_cluster_id",
    file_ids=["file_id_1", "file_id_2"],
    target_folder_id="target_folder_id"
)

# Rename a file or folder
client.rename_file(
    cluster_id="your_cluster_id",
    file_id="file_id",
    new_name="New Name"
)
```

## API Reference

### NebulaClient

The main client class for interacting with the Nebula API.

#### `__init__(api_key, base_url=None)`

Initialize a new client instance.

- `api_key` (str): Your Nebula API key
- `base_url` (str, optional): Custom API base URL. Defaults to production API.

#### File Operations

- `list_files(cluster_id, folder_id="ROOT")`: List files and folders
- `get_upload_url(cluster_id, file_name, folder_id="ROOT", content_type=None)`: Get a pre-signed upload URL
- `upload_file(cluster_id, file_path, folder_id="ROOT", content_type=None)`: Upload a file
- `get_download_url(cluster_id, file_id)`: Get a pre-signed download URL
- `download_file(cluster_id, file_id, output_path)`: Download a file
- `create_folder(cluster_id, folder_name, parent_folder_id="ROOT")`: Create a folder
- `delete_files(cluster_id, file_ids)`: Delete files/folders
- `move_files(cluster_id, file_ids, target_folder_id)`: Move files to another folder
- `rename_file(cluster_id, file_id, new_name)`: Rename a file/folder

## License

MIT 