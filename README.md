# File Sharing Application Protocol

## Overview

This protocol defines the communication format between the client and server in a file-sharing application based on a client-server model. The protocol includes request and response messages, each comprising three main parts: the request line, message header, and message body. The structure varies depending on whether it's a request or response message.

## Request Message Format

![Request Message Format](images/request_message_format.png)

- `<method>`: Request method (e.g., GET, POST, LIST).
- `<IP address>`: Server's IP address.
- `<File name>`: Name of the file being uploaded or downloaded.
- `<permission>`: Specifies if the file is open or protected.
- `<key>`: Key for accessing protected files.
- `<carriage_return>`: Carriage return.
- `<Header>`: Additional information about the request.
- `<message-body>`: Actual content of the file.

## Response Message Format

![Response Message Format](images/response_message_format.png)

- `<status code>`: Three-digit code indicating the status of the request (e.g., 200 for OK, 404 for Not Found).
- `<status message>`: Human-readable response status description.
- `<headers>`: Additional information about the response.
- `<message-body>`: Actual data being sent in the response (for file downloads).

## Features

### File Storage & User Authentication

#### Segregation of File Storage Directories

The server utilizes two directories: "Open_Storage" for open files and "Protected_Storage" for protected files. This segregation simplifies tracking and categorization of files based on their permissions.

#### File Management & Tracking Mechanism in Protected Storage

- **File Tagging:** Each protected file is associated with a key and tagged in a designated text file called "keys_admn."
  
- **Key Administration File (`keys_admn.txt`):**
  - Stores a list of existing keys with corresponding file names.
  - Simplifies file tracking and avoids the need to open each file for key verification.

![Key Administration File](images/keys_admn_file.png)

### File Validation

The server employs the hashlib Python library to validate the integrity of files during transit. The validation process ensures that the files uploaded to the server match their original versions. If a discrepancy is detected, the file upload is terminated, and an error message is sent to the client.

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

This file-sharing application protocol ensures secure and efficient communication between the client and server. It supports various features, including file segregation, user authentication, and file validation, enhancing the overall reliability of the system.

---

**Note:** This project is developed as part of a sample networked applications and may be subject to further improvements and enhancements.
