
from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1)
print("Server is ready to respond to http requests!")


def parse_request(req):
    parts = req.split()
    if not (parts[0].startswith("GET")):
        return 400
    return parts[1]
    
    
def read_file(filename):
    fd = open("." + filename)
    content = fd.read()
    return content


def form_response(req):
    
    filename = parse_request(req)
    body = read_file(filename)  
    
    if filename == 400:
        return "HTTP/1.1 400 Bad Request\r\n"
    
        
        
    resp = ""
    resp += "HTTP/1.1 200 OK\n"
    resp += "Content-Type: text/html; charset=utf-8\n"
    resp += "Content-Length: " + str(len(body)) + "\n"
    resp += "\r\n"
    resp += body
    return resp



while True:
    connectionSocket, addr = serverSocket.accept()
    http_req = connectionSocket.recv(1024).decode() 

    http_resp = form_response(http_req)

    connectionSocket.send(http_resp.encode())
    connectionSocket.close()

