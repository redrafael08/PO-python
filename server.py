import socket



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostbyname(socket.gethostname()), 5555))


s.listen(2) # maximale aantal clienten

print('server created')


client, addr = s.accept()
print('client1 connected')
client2, addr2 = s.accept()
print('client2 connected')
while True:
    data = client.recv(4096)
    client2.send(data)
    data = client2.recv(4096)
    client.send(data)
    


'''
# https://stackoverflow.com/questions/38412887/how-to-send-a-list-through-tcp-sockets-python
y = [0,12,6,8,3,2,10] 
# Convert To String
y = str(y)
# Encode String
y = y.encode()
# Send Encoded String version of the List
s.send(y)
'''
'''
data = connection.recv(4096)
# Decode received data into UTF-8
data = data.decode('utf-8')
# Convert decoded data into list
data = eval(data)
'''

