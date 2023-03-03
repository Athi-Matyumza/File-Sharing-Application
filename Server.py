import socket, os, hashlib

def verify(cl_socket):

    return

def add_open(filename, data):
    with open("./Open_Storage/"+filename, 'w') as file:
            file.write(data)

def generate_key(filename):  #UNDER CONSTRUCTION
    # ENTER CODE HERE
    key = ""

    return key

def add_protected(key, filename, new): #UNDER CONSTRUCTION
    if (new == "y"):
        with open("./Protect_Storage/keys_admn.txt", "a") as file:
            file.write(f"{key}: {filename}")
    else:
        with open("./Protect_Storage/keys_admn.txt", "r") as file:
            arrdata = file.readlines()

            if (key > len(arrdata)): # ASSUMING KEYS ARE NUMBERS GENERATED CHRONOLOGICALLY
                arrdata[key] += ', ' + filename
                data = "\n".join(arrdata)
            else:
                print("Key does not exist.") #CHANGE THIS
                return

        with open("./Protect_Storage/keys_admn.txt", "w") as file:
            file.write(data)

def receive_file(cl_socket): #UNDER CONSTRUCTION
    # receive filename from client
    cl_socket.send(("Enter file name to POST:   ").encode())

    filesent = cl_socket.recv(1024).decode()
    print(f'Receiving file "{filesent}"...')
    
    cl_socket.send(("File name received by server successfully!").encode())

    # receive data from client
    data = cl_socket.recv(1024).decode()

    # print("This is the data:", data)

    if not(data):
        print("No data found")
        return
    
    cl_socket.send(("Data received by server!").encode())
    #verify at this point if the data matches

    #receive hash of file from server
    received_hash = cl_socket.recv(16)

    hash_chk = hashlib.md5()
    hash_chk.update(data.encode())

    if  (received_hash == hash_chk.digest()):
        cl_socket.send((f"File {filesent} uploaded successfully and verified!").encode())
    else:
        cl_socket.send((f"Error: file {filesent} upload usuccessful because file is not valid!").encode())
        return

    # check if protected or open
    # cl_socket.send(("Is the file protected or not [Yes/No]:  ").encode())

    permission = cl_socket.recv(1024).decode()

    if (permission == "protected"):
        # if a file is protected check if the user is entering to the protected files 
        # for the first time or not
        cl_socket.send(("If you are not adding file for the 1st time enter protection key/ 'Yes' for 1st time:   ").encode())
        response = cl_socket.recv(1024).decode()

        if (response.upper() == "yes".upper()):
            key = generate_key(filesent)
            add_protected(key, filesent, "y")
        else:
            key = response
            add_protected(key, filesent, "n") #Adjust in definition
    else:
        add_open(filesent, data)
    # write data to file
    add_open(filesent, data)
            
    print('File received successfully!')

def list_files():   #UNDER CONSTRUCTION
    print(os.listdir("./Open_Storage") + os.listdir("./Protected_Storage"))

# def request_file(filename, permission):
def download_file(cl_socket):  #UNDER CONSTRUCTION
     # receive filename from client
    cl_socket.send(("Enter file name to GET [download]:   ").encode())

    fileRqsted = cl_socket.recv(1024).decode()
    print(f'Receiving file "{fileRqsted}"...')
    
     # open file and read data from it
    with open("./Open_Storage/"+ fileRqsted, 'r') as file:
        # compute hash of file
        hash_chk = hashlib.md5()

        # read data from file
        data = file.read()
        hash_chk.update(data.encode())
        
    print("File data sent by server successfully!")
    # send data to client
    cl_socket.send(data.encode())

    print(cl_socket.recv(1024).decode())

    # send hash of the file to client
    cl_socket.send(hash_chk.digest())

    # cl_socket.send(("File name received by server successfully!").encode())

    return

def main():
    # set up server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8000))
    server_socket.listen(1)

    print('Waiting for client connection...')

    while True:
        # accept client connection
        client_socket, address = server_socket.accept()
        print(f'Client connected from {address}')

        mode = client_socket.recv(1024).decode()

        if (mode.upper() == "GET"):
            download_file(client_socket)
        elif (mode.upper() == "POST"):
            receive_file(client_socket)
        elif (mode.upper() == "LIST"):
            list_files()
        else:
            print("404: request not recognised")
            break

        # Receiving function call [check mode (i.e send or receive)]

        # close sockets
        client_socket.close()

    # server_socket.close()

if __name__ == "__main__":
    main()