# IdentiBreed - The dog breed identification AI

<p align="center">
    <img src="./resources/images/banner_color.png"/>
</p>

This here repository represents a project I started doing during an online course. Upon finishing said course I decided to expand and further work on this model.

In simple words - if you've got a picture of a dog, this should be able to recognize it! As long as it's breed is within the 120 ones given by Kaggle, but will get onto that in a bit...

## Background

Through this repository (and more specifically the `IdentiBreed.ipynb` notebook) I'm tackling a multi-class classification problem. Kaggle, through its 2017 <a href="https://www.kaggle.com/competitions/dog-breed-identification">"Dog Breed Identification"</a> competition equipped us with over 10k images of different dog breeds, which we can use to train models in recognising said breeds. Then, we were expected to make predictions on a test set and submit them in a .csv format.

I said 'were' above since the competition has already finished, but we can still post late submissions and get evaluation scores on how our models performed.

## What to expect?

I set out to create a model using a network imported from TensorFlow Hub. I decided on a MobileNet v2 based model, which takes 244 x 244 images as input. In the `IdentiBreed.ipynb` notebook I efectively take my first steps in creating a transfer learning model, and I declare all necessary functions as I go along. Originally it was done with a help of an online course, but after finishing it I came back and improved this notebook as much as I could.

## What's already happened?

Inital model has been completed a long time ago (some time in April) and then I set out to expand on the project.

<i>-- 12.06.2023 --</i>

Since the last update I focused on creating a windowed version of the app using the `tkinter` module. Now, if you run the `IdentiBreed.py` file within an active Conda env (please use the `dl-env.yml` to recreate the environment) you're greeted to a simple, rather user-friendly window.

Under the banner you will see three divisions that you can interact with! Let me go through each one of them:

- `User Images Input/Output` - As the text label suggests, if you click on either "Input Folder" or "Output Folder" buttons Finder/Explorer will open new windows. In order to give the app files to predict place your images inside of the "Input folder". If you check the box right under those buttons, all saved predictions will appear inside "Output folder".
- `Predict Breeds` - Just one button here, before you click it make sure you've decided whether you want your images saved or not since you won't be able to change it later. As you click "Make Predictions", you let IdentiBreed do what it's best at - predicting dog breeds from images. The banner will change to a figure containing a labeled image and top 5 predicted labels.
- `Navigation Controls` - Once IdentiBreed's made predictions on your images you will get access to those controls. The counter will display which image out how many it is showing, and the buttons "< Previous" and "Next >" will take you through all of your predictions! Easy as that!

<i>-- 26.05.2023 -- </i>

The repostiory was updated with this new notebook `Identifyin_User_Images.ipynb` and two files containing functions defined so far - `model_funcs.py` and `user_funcs.py`. Now the user can give model their images, see what breeds the model thinks are present in these images and if they want save those outputs for them. Alongside these the images are saved (currently locally) in 'user_submissions' directory within './data/' with the correct breed as label. This in future will allow me to gather those images and use them for retraining the network.

## What's next?

Three boxes down, one new and four old ones to go...

From now on I will focus on expanding the app with few more controls. I want to make the user evaluate the breeds in the same way as in the `Identifying_User_Images.ipynb`. This will require a `LabelFrame` with about three or four buttons and a combobox. I played around a bit with a possible UI, so implementation won't take very long.

Next up I will have to consider expanding the training dataset, since it's missing some dog breeds (for instance the internet staple - the Doge itself - both 'shiba' and 'akita' breeds).

That's as far as my goals stretch for now. Another goal I can consider is putting the model up on my portfolio website, as a web accessible breed identifier. And some more things like streamlining the notebooks, creating a new iteration of IdentiBreed that's from the ground up mine etc.

So to sum up the goals (present and future):
<br /> ✅ Create the first iteration of IdentiBreed
<br /> ✅ Prepare model to make predictions on user submitted pictures
<br /> ✅ Put the model and most of the obligatory functions into a windowed app
<br /> ◽️ Add prediction evaluation and dataset expansion
<br /> ◽️ Expand the training dataset with missing dog breeds
<br /> ◽️ Make the model web accessible
<br /> ◽️ Streamline the notebooks
<br /> ◽️ Rebuild the model from ground up (no TensorFlow Hub)
