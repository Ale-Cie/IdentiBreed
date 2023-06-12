import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import subprocess

from resources import model_funcs

from IPython.display import Image
from PIL import Image


def predict_user_images(file_paths, unique_labels, model):
    """
    This function takes a path to the user input directory and the unique_labels list.
    It makes model create predictions of dog breeds present in user's images.
    The function creates a list of dictionaries for each image. 
    These dictionaries contain the image tensor, predicted breed, model's confidence, four other probable breeds and their confidences.

    Returns list of image paths and list of image dictionaries. 
    """

    # Instantiating empty lists for image paths and image dictionaries
    dir_list, predicted_files = [], []
    print("Predicting dog breeds from images in './images' folder.")
    print("This could take a moment...")

    for file in os.listdir(file_paths):
        try:
            img_path = file_paths + "/" + file

            # We turn each image into it's own minibatch and feed it into the model
            img = model_funcs.minibatch_maker(X=[img_path], batch_size=32, test_data=True)
            prediction = model.predict(img, verbose=0)

            # Based on the highest probability we get the breed label and the next four with highest probability
            pred_label = model_funcs.name_predicted_label(prediction, unique_labels)
            top_5_preds = prediction.argsort()[0][-5:][::-1]

            # We create a new `predicted_files` entry 
            pred_dict = {
                "image": model_funcs.turn_to_tensor(img_path), # Tensor for ease of displaying later
                "prediction": pred_label, # The dog breed predicted by the model
                "accuracy": ("%.3f" %(np.max(prediction[0]) * 100)), # Probability in percentage
                "top_5_labels": unique_labels[top_5_preds], # Top 5 predicted labels
                "top_5_confidences": prediction[0][top_5_preds] # Top 5 confidences
            }

            # We append the dictionary to the list and an image file path into another list
            predicted_files.append(pred_dict)
            dir_list.append(img_path)
        except:
            pass
        # return_list = [dir_list, predicted_files]
    print("Predicting completed")
    # return return_list
    return dir_list, predicted_files

def image_saver(image, breed_label, accuracy= None, data_expansion= False, prefix= None):
    """
    This function takes an image, breed label and optionally:
        - accuracy: Model's confidence of the prediction being correct
        - data_expansion: True if we want to save images as future dataset expansion submissions
        - prefix: string if we want to mark user submitted breed for future reference

    It saves the image either into './user/output' if data_expansion is False or './data/user_submissions' if data_expansion is True.

    When it is saving the predicted images to the './user/output' it returns a label_string that gets displayed in the navigation frame.
    """
    # We get the current time in order to add as a suffix to the file name
    date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # This block runs when the predicted breed was evaluated by the user
    if data_expansion:
        print("Currently images are only stored locally, they are not sent to the staff.")
        print("Adding image to the training dataset...")
        with Image.open(image) as img:
            if not prefix:
                # This line runs in two scenarios:
                # 1) The prediction was correct from the get go
                # 2) The prediction was incorrect, but user provided a breed that exists within the unique_labels list
                img.save(f"./data/user_submissions/{breed_label}_{date}.jpg")
            else:
                # This line runs in another two scenarios:
                # 1) Person running the code wants to differentiate certain saved images
                # 2) The intended scenario - user has provided a breed name three times, but it wasn't present in the unique_labels.
                # User is certain that what he provides is correct, function saves it with an originally intended prefix.
                # The intended prefix is 'US' as in User Submitted. It gets specified elsewhere in the repository
                img.save(f"./data/user_submissions/{prefix}_{breed_label}_{date}.jpg")
    
    # This block runs when user agreed to saving the images with predicted labels and top five predictions
    # The image here is really a matplotlib figure
    else:
        prediction_date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{breed_label}_{accuracy}%_{prediction_date}.jpg"
        image.savefig(f"./user/output/{filename}", bbox_inches= "tight")
        return f"Prediction saved to output folder under name: {filename}'"

def open_directory(directory_name):
    """
    This simple function serves as a command to two different buttons.
    If either of the buttons is pressed a specified folder within './user/' directory opens in a new window.
    """

    try:
        subprocess.run(["start", f"./user/{directory_name}"])
    except:
        subprocess.run(["open", f"./user/{directory_name}"])


def data_expander(image_path, breed_label, unique_labels):
    """
    This function takes an image path, breed label and the unique labels list.
    As it runs it asks the user if the model's prediction was correct.
    Depending on the users evaluation:
        - Correct Prediction: the image is saved into './data/user_submissions' directory with the breed label and date as file name
        - Incorrect Prediction: User is asked if they can provide the correct breed. Depending on their answer:
            * Answer in unique_labels: Image is saved into './data/user_submissions' with the answer and date as a file name
            * Answer not in unique_labels: User is told their breed was not found in the database. User is asked if they want to try again:
                - User agrees: After third try the breed specified by the user is added a prefix of 'US' (as in User Submitted) and saved to './data/user_submissions' as prefix_breed_date.jpg
                - User disagrees: The image is omitted from saving to './data/user_submissions'
            * User declines: The image is omitted from saving to './data/user_submissions'

    Returns nothing.
    """
    

    # Here we start the first loop that user won't break out of until the image is either saved or omitted
    evaluation_loop = True
    while evaluation_loop:
        # We  assume that the user knows the correct breed of the dog present in the image and ask for their evaluation
        correct_flag = input("Was my prediction correct? [Y/N]").lower()
        
        # This block runs if the prediction was correct. It just runs the saver function and then ends the evaluation loop
        if correct_flag == "y":
            image_saver(
                image= image_path,
                breed_label= breed_label,
                data_expansion= True
            )
            evaluation_loop = False
        
        # Here we delve deeper since user says the prediction was not correct. 
        # We will be measuring attempts of breed name input and on the third incorrect one user will be asked to input the breed they think is correct
        elif correct_flag == "n":
            attempt = 1
            
            # Before we start another loop we ask the user if they know the correct breed. 
            # If they say they do we start the loop, if not we end the function
            correction_loop = True
            user_label_flag = input("Do you know the correct dog breed? [Y/N]").lower()
            while correction_loop:
                if user_label_flag == "y":

                    # Now based on user input we check if the breed is present in the 'unique_labels'
                    # Before that however we make edits to the breed provided so that it's in style of other breeds from labels.csv
                    breed_label = input("What was the correct dog breed?").lower().replace(" ", "_")
                    if breed_label in unique_labels:
                        
                        # We save the image because the breed was in the 'unique_breeds', then we close out of both the correction and evaluation loops
                        image_saver(
                            image= image_path,
                            breed_label= breed_label,
                            data_expansion= True
                        )
                        evaluation_loop, correction_loop = False, False
                    
                    # We now go on a bit of a ride - user provided an unknown or incorrect breed, we have to check what's going on
                    else:
                        try_again_loop = True
                        while try_again_loop:
                            
                            # This code is actually last to run but I've put it at the top to make sure it runs when it's needed.
                            # (I know I could reverse it, but it works and I really don't care enough now)
                            # With this if statement we allow user to save na image with the breed he THINKS is correct, but was not recognized three times
                            # However we run the 'image_saver()' function with a prefix 'US'. Then we close ot of all three loops
                            if attempt == 3:
                                user_breed = input("Specified breed not present in the database. Please write down the correct name of the breed. Our staff will manually check it and add to the database if correct.").lower()
                                image_saver(
                                    image= image_path,
                                    breed_label= user_breed,
                                    data_expansion= True,
                                    prefix= "US"
                                )
                                evaluation_loop, correction_loop, try_again_loop = False, False, False
                            
                            # This is a block of code that runs for the most of this loop. We ask for input and count how many attempts have already taken place
                            # If user says they don't want to try again we close all the loops.
                            # However, if they want to try again we give them the chance and add 1 to the attempt variable.
                            else:
                                again = input(f"Attempt {attempt}/3. Dog breed not found in the database. Would you like to try again? [Y/N]").lower()
                                if again == "y":
                                    attempt += 1
                                    try_again_loop = False
                                elif again == "n":
                                    print("Thank you for your cooperation. This breed is not yet supported and the image will not be used for further training purposes.")
                                    evaluation_loop, correction_loop, try_again_loop = False, False, False
                                else:
                                    print("Error, please try again.")
                            
                elif user_label_flag == "n":
                    print("Thank you for your cooperation. This image will not be used for further training purposes.")
                    evaluation_loop, correction_loop = False, False
                    
                else:
                    print("Error, please try again.")
                    user_label_flag = input("Do you know the actual dog breed? [Y/N]").lower()

        else:
            print("Error, please try again.")

def show_user_images(predicted_files, figure, axes, idx=0):
    """
    This function takes the predicted_files (as return by 'predict_user_images()') a matplotlib figure and axes.
    Optionally you can give it an idx, but really this is more of a mandatory argument if you want to see more than just the first prediction
    """

    # Here we go plotting results of the prediction.
    # We create a new figure with two subaxes for each prediction, which we can later easily save
    # On the left of the figure we will be plotting a resized image with a title of 'I am X% sure it's a PREDICTION'
    # On the right we will plot a bar graph containing top five predictions
    
    figure, axes
    figure.set_figheight(2.5)
    figure.set_figwidth(5)
    figure.tight_layout()
    prediction_dict = predicted_files[idx]
    ax1, ax2 = axes[0], axes[1]
    ax1.imshow(prediction_dict["image"])
    breed_label = prediction_dict['prediction'].replace("_", " ")
    ax1.set_title(f"I am {prediction_dict['accuracy']}% sure it's a {breed_label}", fontdict={"fontsize": 6})
    ax1.set_yticks([])
    ax1.set_xticks([])
    ax2.bar(
        x=np.arange(len(prediction_dict["top_5_labels"])),
        height= prediction_dict["top_5_confidences"],
        color= "tab:gray",

    )
    ax2.set_title("Top 5 probable breeds", fontdict={"fontsize": 6})
    labels=[]
    for label in prediction_dict["top_5_labels"]:
        labels.append(label.replace("_", "\n"))
    ax2.tick_params(axis="y", labelsize= 6)
    ax2.set_xticks(
        np.arange(len(prediction_dict["top_5_labels"])),
        labels= labels,
        fontsize= 4
    )
    bars = ax2.containers[0]
    ax2.bar_label(bars, labels = [f'{x.get_height():.3%}' for x in bars], fontsize= 5)

    return figure, prediction_dict["prediction"], prediction_dict["accuracy"]

    

    
    
    