import socket
import pickle

from tkinter import *
from audio import *
from time import sleep
from pydub import AudioSegment
from pydub.playback import play
from os.path import join as j

from time import sleep

p = AudioParser('audio\\audio.mp3', 'large')

#вместо Transcribe в этом варианте это должен делать сервер
sock = socket.socket()
sock.connect(('31.10.64.20', 8080))
#sock.connect(('localhost', 8080))
#sock.settimeout(3)


data = pickle.dumps(p)

'''
print('data len', len(data))
num_parts = ((len(data)+16)//1024)
if (len(data)+16)%1024!=0: num_parts+=1
sock.sendall(num_parts.to_bytes(16, byteorder='big') + data)
'''

msg_len = len(data)
sock.sendall(msg_len.to_bytes(16, byteorder='big') + data)

#sock.send(b'0')
print("probably sent", msg_len, "bytes, that's all, sleeping")

#sock.shutdown(True)
sleep(3)
#sock.shutdown(False)

print('receiving')
###########################################################
###########################################################
###########################################################

data = []
header = sock.recv(16)
target_packet_count = int.from_bytes(header, byteorder='big')
print('target_packet_count', target_packet_count)
packet_count = 0
while True:
#for i in range(target_packet_count):
    #print("true, continuing")
    packet = sock.recv(1024)
    #print("caught something!")
    if not packet:
        break
    else:
        #print("Packet numero", packet_count, "recieved successfully! ")
        packet_count += 1
    data.append(packet)

sock.close()

print(packet_count, "pacets received, loading original file.")
p = pickle.loads(b"".join(data))

p.CutItUp()
# 'large' еще есть



window = Tk()

lbl = Label(window, text='Всем привет🤠', font = ("Arial Bold",20))
lbl.grid(column=0, row=0)

#txt = Entry(window, width=0)
txt = Text(window, height=10, width=60, wrap=WORD, bg='rosybrown', fg='white')
txt.grid(column=0, row=1)
txt.focus()

count = 0
def click_button():
	global txt, gen_p, p, count
	count += 1
	txt.delete('1.0', 'end')
	txt.insert(END, next(gen_p)['text'])
	if count == p.length:
		btn["state"] = DISABLED


def play_audio():
	global count
	segment = AudioSegment.from_mp3( j('tmp', str(count-1) + '.mp3') )
	play(segment)

gen_p = p.NextLineGenerator()
btn = Button(window, text="Show next phrase", command=click_button)
btn.grid(column=0, row=2) 

play_btn = Button(window, text="Play audio", command=play_audio)
play_btn.grid(column=0, row=3)



click_button()

window.geometry('500x700')

for c in range(4):
	window.columnconfigure(index=c, weight=1)

window.mainloop()








