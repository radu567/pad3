import socket
import json
import collections
import queue
import xml.etree.ElementTree as ET
import xml.dom.minidom
from xml import *
from xml.dom import *


tree = ET.parse('d:\\Python\\pad3\\rezultat.xml')
root = tree.getroot()

MESSAGE_TYPE = collections.namedtuple('MessageType', ('client', 'node'))(*('client', 'node'))
lista_date = queue.Queue()

ip_tcp = '127.0.0.10'
port_tcp = 10000

# creare socket TCP ....... date utilizate pentru TCP
sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_tcp.bind((ip_tcp, port_tcp))

nodes = [('127.0.0.1', 9991), ('127.0.0.2', 9992), ('127.0.0.3', 9993), ('127.0.0.4', 9994), ('127.0.0.5', 9995),
         ('127.0.0.6', 9996)]

while True:
    sock_tcp.listen(6)
    print('socket tcp in functiune')
    clientsocket, addr = sock_tcp.accept()
    # citim datele primite !!!
    data = clientsocket.recv(1024)
    data = json.loads(data.decode('utf-8'))
    types = data.get('type')
    message = data.get('message')
    print(message)

    if types == MESSAGE_TYPE.client:
        # atribuim variabilei relatii, numarul de noduri cunoscute
        i = 0
        relatii = len(nodes)

        while i < relatii:
            # preluam prima relatie pentru a ne conecta la acest nod
            ip, port = nodes[i]
            sock_node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_node.connect((ip, port))
            # facem cererea la nod
            cerere = {
                'type': 'node',
                'message': ''
            }
            jsonobj = json.dumps(cerere).encode('utf-8')
            sock_node.send(jsonobj)

            # asteptam raspuns de la nod
            raspuns = sock_node.recv(1024)
            raspuns = json.loads(raspuns.decode('utf-8'))

            typ = raspuns.get('type')
            mess = raspuns.get('message')

            # adaugam raspunsul in lista de date
            print('raspunsul primit de la nod este : ', mess)

            # aici incepem sa lucram cu datele primite pe care trebuie sa le punem in fisier xml

            for element in root.iter('rezultat'):
                new_row = 'node' + str(i)

                adaugat = ET.SubElement(element, new_row)
                adaugat.text = mess
                adaugat.set('activ', 'yes')
                ET.dump(adaugat)

            tree.write('rezultat.xml')
            # aici se termina lucrul cu fisierul xml

            lista_date.put(mess)
            sock_node.close()
            i += 1

            # atit timp cit avem date in lista le trimitem clientului
            # pentru testare trimitem mesajul primit de la nod imediat clientului

            m = lista_date.get()
            clientsocket.send(m.encode('utf-8'))
            # print(m)   # comentat de radu

        else:
            final = 'Queue is empty'
            final = final.encode('utf-8')
            clientsocket.send(final)

            # abc = ET.dump(root).encode('utf-8')

            # clientsocket.send(abc)

    else:
        clientsocket.close()
