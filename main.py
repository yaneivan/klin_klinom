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
	window.columnconfigure(index=c, weight=2)

window.mainloop()

