serverFile = "registeredServers.txt"

def RegisterServer(serverName, pk):
    try:
        registeredServers = _GetRegisteredServers()
        if registeredServers.get(serverName, None) == None:
            registry = open(serverFile, "a")
            registry.write( "{}:{}".format(serverName, pk) )
            registry.close()
        else:
            return "Server Already Registered With Certificate Authority"
    except:
        return "Registration Failed"
    return "Registered With Certificate Authority"

def ValidateServer(serverName):
    registry = _GetRegisteredServers()
    return registry.get(serverName, None)

def _GetRegisteredServers():
    registry = {}
    f = open(serverFile, "r")
    servers = f.readlines()
    for line in servers:
        server = line.split(':')
        registry[server[0]] = server[1]
    f.close()
    return registry