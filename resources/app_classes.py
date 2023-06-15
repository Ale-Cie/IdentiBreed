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
        self.columnconfigure(0, weight=5)
        self.rowconfigure(0, weight=3)

    def display(self, predicted_list, save_method, idx=0):
        self.figure, self.axs = plt.subplots(1, 2, figsize=(4, 2.5))
        self.label_string = ""
        self.figure, self.breed, self.accuracy = app_funcs.show_user_images(predicted_list, self.figure, self.axs, idx)
        self.image_frame.destroy()
        self.image_frame = ttk.Frame(self)
        self.image_frame.grid(column=0, row=0)
        prediction_image = FigureCanvasTkAgg(self.figure, self.image_frame)
        prediction_image.get_tk_widget().grid(column=0, row=0)
        if save_method == "all":
            self.save_image(idx)
        else:
            pass

        return self.label_string
        

    def prediction(self, file_paths, unique_labels, model):
        self.dir_list, self.predicted_list = app_funcs.predict_user_images(file_paths, unique_labels, model)
        self.saved_idxs = []
        self.saved_label_texts =[]

    def save_image(self, idx=0):
        if idx not in self.saved_idxs:
            self.label_string = app_funcs.image_saver(
                image= self.figure, 
                breed_label= self.breed, 
                accuracy= self.accuracy
            )
            self.saved_idxs.append(idx)
            self.saved_label_texts.append(self.label_string)   
        else:
            self.label_string = self.saved_label_texts[idx]
         

class NavigationFrame(LabelFrame):
    def __init__(self, parent, prediction_frame, x=0, y=0):
        LabelFrame.__init__(self, parent, text="Navigation Controls", width=200)
        self.parent = parent
        self.idx = 0
        self.y = 0
        self.prediction_frame = prediction_frame
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


    def activate(self, label_string, save_method, y):
        self.idx = 1
        self.y = y
        self.counter["text"] = f"{self.idx}/{self.y}"
        self.next.state(["!disabled"])
        self.save_method = save_method
        if save_method != "none":
            self.text_label = ttk.Label(self, text=label_string)
            self.text_label.grid(column=0, row=1, columnspan=3, sticky=(N,S,E,W))
            self.text_label["anchor"] = "center"
        
        if save_method == "manual":
            self.save_button = ttk.Button(self, text="Save Image", command=lambda: app_funcs.manual_save(self.prediction_frame.figure, self.prediction_frame.breed, self.prediction_frame.accuracy, self.idx, self.manually_saved_idxs, self.manually_saved_texts, self.text_label, self.save_button))
            self.save_button.grid(column=0, row=2, columnspan=3, sticky=(N,S,E,W))
            self.manually_saved_idxs = []
            self.manually_saved_texts = {}
            self.text_label["text"] = "Would you like to save this image?"

            

    def deactivate(self):
        self.counter["text"] = "0/0"
        self.next.state(["disabled"])
        self.previous.state(["disabled"])
        try:
            self.text_label.destroy()
            self.save_button.destroy()
        except:
            pass

       
    def next_image(self, prediction_frame): 
        label_string = prediction_frame.display(prediction_frame.predicted_list, self.save_method, idx=self.idx)
        self.idx += 1
        if self.save_method == "manual":
            if self.idx not in self.manually_saved_idxs:
                self.text_label["text"] = "Would you like to save this image?"
                self.save_button.state(["!disabled"])
            else:
                self.text_label["text"] = self.manually_saved_texts[self.idx]
                self.save_button.state(["disabled"])
        elif self.save_method == "all":
            self.text_label["text"] = label_string
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
        label_string = prediction_frame.display(prediction_frame.predicted_list, self.save_method, idx=self.idx-1)
        if self.save_method == "manual":
            if self.idx not in self.manually_saved_idxs:
                self.text_label["text"] = "Would you like to save this image?"
                self.save_button.state(["!disabled"])
            else:
                self.text_label["text"] = self.manually_saved_texts[self.idx]
                self.save_button.state(["disabled"])
        elif self.save_method == "all":
            self.text_label["text"] = label_string

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
