import requests
import os
from typing import Dict, List, Optional, Union, BinaryIO
import json


class NebulaClient:
    """Client for interacting with the Nebula file system API."""

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        Initialize a Nebula client.
        
        Args:
            api_key: The API key for authentication
            base_url: Optional custom API base URL. If not provided, uses the production URL.
        """
        self.api_key = api_key
        self.base_url = base_url or "https://api.nebula-app.com"
        self.headers = {
            "Authorization": f"ApiKey {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def list_files(self, cluster_id: str, folder_id: str = "ROOT") -> Dict:
        """
        List files and folders in a cluster.
        
        Args:
            cluster_id: The ID of the cluster
            folder_id: Optional folder ID to list contents of. Defaults to root folder.
            
        Returns:
            Response containing files and folders
        """
        url = f"{self.base_url}/clusters/{cluster_id}/files/list"
        payload = {"parentFolderId": folder_id}
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_upload_url(self, cluster_id: str, file_name: str, folder_id: str = "ROOT", content_type: Optional[str] = None) -> Dict:
        """
        Get a pre-signed URL for uploading a file.
        
        Args:
            cluster_id: The ID of the cluster
            file_name: Name of the file to upload
            folder_id: Optional folder ID to upload to. Defaults to root folder.
            content_type: Optional content type of the file
            
        Returns:
            Response containing the upload URL and file ID
        """
        url = f"{self.base_url}/clusters/{cluster_id}/files/upload-url"
        payload = {
            "fileName": file_name,
            "folderId": folder_id
        }
        
        if content_type:
            payload["contentType"] = content_type
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def upload_file(self, cluster_id: str, file_path: str, folder_id: str = "ROOT", content_type: Optional[str] = None) -> Dict:
        """
        Upload a file to a cluster. Handles getting the presigned URL and uploading the file.
        
        Args:
            cluster_id: The ID of the cluster
            file_path: Path to the file to upload
            folder_id: Optional folder ID to upload to. Defaults to root folder.
            content_type: Optional content type of the file
            
        Returns:
            Response containing the file information
        """
        file_name = os.path.basename(file_path)
        
        # Get upload URL
        upload_response = self.get_upload_url(cluster_id, file_name, folder_id, content_type)
        
        # Upload file to presigned URL
        with open(file_path, 'rb') as file:
            upload_url = upload_response['signedUrl']
            file_id = upload_response['fileId']
            
            # Use standard requests lib for the upload (different headers for S3)
            upload_headers = {}
            if content_type:
                upload_headers["Content-Type"] = content_type
                
            response = requests.put(upload_url, data=file, headers=upload_headers)
            response.raise_for_status()
            
            return {
                "fileId": file_id,
                "fileName": upload_response.get('fileName', file_name),
                "status": "completed"
            }
    
    def get_download_url(self, cluster_id: str, file_id: str) -> Dict:
        """
        Get a pre-signed URL for downloading a file.
        
        Args:
            cluster_id: The ID of the cluster
            file_id: ID of the file to download
            
        Returns:
            Response containing the download URL
        """
        url = f"{self.base_url}/clusters/{cluster_id}/files/download-url"
        payload = {"fileId": file_id}
        
        response = requests.get(url, headers=self.headers, params=payload)
        response.raise_for_status()
        return response.json()
    
    def download_file(self, cluster_id: str, file_id: str, output_path: str) -> str:
        """
        Download a file from a cluster. Handles getting the presigned URL and downloading the file.
        
        Args:
            cluster_id: The ID of the cluster
            file_id: ID of the file to download
            output_path: Path where the downloaded file should be saved
            
        Returns:
            Path to the downloaded file
        """
        # Get download URL
        download_response = self.get_download_url(cluster_id, file_id)
        download_url = download_response['signedUrl']
        
        # Download file
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        # If output_path is a directory, use the original filename
        if os.path.isdir(output_path):
            output_path = os.path.join(output_path, download_response.get('fileName', f'file_{file_id}'))
            
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        return output_path
    
    def create_folder(self, cluster_id: str, folder_name: str, parent_folder_id: str = "ROOT") -> Dict:
        """
        Create a new folder in a cluster.
        
        Args:
            cluster_id: The ID of the cluster
            folder_name: Name of the folder to create
            parent_folder_id: Optional parent folder ID. Defaults to root folder.
            
        Returns:
            Response containing the created folder information
        """
        url = f"{self.base_url}/clusters/{cluster_id}/files/create-folder"
        payload = {
            "folderName": folder_name,
            "parentFolderId": parent_folder_id
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def delete_files(self, cluster_id: str, file_ids: List[str]) -> Dict:
        """
        Delete files or folders from a cluster.
        
        Args:
            cluster_id: The ID of the cluster
            file_ids: List of file/folder IDs to delete
            
        Returns:
            Response containing the deletion results
        """
        url = f"{self.base_url}/clusters/{cluster_id}/files/delete"
        payload = {"fileIds": file_ids}
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def move_files(self, cluster_id: str, file_ids: List[str], target_folder_id: str) -> Dict:
        """
        Move files or folders to a different folder.
        
        Args:
            cluster_id: The ID of the cluster
            file_ids: List of file/folder IDs to move
            target_folder_id: ID of the destination folder
            
        Returns:
            Response containing the move results
        """
        url = f"{self.base_url}/clusters/{cluster_id}/files/move"
        payload = {
            "fileIds": file_ids,
            "targetFolderId": target_folder_id
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def rename_file(self, cluster_id: str, file_id: str, new_name: str) -> Dict:
        """
        Rename a file or folder.
        
        Args:
            cluster_id: The ID of the cluster
            file_id: ID of the file/folder to rename
            new_name: New name for the file/folder
            
        Returns:
            Response containing the rename results
        """
        url = f"{self.base_url}/clusters/{cluster_id}/files/rename"
        payload = {
            "fileId": file_id,
            "newName": new_name
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json() 