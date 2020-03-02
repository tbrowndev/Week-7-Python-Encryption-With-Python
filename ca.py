import socket
import threading

serverFile = "registeredServers.txt"

server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Sockets sucessfully created!")

server_port = 9501
client_port = 9502
server_s.bind((socket.gethostbyname('localhost'),server_port))
client_s.bind((socket.gethostbyname('localhost'),client_port))

server_s.listen(1)
client_s.listen(1)
print('Certificate Authority is now Listening on port 9501 for Servers...')
print('Certificate Authority is now Listening on port 9502 for Clients...')

def RegisterServers(ss):
    while True:
        sSocket, sAddress = ss.accept()
        print("Server ", sAddress, " is registering....")
        sSocket.send("CA Request Server Name...".encode("utf-8"))
        serverName = sSocket.recv(1024).decode("utf-8")
        sSocket.send("CA Request Server Public Key...".encode("utf-8"))
        pk = sSocket.recv(1024).decode("utf-8")
        print(serverName, pk)
        try:
            registeredServers = _GetRegisteredServers()
            if registeredServers.get(serverName, None) == None:
                registry = open(serverFile, "a")
                registry.write( "{}:{}\n".format(serverName, pk) )
                registry.close()
                print("Registered With Certificate Authority")
                sSocket.send("Registered With Certificate Authority".encode("utf-8"))
                sSocket.close()
            else:
                print("Server Already Registered With Certificate Authority")
                sSocket.send("Server Already Registered With Certificate Authority".encode("utf-8"))
                sSocket.close()
        except:
            print("Registration Failed")
            sSocket.send("Registration Failed".encode("utf-8"))
            sSocket.close()
        

def ValidateServer(serverName):
    registry = _GetRegisteredServers()
    return registry.get(serverName, None)

def _GetRegisteredServers():
    registry = {}
    f = open(serverFile, "r")
    servers = f.readlines()
    for line in servers:
        server = line.strip().split(':')
        registry[server[0]] = server[1]
    f.close()
    return registry

server_thread = threading.Thread(target=RegisterServers, args=(server_s,))
server_thread.start()
while True:
    cSocket, cAddress = client_s.accept()
    serverName = cSocket.recv(1024).decode("utf-8")
    print("Client Requested Public key for Server: ", serverName)
    server_public_key = ValidateServer(serverName)
    if server_public_key is not None:
        cSocket.send(server_public_key.encode("utf-8"))
    else:
        cSocket.send("Invalid".encode("utf-8"))