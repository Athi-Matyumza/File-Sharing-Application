# Networked File Sharing Application

## Project Overview

This project involves the design and implementation of a client-server file sharing application using TCP sockets in Python. The primary focus is on protocol design, socket programming, and ensuring file integrity during transmission. The application follows a client-server model where clients can upload/download files from a shared server.

## Application Features

1. **File Upload/Download:**
   - Clients can upload files to the server.
   - Clients can download files from the server.

2. **File Visibility:**
   - Clients can indicate whether uploaded files are 'open' or 'protected.'
   - 'Open' files are visible and downloadable by any client.
   - 'Protected' files are only accessible to clients with the correct 'key.'

3. **File Listing:**
   - Clients can query the server for a listing of available files.

4. **File Validation:**
   - Implement a file validation mechanism to ensure the integrity of transferred files.
   - Include validation information within each message for sender and receiver verification.

5. **Error Handling:**
   - Server sends appropriate error messages if the requested file is not present or the client lacks permission.

## Protocol Design

### Privacy/Confidentiality Considerations

- Users can specify file sharing permissions.
- Options include:
  - Visibility/Downloadable by anyone.
  - Visibility/Downloadable to specific clients.
  - Shared secret-key access.

### Message Types

1. **Command Messages:**
   - Initiate or terminate communication.
   - Specify actions such as upload, download, and file listing.

2. **Data Transfer Messages:**
   - Carry the actual data exchanged between parties.
   - May be fragmented into multiple messages.

3. **Control Messages:**
   - Manage dialogue between parties.
   - Include acknowledgments and retransmission requests.

### Message Structure

- **Header:**
  - Contains fields like message type, command, recipient information, and sequence information.
  - Fixed size to help the receiver understand the message.

### Communication Rules

- Clearly specify messages and reactions for each communication scenario.
- Represent rules with sequence diagrams, including at least two:
  1. Upload process sequence diagram.
  2. Download process sequence diagram.

## How to Run

1. **Server:**
   - Run the server script specifying the listening address and port.
     ```bash
     python server.py -a <address> -p <port>
     ```

2. **Client:**
   - Run the client script with command-line arguments.
     ```bash
     python client.py -a <server_address> -p <server_port> -u <upload_file> -d <download_file>
     ```

## Conclusion

This project aims to provide a secure and efficient file-sharing solution using TCP sockets. The protocol design ensures privacy, reliability, and file integrity. The application allows users to seamlessly upload and download files while managing access permissions.

---

**Note:** This project is developed as part of a networked applications assignment and may be subject to further improvements and enhancements.
