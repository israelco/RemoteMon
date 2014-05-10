import socket
import threading
import Queue
import time
import sys
from httperfpy import Httperf
from optparse import OptionParser
import matplotlib.pyplot as plt


def httperf(server, uri, ncons, rate):
	while run:
		perf = Httperf(server=server, uri=uri, num_conns=ncons, rate=rate)
		perf.parser = True
		results = perf.run()
		q.put(results["connection_time_avg"] + " is avg")
		responseTime.append(float(results["connection_time_avg"]))

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
	print "Receiving Data"
	while connected:
		tcp.sendall("HELLO")
		msg = tcp.recv(1024)
		CPU = msg[:msg.index("|")]
		#print "CPU", CPU
		cpu.append(float(CPU))
		MEMORIA = msg[msg.index("|")+1:]
		#print "Memory", MEMORIA
		memory.append(float(MEMORIA))
		time.sleep(1)
   		



if __name__ == '__main__':

	parser = OptionParser()
	parser.add_option("--server", dest="server",help="Servidor Destino")
	parser.add_option("--uri", dest="uri",help="Endereco Destino")
	parser.add_option("--nunConns", dest="nunConns",help="Numero de Conexoes")
	parser.add_option("--rate", dest="rate",help="Numero de Conexoes Simultaneas")
	
	(options, args) = parser.parse_args()	
	server = str(options.server)
	uri = str(options.uri)
	nunConns = int(options.nunConns)
	rate = int(options.rate)
	
	#Variables to control loops
	run = True


	#Variables for the generation of graphics
	responseTime=[]
	cpu=[]
	memory=[]
	
	#Threads for monitoring response time
	q=Queue.Queue()
	LeituraTempoResposta=threading.Thread(target=httperf,args=(server,uri,nunConns,rate))
	LeituraTempoResposta.start()
	#PrintTempoResposta=threading.Thread(target=PrintResults)
	#PrintTempoResposta.start()
	
	global connected
	connected = True
	
	#Threads for remote monitoring
	monitoramento=threading.Thread(target=MonSocket,args=('127.0.0.1',10000,))
	monitoramento.setDaemon(True)
	monitoramento.start()
	
	try:
		while run:
			time.sleep(1)
	except KeyboardInterrupt:
		connected = False
		run = False

			#Graf 1 - CPU/MEMORY
		plt.figure(1)
		plt.xlabel("Tempo")
		plt.ylabel("Response Time")
		plt.plot(responseTime)
		

		#Graf 1 - CPU/MEMORY
		plt.figure(2)
		plt.subplot(211)
		plt.ylabel("CPU")
		plt.plot(cpu)
		plt.subplot(212)
		plt.ylabel("Memoria")
		plt.plot(memory)
		plt.show()
		pass

		

