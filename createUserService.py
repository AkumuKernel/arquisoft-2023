import socket
import sys
import re
from database import databaseServer

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sv_addr = ('localhost', 5000)
print(f'connecting to {sv_addr[0]} to port {sv_addr[1]}')
sock.connect(sv_addr)

db_server = databaseServer("localhost", "5432", "ArquiSoft", "postgres", "")
db_server.create_connection()

regex = re.compile(r'''((?:"[^"]*"|'[^']*'|[^"'\s])+)''')
try:
 message = b'00010sinitcrear'
 print(f'sending {message}')
 sock.sendall(message)

 a_received = 0
 a_expected = int(sock.recv(5))
 while a_received < a_expected:
  data = sock.recv(a_expected - a_received)
  a_received += len(data)
  print(f'received {data}')

 while True:
  print('Waiting for transaction')
  a_received = 0
  a_expected = int(sock.recv(5))

  while a_received < a_expected:
   data = sock.recv(a_expected - a_received)
   a_received += len(data)
   print(f'received {data}')

  print('Processing...')
  resp = '{:05d}'.format(len(data)) + data.decode()
  resp2 = resp.split('crear')
  datos = regex.findall(resp2[1])
  datos[4] = f'{datos[4]} {datos[5]}'
  print('Send answer (if needed)')
  print(f'Sending [{resp2[1]}] to database')
  success = db_server.register(datos[0], datos[1], datos[2], datos[3], datos[4])
  success = f'crear{success}'
  success = '{:05d}'.format(len(success)) + success
  sock.sendall(bytes(success, 'latin-1'))

finally:
 print('closing socket')
 sock.close()