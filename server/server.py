import os
import sys
import socket

localIP     = "127.0.0.1"
localPort   = 1997
bufferSize  = 65535

def receiveFile(file, ServerSocket):
	numberOfMessagesRead = 0
	numberOfBytesRead = 0
	file = file.decode("utf-8") 
	directories = "".join(file.split("\\")[:-1])
	if(directories != ''):
		os.makedirs(directories, exist_ok=True)
	
	f = open(file,'wb')
	message = ServerSocket.recv(bufferSize)
	while(message):
		numberOfMessagesRead = numberOfMessagesRead + 1
		numberOfBytesRead = numberOfBytesRead + len(message)
		if  message.decode("utf-8")  == "[END]":
			break
		f.write(message)
		message = ServerSocket.recv(bufferSize)
	f.close()
	return (numberOfMessagesRead, numberOfBytesRead)
def serverStreaming(option):
	
	option = option.upper()
	if option == "TCP":
		sck = socket.SOCK_STREAM
	elif option == "UDP":
		sck = socket.SOCK_DGRAM
	else:
		print('[Server]Not a valid option for socket')
		return (0, 0)
	numberOfMessagesRead = 0
	numberOfBytesRead = 0
	ServerSocket = socket.socket(family=socket.AF_INET, type=sck)
	ServerSocket.bind((localIP, localPort))
	if option == "TCP":
		ServerSocket.listen(1)
		conn, addr = ServerSocket.accept()
	

	while(True):
		if option == "TCP":
			message = ServerSocket.recv(bufferSize)
		else:
			bytesAddressPair = ServerSocket.recvfrom(bufferSize)
			message = bytesAddressPair[0]
			address = bytesAddressPair[1]
		numberOfMessagesRead = numberOfMessagesRead + 1
		numberOfBytesRead = numberOfBytesRead + len(message) 
		if message.decode("utf-8") == "[STOP]":
			break
		resp = receiveFile(message, ServerSocket)	
		numberOfMessagesRead = numberOfMessagesRead + resp[0]
		numberOfBytesRead = numberOfBytesRead + resp[1]
	
	return (numberOfMessagesRead, numberOfBytesRead)
	
def main():
	#print(len(sys.argv))
	#print(sys.argv)
	
	if len(sys.argv) != 2:
		print("[Server] usage: server.py option [TCP/UDP]")
		return 
	option = sys.argv[1]	
	(numberOfMessagesRead, numberOfBytesRead) = serverStreaming(option)
	print("[Server]Protocol used:{}\n  number of messages read:{} \n number of bytes reads: {}".format(option, numberOfMessagesRead, numberOfBytesRead))
  
  
  
if __name__== "__main__":
  main()

