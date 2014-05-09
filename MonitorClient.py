import socket
import threading
import Queue
import time
from httperfpy import Httperf
from optparse import OptionParser


def httperf(server, uri, ncons, rate):
	while run:
		perf = Httperf(server=server, uri=uri, num_conns=ncons, rate=rate)
		perf.parser = True
		results = perf.run()
		q.put(results["connection_time_avg"] + " is avg")


def PrintResults():
	while run:
		print "Response Time : \n", q.get()

def MonSocket(host, port):
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print "Connecting ", host, port
	orig = (host, port)
	tcp.connect(orig)
	time.sleep(1)
	print "Connected"
	global connected
	while connected:
		print "Will send Hello"
		tcp.sendall("HELLO")
		msg = tcp.recv(1024)
		CPU = msg[:msg.index("|")]
		print "CPU", CPU
		MEMORIA = msg[msg.index("|")+1:]
		print "Memoria", MEMORIA
		time.sleep(1)
   	



if __name__ == '__main__':

	parser = OptionParser()
	parser.add_option("--server", dest="server",help="Servidor Destino")
	parser.add_option("--uri", dest="uri",help="Endereco Destino")
	parser.add_option("--nunConns", dest="nunConns",help="Numero de Conexoes")
	parser.add_option("--rate", dest="rate",help="Numero de Conexoes Simultaneas")
	
	#Variaveis de controle recebem os valores indicados nos parametros de inicializacao
	(options, args) = parser.parse_args()	
	server = str(options.server)
	uri = str(options.uri)
	nunConns = int(options.nunConns)
	rate = int(options.rate)
	
	run = True
	
	#Threads para o monitoramento de Tempo de resposta
	q=Queue.Queue()
	LeituraTempoResposta=threading.Thread(target=httperf,args=(server,uri,nunConns,rate))
	LeituraTempoResposta.start()
	PrintTempoResposta=threading.Thread(target=PrintResults)
	PrintTempoResposta.start()

	connected = True
	global connected
	monitoramento=threading.Thread(target=MonSocket,args=('127.0.0.1',10000,))
	monitoramento.setDaemon(True)
	monitoramento.start()
	#MonSocket('127.0.0.1',10000)

	try:
		while 1:
			time.sleep(0.1)
	except KeyboardInterrupt:
		connected = False
		run = False


