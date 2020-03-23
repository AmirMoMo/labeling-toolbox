import os
import glob
import numpy as np
import tkinter as tk
from PIL import Image
from random import shuffle
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define an image index:
image_idx = 0

# Define the GUI
root = tk.Tk()
canvas1 = tk.Canvas(root, width=1200, height=500)
canvas1.pack()

label1 = tk.Label(root, text='QualitAI Labeling GUI')
label1.config(font=('Arial', 40))
canvas1.create_window(600, 50, window=label1)

entry1 = tk.Entry(root, font=('Arial', 25))
canvas1.create_window(600, 110, window=entry1)

entry2 = tk.Entry(root, font=('Arial', 25),)
canvas1.create_window(600, 170, window=entry2)

# Reading the results txt file:
def read_results():
    global results_dir
    results_dictionary = {}
    with open(os.path.join(results_dir, 'labeling_results.txt'), 'r') as file:
        for item in file.readlines():
            filename = item.split(' ')[0]
            label = int(item.split(' ')[1].replace('\n', ''))
            results_dictionary[filename] = label
    return results_dictionary

# Initializing the GUI
def start():
    global image_idx
    global data_dir
    global results_dir
    global list_of_images
    global labels
    global results_dictionary
    data_dir = str(entry1.get())
    results_dir = str(entry2.get())
    list_of_images = glob.glob(os.path.join(*[data_dir, '*', '*', '*.png']))
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
        results_dictionary = dict(zip([], []))
    else:
        results_dictionary = read_results()
        list_of_labeled_images = list(results_dictionary.keys())
        list_of_images = [item for item in list_of_images if not os.path.split(item)[-1] in list_of_labeled_images]
    shuffle(list_of_images)
    list_of_images += [os.path.join('.', 'good_job.jpg')]
    labels = list(-np.ones(len(list_of_images)))
    print(image_idx)
    if image_idx == 0:
        show_next(False)

# Labeling actions
def label_as_good():
    global labels
    global image_idx
    try:
        labels[image_idx] = 0
        results_dictionary[os.path.split(list_of_images[image_idx])[-1]] = 0
    except:
        root.destroy
    print('Labeled as good')
    image_idx += 1
    show_next()

def label_as_possible():
    global labels
    global image_idx
    global list_of_images
    global results_dictionary
    try:
        labels[image_idx] = 1
        results_dictionary[os.path.split(list_of_images[image_idx])[-1]] = 1
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
        results_dictionary[os.path.split(list_of_images[image_idx])[-1]] = 2
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
    if not image_idx > len(list_of_images)-1:
        #if len(list_of_images)>0:
        #    save_labels()
        #else:
        if clear:
            bar1.get_tk_widget().pack_forget()
            save_labels()
        figure, axes = plt.subplots(figsize=(25, 16), dpi=100)
        bar1 = FigureCanvasTkAgg(figure, root)
        axes.imshow(np.array(Image.open(list_of_images[image_idx])))
        axes.axis('off')
        bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        print('Show next', image_idx, '/', len(list_of_images))

# Labeled the images and save the labels:
def save_labels():
    global results_dir
    global results_dictionary
    with open(os.path.join(results_dir, 'labeling_results.txt'), 'w') as file:
        for key, value in results_dictionary.items():
            file.write('{} {}\n'.format(key, value))

# Go one image back to correct possible mistakes
def previous_image():
    global image_idx
    if image_idx-2 > -1:
        image_idx -= 1
    show_next()

button0 = tk.Button(root, text='{:^15}'.format('Start'), command=start, bg='lightskyblue2', font=('Arial', 25, 'bold'))
canvas1.create_window(600, 240, window=button0)

button1 = tk.Button(root, text='{:^15}'.format('Good'), command=label_as_good, bg='green', font=('Arial', 25, 'bold'))
canvas1.create_window(200, 320, window=button1)
button2 = tk.Button(root, text='{:^15}'.format('Possible Reject'), command=label_as_possible, bg='yellow', font=('Arial', 25, 'bold'))
canvas1.create_window(600, 320, window=button2)
button3 = tk.Button(root, text='{:^15}'.format('Reject'), command=label_as_reject, bg='red',
                    font=('Arial', 25, 'bold'))
canvas1.create_window(1000, 320, window=button3)

button4 = tk.Button(root, text='{:^15}'.format('Back'), command=previous_image, bg='lightskyblue2',
                    font=('Arial', 25, 'bold'))
canvas1.create_window(400, 400, window=button4)
button6 = tk.Button(root, text='{:^15}'.format('Exit'), command=root.destroy, bg='lightskyblue2',
                    font=('Arial', 25, 'bold'))
canvas1.create_window(800, 400, window=button6)

root.mainloop()