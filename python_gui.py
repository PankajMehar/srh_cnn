

# todd@thor:~/Desktop$ sudo /home/todd/anaconda3/bin/python python_gui.py 341872

import numpy as np
import os
import sys
import keyboard

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

import shutil
from PIL import Image
from PIL.ImageTk import PhotoImage
from functools import partial

img_dir = "/home/todd/Desktop/NIO_088/lymphoma"
nondiag_dir = "/home/todd/Desktop/filter_quick_dir/nondiagnostic"	
grey_dir = "/home/todd/Desktop/filter_quick_dir/greymatter"
white_dir = "/home/todd/Desktop/filter_quick_dir/whitematter"
pseudo_dir = "/home/todd/Desktop/filter_quick_dir/pseudoprogression"

img_list = sorted(os.listdir(img_dir))
display_imgs = 144
current_img_index = 0

def move_file(image_file, dest_dir):
	# shutil.copy(src = os.path.join(img_dir, image_file), dst = os.path.join(dest_dir, image_file))
    shutil.move(src = os.path.join(img_dir, image_file), dst = os.path.join(dest_dir, image_file))

def button_press(e):

	if keyboard.is_pressed('1'):
		move_file(e, grey_dir)
		print(e + " > greymatter")

	elif keyboard.is_pressed('2'):
		move_file(e, white_dir)
		print(e + " > whitematter")

	elif keyboard.is_pressed('3'):
		move_file(e, pseudo_dir)
		print(e + " > pseudoprogression")

	else:
		move_file(e, nondiag_dir)
		print(e + " > nondiagnostic")

def load_next_batch(root):
	global current_img_index
	global display_imgs
	current_img_index += display_imgs
	print(str(img_list[current_img_index]) + ": " + str(current_img_index))
	image_batch(root)

def go_to_index(root):
	global current_img_index
	global display_imgs
	current_img_index = int(e1.get()) - display_imgs
	e1.delete(0,END)
	load_next_batch(root)

pics = list(np.repeat(None, display_imgs))  #  This will be the list that will hold a reference to each of your PhotoImages.
def image_batch(root):

	col = 0
	row = 0
	for k, image_file in enumerate(img_list[current_img_index : current_img_index + display_imgs]):
		
		width = 75
		height = 75

		img = Image.open(os.path.join(img_dir, image_file))
		img = img.resize((width, height))
		pics[k] = PhotoImage(img)
		b = Button(root, image=pics[k], width=80, height=80, command=partial(button_press, image_file))
		b.grid(column=col, row=row, sticky=(W, E))

		col += 1
		if (col % 12 == 0):
			row += 1
			col = 0

if __name__ == '__main__':

	root = Tk()
	root.title("SRH labelling GUI")
	image_batch(root)
	
	button_next = Button(root, text = "Next batch", command=partial(load_next_batch, root)).grid(column = 13, row = 0)  # Need write function for click event
	
	e1 = Entry(root)
	e1.grid(column = 13, row = 2)

	jump_to = Button(root, text = "Jump to" , command=partial(go_to_index, root)).grid(column = 13, row = 1)  # Need write function for click event

	root.mainloop()
