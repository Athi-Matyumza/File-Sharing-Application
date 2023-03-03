import socket, hashlib

def verify(cl_socket, data, hash_chk, filename):
    # compute hash of file
    hash_chk.update(data.encode())

    #receive hash of file from server
    received_hash = cl_socket.recv(16)

    if  (received_hash == hash_chk.digest()):
        print(f"File {filename} downloaded successfully and verified!")
    else:
        print(f"Error: file {filename} downloaded successfully and but not valid!")

def POST_reqst(cl_socket):
    # Sending filename to server
    filename = input(cl_socket.recv(1024).decode())
    # permission = input("Please enter file name:   ")
    cl_socket.send(filename.encode())
    print(f'Sending file "{filename}"...')

    print(cl_socket.recv(1024).decode())

    # open file and read data from it
    with open("./Data/"+ filename, 'r') as file:
        # compute hash of file
        hash_chk = hashlib.md5()

        # read data from file
        data = file.read()

        hash_chk.update(data.encode())
        
    print("File data sent by client successfully!")
    # send data to server
    cl_socket.send(data.encode())

    print(cl_socket.recv(1024).decode()) # message received from server to confirm data RECEIVED
                                         # but verified

    cl_socket.send(hash_chk.digest())

    status = cl_socket.recv(1024).decode()
    # print(status)

    if (status.find("unsuccesful") == -1):
        permission = input("Is the file protected or not [Yes/No]:  ")
        # permission = input(cl_socket.recv(1024).decode())

        if (permission.lower() == "yes"):
            cl_socket.send(("protected").encode())
        else:
            cl_socket.send(("not protected").encode())

        print('File sent successfully!')
    else:
        print("File upload terminated!")

def GET_reqst(cl_socket):   #UNDER CONSTRUCTION
# Sending filename to server
    filename = input(cl_socket.recv(1024).decode())
    # permission = input("Please enter file name:   ")
    cl_socket.send(filename.encode())
    print(f'Sending file "{filename}"...')

    data = cl_socket.recv(1024).decode()
        
    cl_socket.send(("Data received by client.").encode())

    with open("./Data/"+filename, 'w') as file:
        hash_chk = hashlib.md5()
        file.write(data)

    # verify received file
    verify(cl_socket, data, hash_chk, filename) 

    # receive data from server
    # cl_socket.send(data.encode())

def LIST_reqst(cl_socket):

    return

def main():
    # set up client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #add arguments here - UNDER CONSTRUCTION 
    # //
    # //
    # //
    # //

    client_socket.connect(('localhost', 8000))

    reqst_msg = input("Enter request [GET/POST/LIST]:  ")

    client_socket.send(reqst_msg.encode())

    if (reqst_msg.upper() == "GET"):
        GET_reqst(client_socket)
    elif (reqst_msg.upper() == "POST"):
        POST_reqst(client_socket)
    elif (reqst_msg.upper() == "LIST"):
            LIST_reqst(client_socket)

    # close socket
    client_socket.close()

if __name__ == "__main__":
    main()
