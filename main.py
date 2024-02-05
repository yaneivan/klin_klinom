from audio import *
from gui import *
from time import sleep
import argparse


parser = argparse.ArgumentParser(
	prog='KlinKlinom',
	description='This programm will help you exctract conversations from audio file',
	epilog='Da.')
parser.add_argument('filepath')
parser.add_argument('-m', '--model')
parser.add_argument('-r', '--remote')
parser.add_argument('-k', '--keep')
parser.add_argument('-l', '--load')

args = parser.parse_args()

def process(args):
	if args.remote == 'local':
		p = AudioParser(args.filepath, args.model, args.keep, args.load)
		p.Transcribe()
		if p.transcribtion == []:
			raise RuntimeError("Answer from server was empty, probably this file wasnt processed earlier.")
		p.CutItUp()

	if args.remote == 'remote':
		import socket
		import pickle

		p = AudioParser(args.filepath, args.model, args.keep, args.load)

		#вместо Transcribe в этом варианте это должен делать сервер
		sock = socket.socket()
		#sock.connect(('31.10.64.20', 8080))
		sock.connect(('localhost', 8080))

		data = pickle.dumps(p)
		msg_len = len(data)
		sock.sendall(msg_len.to_bytes(16, byteorder='big') + data)
		print("probably sent", msg_len, "bytes, that's all, sleeping")

		sleep(3)


	#############################################################
		print('receiving')
		data = []
		header = sock.recv(16)
		msg_len = int.from_bytes(header, byteorder='big')
		print('receiving', msg_len, 'bytes')
		bytes_recd = 0
		while bytes_recd < msg_len:
		    packet = sock.recv(min(msg_len - bytes_recd, 1024))
		    if not packet:
		        raise RuntimeError("No packet error")
		    
		    data.append(packet)
		    bytes_recd += len(packet)
	#############################################################

		sock.close()

		print("all recieved, loading original file.")
		p = pickle.loads(b"".join(data))
		if p.transcribtion == []:
			raise RuntimeError("Answer from server was empty, probably this file wasnt processed earlier.")
		p.CutItUp()

		if args.keep == 'yes':
			p.Save()

	return p


'''def load(args):
	p = AudioParser(args.filepath, args.model)


	if p.Load():
		print('Ура чето загрузилось')
		return p
	else:
		raise Exception('Ниче не загрузилось вообще ниче блин')

	


if args.load == 'yes':
	p = load(args)
elif args.load == 'no':
	p = process(args)
'''

p = process(args)

show_gui(p)
#from gui import *