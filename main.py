from tkinter import *
from audio import *
from time import sleep
from pydub import AudioSegment
from pydub.playback import play
from os.path import join as j

#Всем привет!
#Начинаю это писать ровно в новый год, но это совпадение.
#Первый раз я пришу чето реально для людей, поэтому придется разбираться с интерфейсом. Думал сначала про Qt, потому что с английского это перевиодится как "милашка", но эта штука выдала ошибку когда я попытался хело ворлд написать. Ну то так начинает разговор? Поэтому tkinter. Надеюсь доделаю, идея нравится.

p = AudioParser('audio\\short.mp3', 'tiny')
p.Transcribe()
p.CutItUp()
# 'large' еще есть



window = Tk()

lbl = Label(window, text='Всем привет🤠', font = ("Arial Bold",20))
lbl.grid(column=0, row=0)

#txt = Entry(window, width=0)
txt = Text(window, height=15, width=150, wrap=WORD, bg='rosybrown', fg='white')
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

window.geometry('1100x400')

for c in range(4):
	window.columnconfigure(index=c, weight=2)

window.mainloop()

