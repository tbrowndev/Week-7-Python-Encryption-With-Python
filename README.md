# Week-7-Python-Encryption-With-Python
 this is a client server application that first authenticates the connection to validate the server then starts session
 
 1. Server registers its name and public key with CA
 2. client send initial contact
 3. server responds with server name
 4. client validates the server name with CA to get the public key
 5. with public key from CA, an encrypted cipher session key is created and sent to server
 6. the server varifies the clients session key and acknowledges the client as authentic
 7. session begins and transmits messages back and for between server and client.
