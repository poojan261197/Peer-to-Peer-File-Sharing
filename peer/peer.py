import requests
import os

def register_peer(peer_id, files):
    url = "http://127.0.0.1:5000/register"
    data = {
        "peer_id": peer_id,
        "files": files
    }
    response = requests.post(url, json=data)
    print("Register response:", response.json())

def upload_file(peer_id, filename):
    url = "http://127.0.0.1:5000/upload"
    with open(filename, 'rb') as f:
        files = {'file': f}
        data = {'peer_id': peer_id}
        response = requests.post(url, files=files, data=data)
        print("Upload response:", response.json())

def download_file(filename):
    url = f"http://127.0.0.1:5000/download/{filename}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename} successfully.")
    else:
        print("Error downloading file:", response.json())

def search_files(query):
    url = f"http://127.0.0.1:5000/search?query={query}"
    response = requests.get(url)
    print("Search response:", response.json())

def delete_file(peer_id, filename):
    url = "http://127.0.0.1:5000/delete"
    data = {
        "peer_id": peer_id,
        "filename": filename
    }
    response = requests.post(url, json=data)
    print("Delete response:", response.json())

def list_files(peer_id):
    url = "http://127.0.0.1:5000/list_files"
    data = {
        "peer_id": peer_id
    }
    response = requests.post(url, json=data)
    print("List files response:", response.json())

if __name__ == "__main__":
    peer_id = "peer_1"  # Change this for different peers
    files = ["file1.txt", "file2.txt"]  # List of files for this peer
    
    # Register the peer
    register_peer(peer_id, files)
    
    # Upload a file
    upload_file(peer_id, 'file1.txt')
    
    # List files for the peer
    list_files(peer_id)  # Test listing files
    
    # Search for a file
    search_files('file1')
    
    # Delete a file
    delete_file(peer_id, 'file1.txt')  # Test deleting the uploaded file
