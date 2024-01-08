import socket, os, hashlib

# Function to verify the integrity of the downloaded file (not implemented)
def verify(cl_socket):
    # This function is currently under construction and not implemented yet
    return

# Function to add open files to the Open Storage directory
def add_open(filename, data):
    with open("./Open_Storage/"+filename, 'w') as file:
        file.write(data)

# Function to generate a key for protecting files (under construction)
def generate_key(filename):
    # This function is currently under construction and needs to be implemented
    key = ""
    return key

# Function to manage the list of protected files and associated keys
def add_protected(key, filename, new):
    # This function is under construction and not fully implemented
    # It is intended to add a protected file and its key to the keys_admn.txt file
    if new == "y":
        with open("./Protect_Storage/keys_admn.txt", "a") as file:
            file.write(f"{key}: {filename}")
    else:
        with open("./Protect_Storage/keys_admn.txt", "r") as file:
            arrdata = file.readlines()

            if key > len(arrdata):  # Assuming keys are numbers generated chronologically
                arrdata[key] += ', ' + filename
                data = "\n".join(arrdata)
            else:
                print("Key does not exist.")  # Change this to handle the case where the key doesn't exist
                return

        with open("./Protect_Storage/keys_admn.txt", "w") as file:
            file.write(data)

# Function to receive files from the client (under construction)
def receive_file(cl_socket):
    # Send a request for the filename from the client
    cl_socket.send(("Enter file name to POST:   ").encode())

    # Receive the filename from the client
    filesent = cl_socket.recv(1024).decode()
    print(f'Receiving file "{filesent}"...')

    # Send acknowledgment to the client for filename received
    cl_socket.send(("File name received by server successfully!").encode())

    # Receive data from the client
    data = cl_socket.recv(1024).decode()

    if not data:
        print("No data found")
        return

    # Send acknowledgment to the client for data received
    cl_socket.send(("Data received by server!").encode())

    # Verify if the received data matches its hash
    received_hash = cl_socket.recv(16)
    hash_chk = hashlib.md5()
    hash_chk.update(data.encode())

    if received_hash == hash_chk.digest():
        cl_socket.send((f"File {filesent} uploaded successfully and verified!").encode())
    else:
        cl_socket.send((f"Error: File {filesent} upload unsuccessful because the file is not valid!").encode())
        return

    # Check if the file is protected or open
    permission = cl_socket.recv(1024).decode()

    if permission == "protected":
        # If a file is protected, check if the user is adding the file for the first time or not
        cl_socket.send(("If you are not adding the file for the 1st time, enter the protection key/'Yes' for the 1st time:   ").encode())
        response = cl_socket.recv(1024).decode()

        if response.upper() == "YES":
            key = generate_key(filesent)
            add_protected(key, filesent, "y")
        else:
            key = response
            add_protected(key, filesent, "n")  # Adjust in the definition
    else:
        # If the file is open, write data to the file in Open Storage
        add_open(filesent, data)

    print('File received successfully!')

# Function to list files (under construction)
def list_files():
    # This function is under construction and needs to be implemented
    print(os.listdir("./Open_Storage") + os.listdir("./Protected_Storage"))

# Function to handle downloading files from the server (under construction)
def download_file(cl_socket):
    # Send a request for the filename from the client
    cl_socket.send(("Enter file name to GET [download]:   ").encode())

    # Receive the filename from the client
    fileRqsted = cl_socket.recv(1024).decode()
    print(f'Receiving file "{fileRqsted}"...')

    # Open the file and read data from it
    with open("./Open_Storage/"+ fileRqsted, 'r') as file:
        # Compute the hash of the file
        hash_chk = hashlib.md5()

        # Read data from the file
        data = file.read()
        hash_chk.update(data.encode())

    print("File data sent by server successfully!")

    # Send data to the client
    cl_socket.send(data.encode())

    # Receive acknowledgment from the client
    print(cl_socket.recv(1024).decode())

    # Send the hash of the file to the client
    cl_socket.send(hash_chk.digest())

    return

# Main server function
def main():
    # Set up the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8000))
    server_socket.listen(1)

    print('Waiting for client connection...')

    while True:
        # Accept client connection
        client_socket, address = server_socket.accept()
        print(f'Client connected from {address}')

        # Receive the type of request from the client (GET, POST, LIST)
        mode = client_socket.recv(1024).decode()

        # Handle the corresponding request type
        if mode.upper() == "GET":
            download_file(client_socket)
        elif mode.upper() == "POST":
            receive_file(client_socket)
        elif mode.upper() == "LIST":
            list_files()
        else:
            print("404: Request not recognized")
            break

        # Close the client socket
        client_socket.close()

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
