import socket
import psutil

HOST = '127.0.0.1' # Endereco IP do Servidor
PORT = 10000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.bind(dest)
tcp.listen(1)
print "Waiting Connections..."
con,addr = tcp.accept()
print "Connection from  ",addr
print "Sending Data"
while 1:
	#print 'Para sair use CTRL+X\n'
	rcv = con.recv(5)
	cpu = str(psutil.cpu_percent(interval=1))
	memoria = str(psutil.phymem_usage().percent)
	msg = cpu + "|" + memoria
	con.sendall(msg)

tcp.close()