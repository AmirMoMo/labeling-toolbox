import os
import glob
import numpy as np
import tkinter as tk
from PIL import Image
from shutil import move
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Give the location of the file
data_dir = 'data_2019_relabel/'
new_dir = 'data_2019_newlabeling/'

# Define the list of images and initialize labels
list_of_images = glob.glob(data_dir + '*/*/*.png')
labels = list(-np.ones(len(list_of_images)))
image_idx = 0

# Create new folders
if not os.path.isdir(new_dir):
    #os.makedirs(new_dir)
    #os.makedirs(new_dir + '/train')
    os.makedirs(new_dir + '/train/good')
    os.makedirs(new_dir + '/train/possible')
    os.makedirs(new_dir + '/train/bad')
    #os.makedirs(new_dir + '/valid')
    os.makedirs(new_dir + '/valid/good')
    os.makedirs(new_dir + '/valid/possible')
    os.makedirs(new_dir + '/valid/bad')

# Define the GUI
global root
root = tk.Tk()
canvas1 = tk.Canvas(root, width=1200, height=500)
canvas1.pack()

label1 = tk.Label(root, text='QualitAI Labeling GUI')
label1.config(font=('Arial', 40))
canvas1.create_window(600, 50, window=label1)

# Initializing the GUI
def start():
    global image_idx
    print(image_idx)
    if image_idx == 0:
        show_next(False)

# Labeling actions
def label_as_good():
    global labels
    global image_idx
    try:
        labels[image_idx] = 0
    except:
        root.destroy
    print('Labeled as good')
    image_idx += 1
    show_next()

def label_as_possible():
    global labels
    global image_idx
    try:
        labels[image_idx] = 1
    except:
        root.destroy
    print('Labeled as possible')
    image_idx += 1
    show_next()

def label_as_reject():
    global labels
    global image_idx
    global root
    try:
        labels[image_idx] = 2
    except:
        root.destroy
    print('Labeled as reject')
    image_idx += 1
    show_next()

# Change the image to the next one
def show_next(clear=True):
    global image_idx
    global bar1
    global list_of_images
    global root
    if image_idx > len(list_of_images)-1:
        if len(list_of_images)>0:
            save_labels()
        root.destroy
    else:
        if clear:
            bar1.get_tk_widget().pack_forget()
        figure, axes = plt.subplots(figsize=(25, 16), dpi=100)
        bar1 = FigureCanvasTkAgg(figure, root)
        axes.imshow(np.array(Image.open(list_of_images[image_idx])))
        axes.axis('off')
        bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        print('Show next', image_idx, '/', len(list_of_images))

# Move the labeled image to the new dataset
def save_labels():
    global list_of_images
    global image_idx
    global labels
    possible_labels = ['good', 'possible', 'bad']
    for i in range(len(labels)):
        if labels[i] != -1:
            dist = list_of_images[i].replace(data_dir, new_dir)
            dist_list = dist.split('/')
            dist_list[-2] = possible_labels[labels[i]]
            dist = os.path.join(*dist_list)
            move(list_of_images[i], dist)
    unlabeled = [i for i, x in enumerate(labels) if x == -1]
    labels = [labels[item] for item in unlabeled]
    list_of_images = [list_of_images[item] for item in unlabeled]
    image_idx = 0
    show_next()

# Go one image back to correct possible mistakes
def previous_image():
    global image_idx
    if image_idx-2 > -1:
        image_idx -= 2
    show_next()

button0 = tk.Button(root, text='{:^15}'.format('Start'), command=start, bg='lightskyblue2', font=('Arial', 25, 'bold'))
canvas1.create_window(600, 140, window=button0)

button1 = tk.Button(root, text='{:^15}'.format('Good'), command=label_as_good, bg='green', font=('Arial', 25, 'bold'))
canvas1.create_window(200, 220, window=button1)
button2 = tk.Button(root, text='{:^15}'.format('Possible Reject'), command=label_as_possible, bg='yellow', font=('Arial', 25, 'bold'))
canvas1.create_window(600, 220, window=button2)
button3 = tk.Button(root, text='{:^15}'.format('Reject'), command=label_as_reject, bg='red',
                    font=('Arial', 25, 'bold'))
canvas1.create_window(1000, 220, window=button3)

button4 = tk.Button(root, text='{:^15}'.format('Back'), command=previous_image, bg='lightskyblue2',
                    font=('Arial', 25, 'bold'))
canvas1.create_window(200, 300, window=button4)
button5 = tk.Button(root, text='{:^15}'.format('Save'), command=save_labels, bg='lightskyblue2',
                    font=('Arial', 25, 'bold'))
canvas1.create_window(600, 300, window=button5)
button6 = tk.Button(root, text='{:^15}'.format('Exit'), command=root.destroy, bg='lightskyblue2',
                    font=('Arial', 25, 'bold'))
canvas1.create_window(1000, 300, window=button6)

root.mainloop()