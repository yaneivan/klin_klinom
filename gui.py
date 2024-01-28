from tkinter import *
from pydub import AudioSegment
from pydub.playback import play
from os.path import join as j

def show_gui(p):
	window = Tk()
	window.title("Klin Klinom")

	lbl = Label(window, text='Всем привет🤠', font = ("Arial Bold",20))
	lbl.grid(column=0, row=0)

	#txt = Entry(window, width=0)
	txt = Text(window, height=15, width=150, wrap=WORD, bg='rosybrown1', fg='black',
		font=('Times New Roman', 14))
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
		#global txt, p
		txt.insert(END, p.GetNextLine()['text'])
		check_buttons()

	def click_next_button():
		#global txt, p
		p.Set_text(txt.get('1.0', END))
		txt.delete('1.0', 'end')
		txt.insert(END, p.GetNextLine()['text'])
		check_buttons()

	def click_previous_button():
		#global txt, p 
		p.Set_text(txt.get('1.0', END))
		txt.delete('1.0', 'end')
		txt.insert(END, p.GetPreviousLine()['text'])
		check_buttons()

	def finish():
		#global p, done_btn
		p.Set_text(txt.get('0.0', END))
		p.ExportText()

		

	def play_audio():
		#segment = AudioSegment.from_mp3( j('tmp', str(p.marker_pos-1) + '.mp3') )
		#play(segment)
		play(p.GetCurrentPart())




	next_btn = Button(window, text="Show next phrase", command=click_next_button)
	next_btn.grid(column=0, row=2, pady=5) 

	previous_btn = Button(window, text="Show previous phrase", command=click_previous_button)
	previous_btn.grid(column=0, row=3, pady=5)

	play_btn = Button(window, text="Play audio", command=play_audio)
	play_btn.grid(column=0, row=4, pady=5)

	done_btn = Button(window, text="Finish and export", command=finish)
	done_btn.grid(column=0, row=5, pady=20)



	#click_next_button() ##replace with inint
	init_text()

	window.geometry('1100x520')

	for c in range(4):
		window.columnconfigure(index=c, weight=2)

	window.mainloop()

