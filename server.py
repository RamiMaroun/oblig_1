import socket
import threading

# We will need an IP-address for the host and a free port number for our server.
# In this example, we will use the localhost address (127.0.0.1) and the port 55555.
host = "127.0.0.1"
port = 55555

# Starting Server
# When we define our socket, we need to pass two parameters. These define the type of socket we want to use.
# The first one (AF_INET) indicates that we are using an internet socket rather than an unix socket.
# The second parameter stands for the protocol we want to use.
# SOCK_STREAM indicates that we are using TCP and not UDP.
# we bind it to our host and the specified port by passing a tuple that contains both values.
# We  put our server into listening mode, so that it waits for clients to connect.
# we create two empty lists, which we will use to store the connected clients and their nicknames later on.
# Connection Data

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# sending a message to each client that is connected and therefore in the clients list.


def broadcast(message):
    for client in clients:
        client.send(message)


# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break
# Receiving / Listening Function


def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
