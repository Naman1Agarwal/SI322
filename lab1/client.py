from socket import *

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input('Enter something')
clientSocket.send(sentence.encode())

serverSentence = clientSocket.recv(1024)
print("From server:", serverSentence.decode())

clientSocket.close()
