from socket import AF_INET, SOCK_STREAM, socket

from time import sleep

from os import getpid

print __name__

if __name__ == "__main__":
	print "App started"
	print "Process ID: %d" % getpid()
	s = socket(AF_INET, SOCK_STREAM)
	print "TCP Socket created"
	print "File descriptor: ", s.fileno()
	s.bind(("127.0.0.1", 7777))
	print "Socket bound to %s:%d" % s.getsockname()
	backlog = 1
	s.listen(backlog)
	print "Listening."
	client_socket, client_addr = s.accept()
	print "New client from %s:%d" % client_addr
	print "Local endpoint socket bound on %s:%d" % client_socket.getsockname()
	buf_len = 1024
	message = ""
	while not message.endswith("\n"):
		m = client_socket.recv(buf_len)
		print "Received block size %d" % len(m)
		message += m
	#print "Received messag:\n%s" % message
	raw_input("Press Enter to terminate.")
	client_socket.close()
	s.close()
	print "Terminating"
