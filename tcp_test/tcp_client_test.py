from socket import AF_INET, SOCK_STREAM, socket

if __name__ == "__main__":
	print "Application started"
	s = socket(AF_INET, SOCK_STREAM)
	print "TCP Socket created"
	server_address = ("127.0.0.1", 7777)
	s.connect(server_address)
	print "Connected to %s:%d" % s.getpeername()
	print "Local endpoint bound to %s:%d" % s.getsockname()
	message = "Hello World!"*7000 + "\n"
	if s.sendall(message) == None:
		print "Send %d bytes to %s:%d"%((len(message),)+s.getpeername())
	#raw_input("Enter to terminate")
	s.close()
	print "Terminating"
