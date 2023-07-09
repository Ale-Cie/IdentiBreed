from resources import model_funcs, app_funcs, app_classes

from pyautogui import size

import PIL.Image
import PIL.ImageTk
import time
from tkinter import *
from tkinter import ttk


unique_labels = model_funcs.unique_labels_maker("./data/labels.csv")
identibreed = model_funcs.load_model("./models/20230511-14531683809630-full-image-set-MobileNetV2-Adam-v2.h5")
app_version = "0.3.0"

root = Tk()
root.title(f"IdentiBreed v. {app_version}")
root.iconbitmap("./resources/images/AppIcon.icns")

# Variables
save_method = StringVar()
width, height = size()
width_multiplier = int(width)/1440
height_multiplier = int(height)/900
config_dict = app_funcs.config_reader(app_version)

# Frames
mainframe = ttk.Frame(root,width=1090, height=900)
sidebar = ttk.Frame(mainframe, width=500)
display = ttk.Frame(mainframe, width=200)
input_source_frame = app_classes.InputSource(sidebar)
make_predictions_frame = LabelFrame(sidebar, text="Predict Breeds", height=50, width=200)
save_method_frame = LabelFrame(sidebar, text="Select Save Method")
prediction_frame = app_classes.PredictionImage(display)
navigation_frame = app_classes.NavigationFrame(sidebar, prediction_frame)


# Test Button - Use only when experimenting with new functions!!
# test_button = ttk.Button(sidebar, text="Test", command=lambda: print(navigation_frame.evaluation_frame.log_file))
# test_button.grid(column=7, row=0)

# Widgets
predict_label = ttk.Label(make_predictions_frame, text="Press to make predictions...")
predict_label["anchor"] = "center"
save_method_label = ttk.Label(save_method_frame, text="Please select the saving method")
save_method_label["anchor"] = "center"
save_all_button = ttk.Button(save_method_frame, text="Save All", state=["disabled"], command= lambda: app_funcs.save_button_command(save_method, "all", width_multiplier, height_multiplier, [save_all_button, save_none_button, save_manually_button], prediction_frame, navigation_frame, predict_label))
save_none_button = ttk.Button(save_method_frame, text="Save None", state=["disabled"],command= lambda: app_funcs.save_button_command(save_method, "none", width_multiplier, height_multiplier, [save_all_button, save_none_button, save_manually_button], prediction_frame, navigation_frame, predict_label))
save_manually_button = ttk.Button(save_method_frame, text="Select Manually", state=["disabled"], command= lambda: app_funcs.save_button_command(save_method, "manual", width_multiplier, height_multiplier, [save_all_button, save_none_button, save_manually_button], prediction_frame, navigation_frame, predict_label))
save_separator = ttk.Separator(save_method_frame, orient="horizontal")
output_folder_label = ttk.Label(save_method_frame, text="Saved Images Directory")
output_folder_label["anchor"] = "center"
output_folder = ttk.Button(save_method_frame, text="Output Folder", width=10, command=lambda: app_funcs.open_directory("output"))
predict_button = ttk.Button(make_predictions_frame, text="Make Predictions", default="active", command=lambda: app_funcs.predict_button_command(input_source_frame, save_method, prediction_frame, unique_labels, identibreed, predict_label, [save_all_button, save_none_button, save_manually_button], navigation_frame, sidebar, app_version))

# Grid settings
mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
display.grid(column=0, row=0, columnspan=2)
sidebar.grid(column=0, row=1, columnspan=2)
input_source_frame.grid(column=0, row=0, sticky=(N,S,E,W))
make_predictions_frame.grid(column=1, row=0, columnspan=3, sticky=(N, S, E, W))
navigation_frame.grid(column=0, row=2, columnspan=2, sticky=(N, S, E, W))
prediction_frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
predict_label.grid(column=0, row=0, columnspan= 3, sticky=(N,S,E,W))
predict_button.grid(column=0, row=1, columnspan=3, sticky=(N,S,E,W))
save_method_frame.grid(column= 0, row= 1, columnspan=4, sticky=(N,S,E,W))
save_method_label.grid(column= 0, row= 0, columnspan=3, sticky=(N,S,E,W))
save_all_button.grid(column= 0, row= 1, sticky=(N,S,E,W))
save_none_button.grid(column= 1, row= 1, sticky=(N,S,E,W))
save_manually_button.grid(column= 2, row= 1, sticky=(N,S,E,W))
output_folder_label.grid(column=4, row=0, sticky=(N,S,E,W))
save_separator.grid(column=3, row=0, rowspan=2, sticky=(N,S,E,W))
output_folder.grid(column=4, row=1, sticky=(N,S,E,W))



# Column & row configure settings
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=3)
mainframe.rowconfigure(0, weight=3)
mainframe.rowconfigure(1, weight=3)
sidebar.columnconfigure(0, weight=3)
sidebar.columnconfigure(1, weight=3)
display.columnconfigure(0, weight=3)
make_predictions_frame.columnconfigure(0, weight=3)
save_method_frame.columnconfigure(0, weight=3)
save_method_frame.columnconfigure(1, weight=3)
save_method_frame.columnconfigure(2, weight=3)
navigation_frame.columnconfigure(0, weight=3)
navigation_frame.columnconfigure(1, weight=3)
navigation_frame.columnconfigure(2, weight=3)
prediction_frame.columnconfigure(0, weight=3)

frames = [mainframe, sidebar, make_predictions_frame, save_method_frame, navigation_frame]
for frame in frames:
    if frame == make_predictions_frame:
        for child in frame.winfo_children():
            child.grid_configure(padx=3, pady=15)
    else:
        for child in frame.winfo_children():
            child.grid_configure(padx=3, pady=2)

root.minsize(width=int(round(1090*width_multiplier)), height=int(round(450*height_multiplier)))
root.maxsize(width=int(round(1090*width_multiplier)), height=int(round(900*height_multiplier)))

root.mainloop()



