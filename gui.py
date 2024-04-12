from tkinter import *
from pydub import AudioSegment
from pydub.playback import play
from os.path import join as j
import threading
import pickle

def show_gui(p):
	window = Tk()
	window.title("Klin Klinom")

	lbl = Label(window, text='Всем привет🤠', font = ("Arial Bold",20))
	lbl.grid(column=0, row=0)

	#txt = Entry(window, width=0)
	txt = Text(window, height=15, width=150, wrap=WORD, bg='rosybrown1', fg='black',
		font=('Times New Roman', 14))
	txt.grid(column=0, row=2)
	txt.focus()

	def check_buttons():
		print("Marker pos: ", p.marker_pos)
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
		#global txt, p
		txt.insert(END, p.GetNextLine()['text'])
		check_buttons()

	def click_next_button():
		#global txt, p


		p.Set_text(txt.get('1.0', END))
		txt.delete('1.0', 'end')
		line = p.GetNextLine()
		time = str( int ((line['start']) // 60)) + " Мин. " + str( int((line['start']) % 60)) + " с."
		lbl.config(text=time, font=("Helvetica", 14, "bold"))
		txt.insert(END, line['text'])
		check_buttons()

	def click_previous_button():
		#global txt, p 
		p.Set_text(txt.get('1.0', END))
		txt.delete('1.0', 'end')
		line = p.GetPreviousLine()
		time = str( int ((line['start']) // 60)) + " Мин. " + str( int((line['start']) % 60)) + " с."
		lbl.config(text=time, font=("Helvetica", 14, "bold"))
		txt.insert(END, line['text'])
		check_buttons()

	def finish():
		#global p, done_btn
		p.Set_text(txt.get('0.0', END))
		p.ExportText()

	

	def play_audio():
		threading.Thread( target=play,  args=[p.GetCurrentPart()] ).start()

	def tmp_save():
		with open('tmp_save.pickle', 'wb') as file:
			pickle.dump(p, file)

	tmp_save_btn = Button(window, text="Save progress", command=tmp_save)
	tmp_save_btn.grid(column=0, row=1, pady=5)

	next_btn = Button(window, text="Show next phrase", command=click_next_button)
	next_btn.grid(column=0, row=3, pady=5) 

	previous_btn = Button(window, text="Show previous phrase", command=click_previous_button)
	previous_btn.grid(column=0, row=4, pady=5)

	play_btn = Button(window, text="Play audio", command=play_audio)
	play_btn.grid(column=0, row=5, pady=5)

	done_btn = Button(window, text="Finish and export", command=finish)
	done_btn.grid(column=0, row=6, pady=20)



	#click_next_button() ##replace with inint
	init_text()

	window.geometry('1100x550')

	for c in range(4):
		window.columnconfigure(index=c, weight=2)

	window.mainloop()

