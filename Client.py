import socket, hashlib

# Function to verify the integrity of the downloaded file
def verify(cl_socket, data, hash_chk, filename):
    # Compute hash of the file data
    hash_chk.update(data.encode())

    # Receive hash of the file from the server
    received_hash = cl_socket.recv(16)

    # Compare the received hash with the computed hash
    if received_hash == hash_chk.digest():
        print(f"File {filename} downloaded successfully and verified!")
    else:
        print(f"Error: File {filename} downloaded successfully but not valid!")

# Function to handle POST requests (uploading files to the server)
def POST_reqst(cl_socket):
    # Sending filename request to the server
    filename = input(cl_socket.recv(1024).decode())
    cl_socket.send(filename.encode())
    print(f'Sending file "{filename}"...')

    # Receive acknowledgment from the server
    print(cl_socket.recv(1024).decode())

    # Open file and read data from it
    with open("./Data/" + filename, 'r') as file:
        # Compute hash of the file data
        hash_chk = hashlib.md5()

        # Read data from the file
        data = file.read()
        hash_chk.update(data.encode())

    print("File data sent by client successfully!")

    # Send data to the server
    cl_socket.send(data.encode())

    # Receive acknowledgment from the server for data received
    print(cl_socket.recv(1024).decode())

    # Send the hash of the file to the server for verification
    cl_socket.send(hash_chk.digest())

    # Receive the status of the file upload from the server
    status = cl_socket.recv(1024).decode()

    if "unsuccesful" not in status:
        # If upload is successful, ask for file protection status
        permission = input("Is the file protected or not [Yes/No]:  ")

        if permission.lower() == "yes":
            cl_socket.send(("protected").encode())
        else:
            cl_socket.send(("not protected").encode())

        print('File sent successfully!')
    else:
        print("File upload terminated!")

# Function to handle GET requests (downloading files from the server)
def GET_reqst(cl_socket):
    # Sending filename request to the server
    filename = input(cl_socket.recv(1024).decode())
    cl_socket.send(filename.encode())
    print(f'Sending file "{filename}"...')

    # Receive data from the server
    data = cl_socket.recv(1024).decode()

    # Send acknowledgment to the server for data reception
    cl_socket.send(("Data received by client.").encode())

    # Write the received data to a file
    with open("./Data/" + filename, 'w') as file:
        hash_chk = hashlib.md5()
        file.write(data)

    # Verify the integrity of the received file
    verify(cl_socket, data, hash_chk, filename)

# Function to handle LIST requests (list files on the server)
def LIST_reqst(cl_socket):
    # Placeholder for listing functionality
    return

# Main function
def main():
    # Set up the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect(('localhost', 8000))

    # Get the type of request from the user
    reqst_msg = input("Enter request [GET/POST/LIST]:  ")

    # Send the request type to the server
    client_socket.send(reqst_msg.encode())

    # Handle the corresponding request type
    if reqst_msg.upper() == "GET":
        GET_reqst(client_socket)
    elif reqst_msg.upper() == "POST":
        POST_reqst(client_socket)
    elif reqst_msg.upper() == "LIST":
        LIST_reqst(client_socket)

    # Close the socket
    client_socket.close()

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
