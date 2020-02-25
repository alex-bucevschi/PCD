import os
import sys
import timeit
import socket

localIP     = "127.0.0.1"
localPort   = 1997
bufferSize  = 65535

def sendFile(file, ClientSocket):
	
	ClientSocket.send(bytearray(file, 'utf-8'))
	numberOfMessagesSent =  1
	numberOfBytesSent = len(bytearray(file, 'utf-8')) 
	f = open(file,'rb')
	message = f.read(bufferSize)
	while (message):
		ClientSocket.send(message)
		message = f.read(bufferSize)
		numberOfMessagesSent = numberOfMessagesSent + 1
		numberOfBytesSent = numberOfBytesSent + len(message) 
	f.close()
	ClientSocket.send(bytearray("[END]", 'utf-8'))
	numberOfMessagesSent = numberOfMessagesSent + 1
	numberOfBytesSent = numberOfBytesSent + len(bytearray("[END]", 'utf-8')) 
	return (numberOfMessagesSent, numberOfBytesSent)
		

def clientStreaming(option, directory):
	option = option.upper()
	
	if option == "TCP":
		sck = socket.SOCK_STREAM
	elif option == "UDP":
		sck = socket.SOCK_DGRAM
	else:
		print('[Client]Not a valid option for socket')
		return (0, 0)
	numberOfMessagesSent = 0
	numberOfBytesSent = 0
	ClientSocket = socket.socket(socket.AF_INET, sck)
	ClientSocket.connect((localIP, localPort))
	for root, dirs, files in os.walk(directory):
		for name in files:
			resp = sendFile(os.path.join(root, name), ClientSocket)
			numberOfMessagesSent = numberOfMessagesSent + resp[0]
			numberOfBytesSent = numberOfBytesSent + resp[1]
	ClientSocket.send(bytearray("[STOP]", 'utf-8'))
	numberOfMessagesSent = numberOfMessagesSent + 1
	numberOfBytesSent = numberOfBytesSent + len(bytearray("[STOP]", 'utf-8')) 
	return (numberOfMessagesSent, numberOfBytesSent)
   #data = ClientSocket.recv(BUFFER_SIZE)
   #ClientSocket.close()
  
def main():
	#print(len(sys.argv))
	#print(sys.argv)
	
	if len(sys.argv) != 2:
		print("usage: client.py option [TCP/UDP]")
		return 
	option = sys.argv[1]
	startTime = timeit.default_timer()	
	(numberOfMessagesSent, numberOfBytesSent) = clientStreaming(option, 'toSend')
	stopTime = timeit.default_timer()	
	print("Run Time: {}\nProtocol used:{}\n  number of messages sent:{} \n number of bytes sent: {}".format(stopTime- startTime, option, numberOfMessagesSent, numberOfBytesSent))
  
  
  
if __name__== "__main__":
  main()