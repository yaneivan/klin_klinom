from tkinter import *
from tkinter import filedialog, ttk
from tkinter.filedialog import askopenfile
import subprocess


window = Tk()
window.title('Klin Launcher')
window.geometry("400x400")


lbl1 = Label(window, text="Выберите модель которая будет распозновать текст \n(от этого зависит вес модели,\n время разпознования и точность результата)")
lbl1.grid(column=0, row=0)

models = ['tiny', 'base', 'small', 'medium', 'large-v2', 'large-v3']
model_selector = ttk.Combobox(values = models)
model_selector.grid(column=0, row=1)
model_selector.current(0)



lbl2 = Label(window, text="\nВыберете файл который вы хотели бы обработать")
lbl2.grid(column=0, row=2)

path = ''
def open_file():
	global path
	path = filedialog.askopenfilename(title="Select mp3 file", filetypes=(("Mp3 Files", "*.mp3"),))
	if path == '':
		browse_button.configure(bg='red')
	elif path != '':
		browse_button.configure(bg='green')

browse_button = Button(window, text="Browse", bg='red', command=open_file)
browse_button.grid(column=0, row=3, pady=3)


lbl3 = Label(window, text='\nПопытаться обработать на сервере?')
lbl3.grid(column=0, row=4)

var = IntVar()
chk = Checkbutton(window, text='Да', variable=var)
chk.grid(column=0, row=5)


lbl4 = Label(window, text='\nСохранить результат обработки на сервере или вашем компьютере')
lbl4.grid(column=0, row=6)

keep = IntVar()
chk2 = Checkbutton(window, text='Да', variable=keep)
chk2.grid(column=0, row=7)


lbl5 = Label(window, text='\nПопытаться загрузить обработанный ранее файл?')
lbl5.grid(column=0, row = 8)

load = IntVar()
chk3 = Checkbutton(window, text='Да', variable=load)
chk3.grid(column=0, row = 9)


def confirm():
	global var, window, keep, load
	if path == '':
		raise RuntimeError("No path specified")

	if var.get() == 1:
		remote = 'remote'
	elif var.get() == 0:
		remote = 'local'

	if keep.get() == 1:
		keep = 'yes'
	elif keep.get() == 0:
		keep = 'no'

	if load.get() == 1:
		load = 'yes'
	elif load.get() == 0:
		load = 'no'

	model = model_selector.get()
	window.destroy()
	print("Command for main is:" )
	print('python', 'main.py', path, '--model', model, '--remote', remote, '--keep', keep, '--load', load)
	subprocess.run(['python', 'main.py', path, '--model', model, '--remote', remote, '--keep', keep, '--load', load])
	

confirm_btn = Button(window, text = 'Confirm', command=confirm)
confirm_btn.grid(column=0, row=10, pady=20)



window.mainloop()
