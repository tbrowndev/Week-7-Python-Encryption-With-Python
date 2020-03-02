import socket
import cipher

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cas = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 9500 

s.connect((socket.gethostbyname('localhost'),port)) 

server_name = s.recv(1024).decode("utf-8")
print("Connected to Server: ", server_name)

#contact Certificate Authority with servername
ca_server_port = 9502
cas.connect((socket.gethostbyname('localhost'),ca_server_port))
cas.send(server_name.encode("utf-8"))
server_public_key = cas.recv(1024).decode("utf-8")
# end Certificate Authority

print("Authenticating...")
if server_public_key != "Invalid":
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
