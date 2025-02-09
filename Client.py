import socket
import hashlib
import os

# Constants
CHUNK_SIZE = 1024  # Size of each file chunk in bytes
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

def reassemble_file(chunks, output_path):
    """Reassemble the file from chunks."""
    chunks.sort(key=lambda x: x[0])  # Sort chunks by sequence number
    with open(output_path, "wb") as f:
        for seq_num, chunk in chunks:
            f.write(chunk)

def calculate_checksum(file_path):
    """Calculate the MD5 checksum of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def start_client(file_path):
    """Start the client to upload and verify the file."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Send file path to server
    client_socket.send(file_path.encode())

    # Receive checksum from server
    checksum = client_socket.recv(1024).decode()
    print(f"Received checksum: {checksum}")

    # Receive file chunks from server
    chunks = []
    while True:
        data = client_socket.recv(CHUNK_SIZE + 10)  # Extra bytes for sequence number
        if not data:
            break
        seq_num, chunk = data.split(b':', 1)
        chunks.append((int(seq_num), chunk))

    # Reassemble file
    output_path = "received_" + os.path.basename(file_path)
    reassemble_file(chunks, output_path)

    # Verify checksum
    received_checksum = calculate_checksum(output_path)
    if received_checksum == checksum:
        print("Transfer Successful: File integrity verified.")
    else:
        print("Transfer Failed: Checksum mismatch.")

    client_socket.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python client.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist")
        sys.exit(1)

    start_client(file_path)