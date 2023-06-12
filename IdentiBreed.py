import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import subprocess

from resources import model_funcs, user_funcs, app_funcs, app_classes

from IPython.display import Image
from sklearn.model_selection import train_test_split
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import PIL.Image
import PIL.ImageTk
from tkinter import *
from tkinter import ttk


unique_labels = model_funcs.unique_labels_maker("./data/labels.csv")
identibreed = model_funcs.load_model("./models/20230511-14531683809630-full-image-set-MobileNetV2-Adam-v2.h5")

root = Tk()
root.title("IdentiBreed v. 0.1")
root.iconbitmap("./resources/images/AppIcon.icns")

# Frames
mainframe = ttk.Frame(root,width=700, height=500)
sidebar = ttk.Frame(mainframe, width=200)
display = ttk.Frame(mainframe, width=200)
io_frame = LabelFrame(sidebar, text="User Images Input/Output", width=200, height=100)
make_predictions_frame = LabelFrame(sidebar, text="Predict Breeds", height=50, width=200)
prediction_frame = app_classes.PredictionImage(display)
navigation_frame = app_classes.NavigationFrame(sidebar, prediction_frame)


# Widgets
folders_label = ttk.Label(io_frame, text="Press on one of the buttons below to open either folder", justify="center")
folders_label["anchor"] = "center"
input_folder = ttk.Button(io_frame, text="Input Folder", width=10, command=lambda: app_funcs.open_directory("input"))
output_folder = ttk.Button(io_frame, text="Output Folder", width=10, command=lambda: app_funcs.open_directory("output"))
save_variable = BooleanVar()
save_variable.set(False)
save_check = ttk.Checkbutton(io_frame, text="Save predictions to the output folder?", variable=save_variable, onvalue=True, offvalue= False) 
predict_label = ttk.Label(make_predictions_frame, text="Press to make predictions")
predict_label["anchor"] = "center"
predict_button = ttk.Button(make_predictions_frame, text="Make Predictions", command=lambda: (prediction_frame.prediction("./user/input", unique_labels, identibreed, save_variable.get()), navigation_frame.activate(prediction_frame.label_string, save_variable.get(), len(prediction_frame.predicted_list)), save_check.state(["disabled"])))
predict_spacer = ttk.Label(make_predictions_frame)

# Grid settings
mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
sidebar.grid(column=0, row=1, columnspan=2)
display.grid(column=0, row=0, columnspan=2)
io_frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
make_predictions_frame.grid(column=3, row=0, columnspan=3, sticky=(N, E, W))
navigation_frame.grid(column=0, row=2, columnspan=6, sticky=(N, S, E, W))

prediction_frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
folders_label.grid(column=0, row=0, columnspan=2, sticky=(N, S, E, W))
input_folder.grid(column=0, row=1, sticky=(N, S, E, W))
output_folder.grid(column=1, row=1, sticky=(N, S, E, W))
save_check.grid(column=0, row=2, sticky=(N, S, E, W), columnspan=2)
predict_label.grid(column=0, row=0, columnspan= 3, sticky=(N,S,E,W))
predict_button.grid(column=0, row=1, columnspan=3, sticky=(N,S,E,W))
predict_spacer.grid(column=0, row=2, columnspan=3)



# Column & row configure settings
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=3)
mainframe.columnconfigure(3, weight=3)
sidebar.columnconfigure(0, weight=3)
sidebar.columnconfigure(1, weight=3)
display.columnconfigure(0, weight=3)
io_frame.columnconfigure(0, weight=3)
io_frame.columnconfigure(1, weight=3)
make_predictions_frame.columnconfigure(0, weight=3)
navigation_frame.columnconfigure(0, weight=3)
navigation_frame.columnconfigure(1, weight=3)
navigation_frame.columnconfigure(2, weight=3)
prediction_frame.columnconfigure(0, weight=3)

button_list = []


for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()

