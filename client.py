import socket
import ca
import cipher

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 9500 #1. client connects to port 9500

s.connect((socket.gethostbyname('localhost'),port)) #IP address of this computer on the network

server_name = s.recv(1024).decode("utf-8")
print("Connected to Server: ", server_name)
server_public_key = ca.ValidateServer(server_name)
print("Authenticating...")
if server_public_key is not None:
    key = int( server_public_key )
    session_cipher = cipher.encrypt("Session Cipher Key", key)
    print("sending cipher...")
    s.send( session_cipher.encode("utf-8") )
else:
    print("not Authentic!")
    s.send( "goodbye".encode("utf-8") )
    s.close()
acknowledgement = s.recv(1024).decode("utf-8")
print("Acknowledging...")
if acknowledgement == cipher.encrypt("acknowledged", key):
    print("Session Secured. Starting Session....")
    while True:
        message = input("Message To Server: ")
        s.send( message.encode("utf-8") )
        if message == "goodbye":
            s.close()
            break
        print( s.recv(1024).decode("utf-8") )
else:
    s.close()
