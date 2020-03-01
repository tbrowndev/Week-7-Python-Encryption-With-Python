import socket
import ca
import cipher

#Server Side
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket sucessfully created!")

server_name = "MyServer"
server_public_key = 5
print( ca.RegisterServer(server_name, server_public_key) )

port = 9500 #1. accepts connections on port 9500
s.bind((socket.gethostbyname('localhost'),port)) #socket now is binded to port 9500

s.listen(5) #socket now listens to port 9500 for incoming messages
print('Socket is now Listening...')


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
            client_socket.close()