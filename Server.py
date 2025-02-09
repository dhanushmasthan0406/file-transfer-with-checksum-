import socket
import hashlib
import os

# Constants
CHUNK_SIZE = 1024  # Size of each file chunk in bytes
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

def calculate_checksum(file_path):
    """Calculate the MD5 checksum of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def split_file(file_path, chunk_size):
    """Split the file into chunks and assign sequence numbers."""
    chunks = []
    with open(file_path, "rb") as f:
        sequence_number = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            chunks.append((sequence_number, chunk))
            sequence_number += 1
    return chunks

def start_server():
    """Start the server to receive and process file chunks."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    # Receive file path from client
    file_path = client_socket.recv(1024).decode()
    print(f"Received file path: {file_path}")

    # Verify file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist on the server.")
        client_socket.close()
        server_socket.close()
        return

    # Calculate checksum
    checksum = calculate_checksum(file_path)
    print(f"Checksum: {checksum}")

    # Split file into chunks
    chunks = split_file(file_path, CHUNK_SIZE)

    # Send checksum and chunks to client
    client_socket.send(checksum.encode())
    for seq_num, chunk in chunks:
        client_socket.send(f"{seq_num}:".encode() + chunk)

    print("File transfer complete.")
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()