from socket import *

serverIP, serverPort = 'localhost', 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind((serverIP, serverPort))
serverSocket.listen(1)
print("Server is listening...")

def parse_request(req):
    parts = req.split()
    if not (parts[0].startswith("GET")):
        raise ValueError("HTTP/1.1 400 Bad Request")
    return parts[1]

def read_file(filename):

    if filename.endswith(".png"):
        filetype = b"image/png"
    elif filename.endswith((".jpg", ".jpeg")):
        filetype = b"image/jpeg"
    else:
        filetype = b"text/html"

    fd = open("." + filename, "rb")
    content = fd.read()
    return filetype, content


def form_response(req):

    try:
        filename = parse_request(req)
        filetype, body = read_file(filename)
    except FileNotFoundError as e:
        return "HTTP/1.1 404 Not Found".encode()
    except ValueError as e:
        return str(e).encode()

    resp = b""
    resp += b"HTTP/1.1 200 OK\n"
    resp += b"Content-Type: %b; charset=utf-8\n" % filetype
    resp += b"Content-Length: " + str(len(body)).encode() + b"\n"
    resp += b"\r\n"
    resp += body

    return resp

while True:
    connectionSocket, addr = serverSocket.accept()

    http_req = connectionSocket.recv(1024).decode() 
    http_resp = form_response(http_req)

    connectionSocket.sendall(http_resp)
    connectionSocket.close()



