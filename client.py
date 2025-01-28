import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.101", 5555))

print('connected')

while True:
    try:
        message = 'e'
        message = message.encode()
        s.send(message)

        data = s.recv(4096)
        data = data.decode('utf-8')
        print(data)
    except Exception as e:
        print(e)
        

