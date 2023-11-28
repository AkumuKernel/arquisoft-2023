import socket
import sys
from database import databaseServer

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sv_addr = ('localhost', 5000)
print(f'connecting to {sv_addr[0]} to port {sv_addr[1]}')
sock.connect(sv_addr)

db_server = databaseServer("localhost", "5432", "ArquiSoft", "postgres", "")
db_server.create_connection()

try:
 message = b'00010sinitconsu'
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
  print('Send answer (if needed)')
  print(f'Sending {resp}')
  success = db_server.viewLogged()
  success = f'consu{success}'
  success = '{:05d}'.format(len(success)) + success
  sock.sendall(bytes(success, 'latin-1'))

finally:
 print('closing socket')
 sock.close()