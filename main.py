from socket import *
import os
import re
import collections

# Current server path
path = os.path.dirname(os.path.abspath(__file__)) + "\serverFiles"

# Getting files supported by the server
serverFiles = ['/', '/sortbyname', '/sortbyprice']
for root, dirs, files in os.walk(path):
    for file in files:
        serverFiles.append("/" + file)


# Function: Extracts the route from HTTP request
def getRequestRoute(Request):
    return (Request.partition('\n')[0]).split(" ")[1]


# Function: Requests handler
def get(Request, connection, clientAddress):
    route = getRequestRoute(Request).lower()
    if route in serverFiles:
        connection.send("HTTP/1.0 200 OK".encode())

        # Image Routes Handling
        if re.search(r"\.png|\.jpeg|\.jpg", route):
            if re.search(r"\.png", route):
                connection.send("\nContent-Type: image/png\n\n".encode())
            else:
                connection.send("\nContent-Type: image/jpeg\n\n".encode())
            image_data = open("serverFiles" + route, "rb")
            Bytes = image_data.read()
            connection.send(Bytes)
            image_data.close()

        # Index route handling
        elif route == "/":
            connection.send("\nContent-Type: text/html\n\n".encode())
            index = open("serverFiles/index.html", "r")
            connection.send(index.read().encode())
            index.close()

        elif route == "r\.png":
            connection.send("\nContent-Type: image/png\n\n".encode())
            index = open("serverFiles/mq5.png", "r")
            connection.send(index.read().encode())
            index.close()
        elif route == "r\.jpg":
            connection.send("\nContent-Type: image/jpg\n\n".encode())
            index = open("serverFiles/abood.jpg", "r")
            connection.send(index.read().encode())
            index.close()
        # HTML files handling
        elif re.search(r"\.html", route):
            connection.send("\nContent-Type: text/html\n\n".encode())
            File = open("serverFiles" + route, "r")
            connection.send(File.read().encode())
            File.close()

        # CSS files handling
        elif re.search(r"\.css", route):
            connection.send("\nContent-Type: text/css\n\n".encode())
            File = open("serverFiles" + route, "r")
            connection.send(File.read().encode())
            File.close()

        # Java Script files handling
        elif re.search(r"\.js", route):
            connection.send("\nContent-Type: text/css\n\n".encode())
            File = open("serverFiles" + route, "r")
            connection.send(File.read().encode())
            File.close()
        elif route == "/bzu.html":
            connection.send("\nContent-Type: text/html\n\n".encode())
            index = open("serverFiles/bzu.html", "r")
            connection.send(index.read().encode())
            index.close()

        # Text files handling
        elif route == "/sortbyname" or route == "/sortbyprice":
            connection.send("\nContent-Type: text/html\n\n".encode())

            # Extracting data from file
            phones = open("serverFiles/phones.txt", "r")
            phoneDict = {}
            for line in phones:
                key, value = line.split(",")
                phoneDict[key] = int(value)

            # Sorting the data
            keySorted = collections.OrderedDict(sorted(phoneDict.items()))
            valueSorted = {k: v for k, v in sorted(phoneDict.items(), key=lambda item: item[1])}
            # dataDict = {}
            htmlData = ""

            if route == "/sortbyname":
                dataDict = keySorted
            else:
                dataDict = valueSorted

            for key in dataDict:
                htmlData += "<div class='item clearfix'><div class='key float-left'>" + key + "</div><div " \
                                                                                              "class='value " \
                                                                                              "float-right'>" + str(
                    dataDict[key]) + \
                            "$</div></div> "

            listingIndex = open("serverFiles/listing.html", "r")
            htmlCode = listingIndex.read().replace("<!--REPLACE_ME-->", htmlData)
            connection.send(htmlCode.encode())
            listingIndex.close()

    else:
        connection.send('HTTP/1.1 404 Not Found'.encode())
        connection.send("\nContent-Type: text/html\n\n".encode())
        File = open("serverFiles/error.html", "r")
        html_code = File.read().replace("<!--IP-->", clientAddress[0]).replace("<!--PORT-->", str(clientAddress[1]))

        connection.send(html_code.encode())
        File.close()


# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 6500

# Create socket

# iPv4, TCP Connection
server_socket = socket(AF_INET, SOCK_STREAM)

# Avoid bind() exception: OSError: [Errno 48] Address already in use
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Assigning port 9000 with the server
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:

    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Get the client request
    request = client_connection.recv(1024).decode()

    # Handling client request
    if len(request) > 0:
        get(request, client_connection, client_address)

    print(request)

    # Closing the connection
    client_connection.close()

    # Close socket
    # server_socket.close()
    # By Mohammad Qashoo
