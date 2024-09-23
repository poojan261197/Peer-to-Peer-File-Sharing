from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Dictionary to store peers and their files
peers_files = {}

@app.route('/register', methods=['POST'])
def register_peer():
    peer_data = request.json
    peer_id = peer_data.get('peer_id')
    peer_files = peer_data.get('files', [])
    peers_files[peer_id] = peer_files
    return jsonify({"message": "Peer registered successfully!"}), 201

@app.route('/files', methods=['GET'])
def get_files():
    return jsonify(peers_files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    # Save the file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Gather file metadata
    file_size = os.path.getsize(file_path)  # Get file size
    file_type = file.content_type  # Get file type

    # Store metadata for the peer
    peer_id = request.form.get('peer_id')
    if peer_id not in peers_files:
        peers_files[peer_id] = []
    peers_files[peer_id].append({
        "filename": file.filename,
        "size": file_size,
        "type": file_type
    })

    return jsonify({"message": "File uploaded successfully!", "metadata": {"size": file_size, "type": file_type}}), 201

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/search', methods=['GET'])
def search_files():
    query = request.args.get('query')
    results = {}
    for peer_id, files in peers_files.items():
        matching_files = [f for f in files if query in f["filename"]]
        if matching_files:
            results[peer_id] = matching_files

    if not results:
        return jsonify({"message": "No files found."}), 404

    return jsonify(results)

@app.route('/delete', methods=['POST'])
def delete_file():
    peer_id = request.json.get('peer_id')
    filename = request.json.get('filename')

    if peer_id in peers_files:
        files = peers_files[peer_id]
        for file_info in files:
            if file_info['filename'] == filename:
                files.remove(file_info)  # Remove from the list
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)  # Delete the file from the server
                return jsonify({"message": f"{filename} deleted successfully!"}), 200

    return jsonify({"message": "File not found!"}), 404

@app.route('/list_files', methods=['POST'])
def list_files():
    peer_id = request.json.get('peer_id')

    if peer_id in peers_files:
        return jsonify(peers_files[peer_id]), 200
    else:
        return jsonify({"message": "Peer not found!"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
