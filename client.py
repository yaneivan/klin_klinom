import socket
import pickle

from tkinter import *
from audio import *
from time import sleep
from pydub import AudioSegment
from pydub.playback import play
from os.path import join as j

from time import sleep

p = AudioParser('audio\\short.mp3', 'large')

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
txt = Text(window, height=10, width=80, wrap=WORD, bg='rosybrown', fg='white')
txt.grid(column=0, row=1)
txt.focus()

def check_buttons():
	if p.marker_pos >= p.length:
		next_btn["state"] = DISABLED
		done_btn["state"] = NORMAL
	else:
		next_btn["state"] = NORMAL
		done_btn["state"] = DISABLED

	if p.marker_pos <= 1:
		previous_btn["state"] = DISABLED
	else:
		previous_btn["state"] = NORMAL


def init_text():
	global txt, p
	txt.insert(END, p.GetNextLine()['text'])
	check_buttons()

def click_next_button():
	global txt, p
	p.Set_text(txt.get('1.0', END))
	txt.delete('1.0', 'end')
	txt.insert(END, p.GetNextLine()['text'])
	check_buttons()

def click_previous_button():
	global txt, p 
	#p.Set_text(txt.get('0.0', END))
	txt.delete('0.0', 'end')
	txt.insert(END, p.GetPreviousLine()['text'])
	check_buttons()

def finish():
	global p, done_btn
	p.Set_text(txt.get('0.0', END))
	p.ExportText()

	

def play_audio():
	segment = AudioSegment.from_mp3( j('tmp', str(p.marker_pos-1) + '.mp3') )
	play(segment)


next_btn = Button(window, text="Show next phrase", command=click_next_button)
next_btn.grid(column=0, row=2) 

previous_btn = Button(window, text="Show previous phrase", command=click_previous_button)
previous_btn.grid(column=0, row=3)

play_btn = Button(window, text="Play audio", command=play_audio)
play_btn.grid(column=0, row=4)

done_btn = Button(window, text="Finish and export", command=finish)
done_btn.grid(column=0, row=5)



#click_next_button() ##replace with inint
init_text()

window.geometry('700x500')

for c in range(4):
	window.columnconfigure(index=c, weight=2)

window.mainloop()

