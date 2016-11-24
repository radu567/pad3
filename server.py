import socket
import json
import collections
import queue
from threading import Thread


MESSAGE_TYPE = collections.namedtuple('MessageType', ('client', 'node'))(*('client', 'node'))
lista_date = queue.Queue()


class Nod(object):
    def __init__(self, ip_tcp, port_tcp, data):
        self.ip_tcp = ip_tcp
        self.port_tcp = port_tcp
        self.data = data
        self.thread2 = Thread(target=self.listen_tcp)

    def listen_tcp(self):
        # creare socket TCP ....... date utilizate pentru TCP
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_tcp.bind((self.ip_tcp, self.port_tcp))

        while True:
            sock_tcp.listen(6)

            clientsocket, addr = sock_tcp.accept()
            print('socket tcp in functiune')

            data = clientsocket.recv(1024)
            data = json.loads(data.decode('utf-8'))
            types = data.get('type')

            if types == MESSAGE_TYPE.node:
                info = self.data.encode('utf-8')
                clientsocket.send(info)
                print('am trimis nodului principal mesajul meu')
            else:
                clientsocket.close()

    def run(self):
        self.thread2.start()

    def stop(self):
        self.thread2.join()


# initiem nodurile
node1 = Nod('127.0.0.1', 9991, 'node1')
node2 = Nod('127.0.0.2', 9992, 'node2')
node3 = Nod('127.0.0.3', 9993, 'node3')
node4 = Nod('127.0.0.4', 9994, 'node4')
node5 = Nod('127.0.0.5', 9995, 'node5')
node6 = Nod('127.0.0.6', 9996, 'node6')

nodes = [node1, node2, node3, node4, node5, node6]

for node in nodes:
    node.run()

for node in nodes:
    node.stop()
