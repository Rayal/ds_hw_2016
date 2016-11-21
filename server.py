from socket import AF_INET, SOCK_STREAM, socket

def CommitData(str):
    print str
    text_file = open("SavedData.txt",'w')
    text_file.write(str)
    text_file.close()

s = socket(AF_INET, SOCK_STREAM)
s.bind(('127.0.0.1',7777))

backlog = 0
s.listen(backlog)
print ('Server started and listening...')

client_socket,client_addr = s.accept()
recv_buffer_length = 1024
message = client_socket.recv(recv_buffer_length)
#print message
CommitData(message)
#client_socket.close()
#s.close()


