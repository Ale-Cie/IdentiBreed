import matplotlib.pyplot as plt

from resources import app_funcs

from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PredictionImage(Label):
    def __init__(self, parent):
        Label.__init__(self, parent, height=200, width=400)
        self.figure, self.axs = plt.subplots(1, 2, figsize=(4, 2.5))
        self.image_frame = ttk.Frame(self)
        self.image_frame.grid(column=0, row=0)
        self.parent = parent
        self.startup_image = PhotoImage(file="./resources/images/banner_color.png")
        startup_display = ttk.Label(self.image_frame, image=self.startup_image)
        startup_display.grid(column=0, row=0)

    def display(self, predicted_list, idx=0):
        self.figure, self.axs = plt.subplots(1, 2, figsize=(4, 2.5))
        self.label_string = ""
        figure, breed, accuracy = app_funcs.show_user_images(predicted_list, self.figure, self.axs, idx)
        self.image_frame.destroy()
        self.image_frame = ttk.Frame(self)
        self.image_frame.grid(column=0, row=0)
        prediction_image = FigureCanvasTkAgg(figure, self.image_frame)
        prediction_image.get_tk_widget().grid(column=0, row=0)
        if self.save_variable and idx not in self.saved_idxs:
            label_string = app_funcs.image_saver(
                image= figure, 
                breed_label= breed, 
                accuracy= accuracy
            )
            self.saved_idxs.append(idx)
            self.saved_label_texts.append(label_string)
            self.label_string = label_string
        elif idx in self.saved_idxs:
            label_string = self.saved_label_texts[idx]
        else:
            pass
        
        try:
            return label_string
        except:
            pass

    def prediction(self, file_paths, unique_labels, model, save_variable):
        dir_list, predicted_list = app_funcs.predict_user_images(file_paths, unique_labels, model)
        self.predicted_list = predicted_list
        self.save_variable = save_variable
        self.saved_idxs = []
        self.saved_label_texts =[]
        self.display(predicted_list)
        

class NavigationFrame(LabelFrame):
    def __init__(self, parent, prediction_frame, x=0, y=0):
        LabelFrame.__init__(self, parent, text="Navigation Controls", width=200)
        self.parent = parent
        self.idx = 0
        self.y = 0
        self.previous = ttk.Button(self, text="< Prev", command=lambda: self.previous_image(prediction_frame))
        self.previous.grid(column=0, row=0, sticky=(N,S,E,W))
        self.previous.state(["disabled"])
        self.counter = ttk.Label(self, text= f"{x}/{y}")
        self.counter["anchor"] = "center"
        self.counter.grid(column=1, row=0, sticky=(N,S,E,W))
        self.next = ttk.Button(self, text= "Next >", command=lambda: self.next_image(prediction_frame))
        self.next.grid(column=2, row=0, sticky=(N,S,E,W))
        self.next.state(["disabled"])
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=3)


    def activate(self, label_string, save_variable, y, x=1):
        self.idx = 1
        self.y = y
        self.counter["text"] = f"{x}/{y}"
        self.next.state(["!disabled"])
        if save_variable:
            self.text_label = ttk.Label(self, text=label_string)
            self.text_label["anchor"] = "center"
            self.text_label.grid(column=0, row=1, columnspan=3, sticky=(N,S,E,W))

       
    def next_image(self, prediction_frame):
        label_string = prediction_frame.display(prediction_frame.predicted_list, idx=self.idx)
        try:
            self.text_label["text"] = label_string
        except:
            pass
        self.idx += 1
        if self.idx == 1:
            self.previous.state(["disabled"])
        elif self.idx == 2:
            self.previous.state(["!disabled"])
        elif self.idx == self.y:
            self.next.state(["disabled"])
        else:
            self.next.state(["!disabled"])
            self.previous.state(["!disabled"])
        self.counter["text"] = f"{self.idx}/{self.y}"
        

    def previous_image(self, prediction_frame):
        self.idx -= 1
        label_string = prediction_frame.display(prediction_frame.predicted_list, idx=self.idx-1)
        try:
            self.text_label["text"] = label_string
        except:
            pass
        if self.idx == 1:
            self.previous.state(["disabled"])
        elif self.idx == 2:
            self.previous.state(["!disabled"])
        elif self.idx == self.y:
            self.next.state(["disabled"])
        else:
            self.next.state(["!disabled"])
            self.previous.state(["!disabled"])
        self.counter["text"] = f"{self.idx}/{self.y}"

