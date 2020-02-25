import os
import sys
import socket

localIP     = "127.0.0.1"
localPort   = 1997
bufferSize  = 65535

 
def serverStreaming(option):
	
	option = option.upper()
	if option == "TCP":
		sck = socket.SOCK_STREAM
	elif option == "UDP":
		sck = socket.SOCK_DGRAM
	else:
		print('Not a valid option for socket')
		return (0, 0)
		
	ServerSocket = socket.socket(family=socket.AF_INET, type=sck)
	ServerSocket.bind((localIP, localPort))
	if option == "TCP":
		ServerSocket.listen(1)
		conn, addr = ServerSocket.accept()
	
	#print("UDP server up and listening")
	#msgFromServer       = "Hello UDP Client"
	#bytesToSend         = str.encode(msgFromServer)

	while(True):
		if option == "TCP":
			message = ServerSocket.recv(bufferSize)
		else:
			bytesAddressPair = ServerSocket.recvfrom(bufferSize)
			message = bytesAddressPair[0]
			address = bytesAddressPair[1]
		numberOfMessagesRead = numberOfMessagesRead + 1
		numberOfBytesRead = bytesRead + len(message) 
		if message == "STOP":
			break
			
		#clientMsg = "Message from Client:{}".format(message)
		#clientIP  = "Client IP Address:{}".format(address)
		#print(clientMsg)
		#print(clientIP)
		#UDPServerSocket.sendto(bytesToSend, address)
		
	return (numberOfMessagesRead, numberOfBytesRead)
	
def main():
	#print(len(sys.argv))
	#print(sys.argv)
	
	if len(sys.argv) != 2:
		print("usage: server.py option [TCP/UDP]")
		return 
	option = sys.argv[1]	
	(numberOfMessagesRead, numberOfBytesRead) = serverStreaming(option)
	print("Protocol used:{}\n  number of messages read:{} \n number of bytes reads: {}".format(option, numberOfMessagesRead, numberOfBytesRead))
  
  
  
if __name__== "__main__":
  main()

