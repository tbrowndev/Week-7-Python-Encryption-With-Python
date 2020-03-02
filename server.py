import socket
import cipher

cas = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket sucessfully created!")

server_name = "MyServer"
server_public_key = "5"

#register with Certificate Authority
ca_server_port = 9501
cas.connect((socket.gethostbyname('localhost'),ca_server_port))
print( cas.recv(1024).decode("utf-8"))
cas.send(server_name.encode("utf-8"))
print( cas.recv(1024).decode("utf-8"))
cas.send(server_public_key.encode("utf-8"))
print(cas.recv(1024).decode("utf-8"))
cas.close()
# registration complete.

#start server cosket for clients.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 9500 
s.bind((socket.gethostbyname('localhost'),port)) 
s.listen(5)
print('Server is now Listening for Clients...')

#infinite loop waiting for clients
while True:
    client_socket,client_address = s.accept()
    print("Init started with Client: ", client_address)
    client_socket.send(server_name.encode("utf-8"))
    print("Sent Server Name")
    message = client_socket.recv(1024).decode("utf-8")
    if message.lower == "goodbye":
        client_socket.close()
    else:
        key = server_public_key
        if ( message == cipher.encrypt( "Session Cipher Key", key) ):
            print("Client session cihper authenticated")
            print("Sending Acknowledgement...")
            client_socket.send( cipher.encrypt("acknowledged", key).encode("utf-8") )
            print("Session Secured. Starting Session....")
            while True:
                client_message = client_socket.recv(1024)
                print( client_message.decode("utf-8") )
                if client_message.decode("utf-8") == "goodbye":
                    print("Session Ended with client: ", client_address)
                    client_socket.close()
                    break
                else:
                    client_socket.send(client_message)
        else:
            client_socket.send( "Goodbye".encode("utf-8") )
            client_socket.close()