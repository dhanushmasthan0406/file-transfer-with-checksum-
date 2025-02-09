# File Transfer with Checksum Verification

This project implements a **file transfer system** using Python's **socket programming** with **SHA-256 checksum verification** to ensure data integrity.

## Features
- **Reliable File Transfer**: Transfers files over a network using TCP sockets.
- **Checksum Verification**: Uses SHA-256 to verify the integrity of the received file.
- **Chunk-Based Transfer**: Supports large file transfers efficiently.

## How It Works
1. **Server (Sender)**
   - Computes the SHA-256 checksum of the file.
   - Sends the checksum to the client before transmitting the file.
   - Sends the file in chunks to optimize performance.

2. **Client (Receiver)**
   - Receives the checksum from the server.
   - Receives the file and saves it to disk.
   - Computes the checksum of the received file and compares it with the received checksum.
   - If the checksums match, the transfer is successful; otherwise, an error is reported.

## Installation
### Prerequisites
- Python 3.x

### Clone the Repository
```bash
git clone https://github.com/dhanushmasthan0406/file-transfer-with-checksum
```

## Usage
### Start the Server (Sender)
```bash
python Server.py
```

### Start the Client (Receiver)
```bash
python Client.py data.txt
```

## Example Output
```
Server:
Server listening on 127.0.0.1:5000...
Connected by ('127.0.0.1', 50520)
File sent successfully.

Client:
Connected to server at 127.0.0.1:5000
File received successfully. Checksum verified.
```

## License
This project is licensed under the MIT License 

## Author
Dhanush M ((https://github.com/dhanushmasthan0406/file-transfer-with-checksum)

