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
parser.add_argument('--load_tmp')

args = parser.parse_args()

def process(args):
	import pickle
	if args.load_tmp == 'yes':
		with open('tmp_save.pickle', 'rb') as file:
			p = pickle.load(file)
		return p


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
		sock.connect(('31.10.64.20', 8080))
		#sock.connect(('localhost', 8080))

		data = pickle.dumps(p)
		msg_len = len(data)
		sock.sendall(msg_len.to_bytes(16, byteorder='big') + data)
		print("Sending about", msg_len//1024//1024, "MBytes, that's all, sleeping for now")

		#sleep(3)


	#############################################################
		print('Waiting for response from server')
		data = []
		header = sock.recv(16)
		msg_len = int.from_bytes(header, byteorder='big')
		print('Receiving', msg_len//1024//1024, 'MBytes')
		bytes_recd = 0
		while bytes_recd < msg_len:
			print("Downloading...", round((bytes_recd/msg_len)*100), "%", end='\r')
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