import socket # importeer socket

#https://realpython.com/python-sockets/


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # maak een socket die s heet AF_INET is ipv4 en sockstream het TCP protocol voor het sturen van berichten
s.bind((socket.gethostbyname(socket.gethostname()), 5555)) # maakt de server op het ip van de computer dat hij opvraagt met socket.gethostbyname(socket.gethostname() met poort 5555


s.listen(2) # luisterd naar maximaal 2 clienten

print('server created')


client, addr = s.accept() # wacht tot client met server verbinding maakt en maakt hem client en slaat adres op als addr
print('client1 connected')
client2, addr2 = s.accept() # wacht tot tweede client met server verbinding maakt en maakt hem client2 en slaat adres op als addr2
print('client2 connected') 

message = 'start'
message = message.encode() # maakt bytes van string start
client.send(message) # stuurt bericht naar client
client2.send(message) # stuurt bericht naar client2

while True: # herhaalt het ontvangen en sturen van data
    data = client.recv(4096) # wacht tot client iets stuurt met een maximum van 4096 bytes naar de server en maakt dat data 
    client2.send(data) # stuurt data naar client2
    data = client2.recv(4096) # wacht tot client2 iets stuurt met een maximum van 4096 bytes naar de server en maakt dat data 
    client.send(data) # stuurt data naar client1
    


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

