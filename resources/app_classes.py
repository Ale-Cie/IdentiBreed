import matplotlib.pyplot as plt

from resources import app_funcs

from tkinter import *
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PredictionImage(Label):
    def __init__(self, parent):
        """
        This creates a tk Label that initially shows the app logo and when predictions are made can display each figure.
        For initialization it requires only the 'parent' Frame in which it will be displayed. 
        Has to be placed in a grid manually.
        """
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

    def display(self, predicted_list, save_method, width_multiplier, height_multiplier, idx=0):
        """
        This method takes a list of predictions made on all images, a desired save method, multipliers for both width and height.
        Optionally it can be given an idx, which will show another picture from the predictions list.
        
        Replaces the IdentiBreed logo with a figure containing the subplots, one of which is the image and the other top 5 breeds.
        
        Returns 'label_string' - a string that is either empty or contains the path to saved image. 
        The 'label_string' can be used to display the path details in the navigation bar.
        """
        self.figure, self.axs = plt.subplots(1, 2)
        self.label_string = ""
        self.figure, self.breed, self.accuracy = app_funcs.show_user_images(predicted_list, self.figure, self.axs, width_multiplier, height_multiplier, idx)
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
        """
        This method takes a path to the directory containing the files, list of unique_labels and the model. 
        
        It makes predictions on the files in the directory and creates two lists - saved_idxs and saved_label_texts. 
        Those variables, when given to 'app_funcs.save_image' function and then to navigation bar prevent the app from making
        new copies of the figure in the /output folder, if it has been already saved.

        Returns 'folder_state' - string either 'empty' or 'filled', that is used to prevent app from crashing in case the user
        provided incorrect or empty path/url.
        """
        self.dir_list, self.predicted_list, folder_state = app_funcs.predict_user_images(file_paths, unique_labels, model)
        self.saved_idxs = []
        self.saved_label_texts = []

        return folder_state

    def save_image(self, idx=0):
        """
        This method saves the image under idx. 

        It first checks if the images of this idx has already been saved. If not it saves the image, then appends the 
        'saved_idxs' with the idx and the 'saved_label_texts' with the path to the saved image.
        If the particular prediction has already been saved it sets the 'label_string' to the correct path.
        """
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
        """
        This creates a tk LabelFrame that contains the navigation controls for the display and a tk Label that displays the
        counter (i.e. which image out of how many is displayed on the screen). Using other available methods the navigation
        bar can be expanded to contain a a tk Label that prints the path to the saved image and a tk Button that allows user
        to manually save desired predictions.

        It has to be given a 'parent' in which the navigation bar will be housed and a 'prediction_frame' - a PredictionImage
        object that will be used to display next and previous predictions.

        When created the buttons and counter are 'disabled' by default. They have to be activated with the '.activate()' method.
        """
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


    def activate(self, save_method, width_multiplier, height_multiplier, y, label_string=""):
        """
        This method takes a 'save_method' string, integers for width and height multiplier, 'y' which is the amount of
        predictions made and the 'label_string'. The 'label_string' is a string obtained from the PredictionImage object.
        It set to an empty string by default, but it has to be specified earlier in order to display the predicted path.
        """
        self.width_multiplier = width_multiplier
        self.height_multiplier = height_multiplier
        self.idx = 1
        self.y = y
        self.counter["text"] = f"{self.idx}/{self.y}"
        if self.y != 1:
            self.next.state(["!disabled"])
        self.save_method = save_method
        if save_method != "none":
            self.text_label = ttk.Label(self, text=label_string)
            self.text_label.grid(column=0, row=1, columnspan=3, sticky=(N,S,E,W))
            self.text_label["anchor"] = "center"
        
        if save_method == "manual":
            self.save_button = ttk.Button(self, text="Save Image", command=lambda: app_funcs.manual_save(self.prediction_frame.figure, self.prediction_frame.breed, self.prediction_frame.accuracy, self.idx, self.manually_saved_idxs, self.manually_saved_texts, self.text_label, self.save_button))
            self.save_button.grid(column=0, row=2, columnspan=3, sticky=(N,S,E,W))
            self.save_button.grid_configure(padx=5, pady=2)
            self.manually_saved_idxs = []
            self.manually_saved_texts = {}
            self.text_label["text"] = "Would you like to save this image?"

    def deactivate(self):
        """
        The deactivate method takes no arguments and its only job is to reset the coutner to '0/0', disable the previous and
        next buttons and attempt to destroy the 'text_label' and 'save_button' tk widgets.
        """
        self.counter["text"] = "0/0"
        self.next.state(["disabled"])
        self.previous.state(["disabled"])
        try:
            self.text_label.destroy()
            self.save_button.destroy()
        except:
            pass
       
    def next_image(self, prediction_frame): 
        """
        This method is one of the crucial parts of the 'NavigationFrame' object. As an argument it takes only the 'prediction_frame'
        so a PredictionImage object, in which the next prediction will be displayed.

        Depending on the previously specified save_method it will either ask the user if they want to save the displayed image
        or will print the path to the saved image under the controls.
        It also handles the behaviour of the 'next' and 'previous' buttons, depending on the idx of displayed image.
        """
        label_string = prediction_frame.display(prediction_frame.predicted_list, self.save_method, self.width_multiplier, self.height_multiplier, idx=self.idx)
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
        """
        This method is the other one of the crucial parts of the 'NavigationFrame' object. 
        As an argument it takes only the 'prediction_frame' so a PredictionImage object, in which the next prediction will be displayed.

        Depending on the previously specified save_method it will either ask the user if they want to save the displayed image
        or will print the path to the saved image under the controls.
        It also handles the behaviour of the 'next' and 'previous' buttons, depending on the idx of displayed image.
        """
        self.idx -= 1
        label_string = prediction_frame.display(prediction_frame.predicted_list, self.save_method, self.width_multiplier, self.height_multiplier, idx=self.idx-1)
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

class InputSource(LabelFrame):
    """
    This creates a tk LabelFrame that contains the tk Notebook widget with tabs as options for the input source.
    It has to be given a 'parent' in which the InputSource object will be housed.
    """
    def __init__(self, parent):
        LabelFrame.__init__(self, parent, text="Input Options")
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(column=0, row=0)
        self.input_source = StringVar()
        self.input_frame(self.notebook)
        self.specific_frame(self.notebook)
        self.web_image(self.notebook)
        
    def input_frame(self, notebook):
        """
        This method takes a 'notebook' argument, which is a tk Notebook widget. 

        It creates a tk Frame object that will be displayed under a tab titled 'Input Folder'. This object contains a 
        'folder_label' that instructs the user what the tab does and a tk Button that opens the './user/input' folder
        in a new window.

        After the whole setup it adds the tab to the 'notebook' specified.
        """
        input_frame = ttk.Frame(notebook)
        folder_label = ttk.Label(input_frame, text="Press to open the Input Folder", justify="center")
        folder_label["anchor"] = "center"
        input_folder = ttk.Button(input_frame, text="Input Folder", width=10, command=lambda: app_funcs.open_directory("input"))
        folder_label.grid(column=0, row=0, columnspan=2, sticky=(N, S, E, W))
        input_folder.grid(column=0, row=1, sticky=(N, S, E, W))
        input_frame.columnconfigure(0, weight=3)
        for child in input_frame.winfo_children():
            child.grid_configure(padx=2, pady=2)
        notebook.add(input_frame, text="Input Folder")
    
    def specific_frame(self, notebook):
        """
        This method takes a 'notebook' argument, which is a tk Notebook widget. 

        It creates a tk Frame object that will be displayed under a tab titled 'Specific'. This object contains a 
        'specific_label' that instructs the user what the tab does and two tk Buttons. The 'directory_button' opens a dialog
        window that asks the user to pick a folder in which they have images to make predictions on. The 'file_button' opens
        a fialog window that asks the user to pick a specific image.

        After the whole setup it adds the tab to the 'notebook' specified.
        """
        specific_frame = ttk.Frame(notebook)
        specific_label = ttk.Label(specific_frame, text="Please choose:")
        specific_label["anchor"] = "center"
        self.selected_mode = StringVar()
        self.specific_directory = StringVar()
        directory_button = ttk.Button(specific_frame, text="Directory", command=lambda: (self.specific_directory.set(filedialog.askdirectory(initialdir="./")), self.selected_mode.set("dir")))
        self.specific_file = StringVar()
        file_button = ttk.Button(specific_frame, text="File", command=lambda: (self.specific_file.set(filedialog.askopenfilename(initialdir="./")), self.selected_mode.set("img")))
        or_label = ttk.Label(specific_frame, text="or")
        or_label["anchor"] = "center"
        specific_label.grid(column= 0, row= 0, columnspan= 3, sticky= (N,S,E,W))
        directory_button.grid(column= 0, row= 1, sticky= (N,S,E,W))
        or_label.grid(column= 1, row= 1, sticky= (N,S,E,W))
        file_button.grid(column= 2, row= 1, sticky= (N,S,E,W))
        specific_frame.columnconfigure(0, weight=3)
        specific_frame.columnconfigure(1, weight=3)
        specific_frame.columnconfigure(2, weight=3)
        for child in specific_frame.winfo_children():
            child.grid_configure(padx=2, pady=2)
        notebook.add(specific_frame, text="Specific")

    def web_image(self, notebook):
        """
        This method takes a 'notebook' argument, which is a tk Notebook widget. 

        It creates a tk Frame object that will be displayed under a tab titled 'Web Image'. This object contains a 
        'web_image_label' that instructs the user what the tab does and a tk Entry widget. User is meant to paste the URL
        to a singular image into this Entry field.

        After the whole setup it adds the tab to the 'notebook' specified.
        """
        web_image_frame = ttk.Frame(notebook)
        web_image_label = ttk.Label(web_image_frame, text="Paste the URL to an image")
        web_image_label["anchor"] = "center"
        self.image_url = StringVar()
        url_entry = ttk.Entry(web_image_frame, textvariable=self.image_url)
        web_image_label.grid(column=0, row=0, columnspan=2, sticky=(N,S,E,W))
        url_entry.grid(column=0, row=1, columnspan=2, sticky=(N,S,E,W))
        web_image_frame.columnconfigure(0, weight=3)
        for child in web_image_frame.winfo_children():
            child.grid_configure(padx=2, pady=2)
        notebook.add(web_image_frame, text="Web Image")
