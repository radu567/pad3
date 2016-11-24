import socket
import json

ip_tcp = '127.0.0.10'
port_tcp = 10000

sock_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_TCP.connect((ip_tcp, port_tcp))

# efectuam cererea la nod
cerere = {
    'type': 'client',
    'message': ''
}
jsonobj = json.dumps(cerere).encode('utf-8')
sock_TCP.send(jsonobj)

datas = sock_TCP.recv(1024)

while datas:
    # mesajul de cerere
    datas = datas.decode('utf-8')
    print(datas)
    datas = sock_TCP.recv(1024)

sock_TCP.close()
