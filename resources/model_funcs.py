import tensorflow as tf
import tensorflow_hub as hub
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import io

from IPython.display import Image
from sklearn.model_selection import train_test_split

def turn_to_tensor(img_path, img_size=224):
  """
  This function takes an image path and uses it to load in an image and turn it into a Tensor.
  Then it converts the dtype and resizes the image to img_size x img_size

  Returns a normalized Tensor
  """

  # Load in the image file and turn it into a numerical Tensor
  img = tf.io.read_file(img_path)
  img = tf.image.decode_jpeg(img, channels=3)

  # Normalizing the image and resizing it to a constant (244x244)
  img = tf.image.convert_image_dtype(img, tf.float32)
  img = tf.image.resize(img, size=(img_size, img_size))

  return img

def create_tensor_img_tuple(img_path, label):
  """
  This function takes an image path and its corresponding label. 
  Then it turns the image from path provided into a Tensor. 

  Returns a tuple - (Tensor, label)
  """

  image = turn_to_tensor(img_path)
  
  return image, label

def minibatch_maker(X, batch_size, y=None, valid_data=False, test_data=False):
  """
  Creates data batches out of image and label pairs (X and y pairs).
  Unless specified otherwise thebatch_size equals 32
  Shuffles the data if it's training data.
  Doesn't shuffle if it's validation data.
  Accepts the Kaggle test data.

  Returns a data batch
  """

  if test_data:
    # I commented out the line below because it was really annoying when I started tossing single images at the model to test it IRL
    #print("Splitting test data into batches")
    data = tf.data.Dataset.from_tensor_slices((tf.constant(X)))
    data_batch = data.map(turn_to_tensor).batch(batch_size)
    return data_batch
  elif valid_data:
    print("Splitting validation data into batches")
    data = tf.data.Dataset.from_tensor_slices((tf.constant(X), tf.constant(y)))
    data_batch = data.map(create_tensor_img_tuple).batch(batch_size)
    return data_batch
  else:
    # This one we want to shuffle
    np.random.seed(7821)
    print("Splitting training data into batches")
    data = tf.data.Dataset.from_tensor_slices((tf.constant(X), tf.constant(y)))
    data = data.shuffle(buffer_size=len(X))
    data_batch = data.map(create_tensor_img_tuple).batch(batch_size)
    return data_batch

def build_network(input_shape, output_shape, model_url):
  """
  This function can take an input_shape, output_shape and a model_url in order to create a Neural Network.
  Network created by this function has '2' layers:
   - Input Layer
   - Output Layer, which outputs data in the shape of output_shape (len(unique_labels))
  Any other layers present are hidden within the imported model.

  Returns a network
  """
  model = tf.keras.Sequential([
      hub.KerasLayer(
        model_url, 
        name="InputLayer"
      ), # Layer 1 - Input layer
      tf.keras.layers.Dense(
        units= output_shape, 
        activation= "softmax",
        name= "OutputLayer"
      ) # Layer 2 - Output layer 

  ])

  model.compile(
      loss= tf.keras.losses.CategoricalCrossentropy(),
      optimizer= tf.keras.optimizers.Adam(),
      metrics= ["accuracy"]
  )

  model.build(input_shape)

  return model

def tensorboard_callback():
  """
  Creates checkpoints and saves them in a /logs folder under the date of creation.

  Returns a TensorBoard callback
  """
  try:
    logdir = os.path.join("./logs", datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
  except:
    logdir = os.path.join("/kaggle/working/logs", datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))

  return tf.keras.callbacks.TensorBoard(logdir)

def name_predicted_label(probabilities, unique_labels):
  """
  This function takes a list of 120 probabilities, finds the index of the most probable one and searches 'unique_labels' for the corresponding name

  Returns the breed name
  """

  return unique_labels[np.argmax(probabilities)]

def unbatch_data(batched_data):
  """
  This function takes a data batch and unbatches it into an ordered list of images, and another ordered list of corresponding true labels

  Returns images list and labels list
  """

  images = []
  labels = []

  for image, label in batched_data.unbatch().as_numpy_iterator():
    images.append(image)
    labels.append(unique_labels[np.argmax(label)])

  return images, labels

def display_prediction(prediction_probabilities, labels, images, n=0):
  """
  This function takes a list of prediction probabilities, list of labels, list of images and an index. 
  It plots the result of models prediction - it displays the image of the dog with predicted breed, the probability and an actual label.
  If the prediction was right, the text will appear in green. Else it will be red
  """

  n = 0 if n > len(prediction_probabilities) else n
  probabilities, true_label, image = prediction_probabilities[n], labels[n], images[n]

  pred_label = name_predicted_label(probabilities)

  if pred_label == true_label:
    t_color = "tab:green"
  else:
    t_color = "tab:red"

  plt.imshow(image)
  plt.title("{} {:0.3f}% {}".format(
      pred_label,
      np.max(probabilities)*100,
      true_label),
      color= t_color)
  plt.xticks([])
  plt.yticks([])

def plot_k_confidences(prediction_probabilities, labels, k=5, n=0):
  """
  This function takes list of prediction probabilites, list of dog breed labels.
  Optionally it takes:
   - 'k' - a variable specifying how many highest probabilites to plot
   - 'n' - a specific index of an image to check for prediction and an actual label
  """
  n = 0 if n > len(prediction_probabilities) else n
  pred_probabilities, true_label = prediction_probabilities[n], labels[n]

  # pred_label = name_predicted_label(pred_probabilities)

  top_k_idx = pred_probabilities.argsort()[-k:][::-1]
  top_k_confidences = pred_probabilities[top_k_idx]
  top_k_labels = unique_labels[top_k_idx]

  top_k_plot = plt.bar(np.arange(len(top_k_labels)),
                     top_k_confidences,
                     color="grey")
  plt.xticks(np.arange(len(top_k_labels)),
             labels=top_k_labels,
             rotation="vertical")
  
  if np.isin(true_label, top_k_labels):
    top_k_plot[np.argmax(top_k_labels == true_label)].set_color("tab:green")
  else:
    pass

def plot_k_predictions(prediction_probabilities, labels, images, i_multiplier=0, n_rows= 4, n_cols= 2, k=5):
  """
  This function creates a figure showing different predictions and the top probabilities. 
  It takes following arguments:
   - prediction_probabilities - an ordered list of probabilities created by the model
   - labels - an ordered list of actual labels for the dataset on which predictions were made
   - images - an ordered list of tensors, on which predictions were made
  
  Optional arguments:
   - i_multiplier - int that makes the function show next images
   - n_rows - int specifying how many rows of predictions to describe
   - n_cols - int specifying how many columns of predictions to describe
   - k - int specifying how many top prediction values to plot
  """

  n_images = n_rows * n_cols

  plt.figure(figsize=(10*n_cols, 5*n_rows))
  for i in range(n_images):
    plt.subplot(n_rows, 2*n_cols, 2*i+1)
    display_prediction(
        prediction_probabilities= prediction_probabilities,
        labels = labels,
        images = images,
        n = i+i_multiplier
    )
    plt.subplot(n_rows, 2*n_cols, 2*i+2)
    plot_k_confidences(
        prediction_probabilities= prediction_probabilities,
        labels = labels,
        k= k,
        n= i+i_multiplier,
    )
  plt.tight_layout(h_pad=1.0)
  plt.show()

def save_model(model, suffix=None):
  """
  Saves the model in the ./models directory. It takes two arguments:
   - model - the actual model to be saved
   - suffix (optional) - any user defined string that describes the model and will be attached to the file name for identification purposes

  Returns path to the saved .h5 file
  """
  try:
    modeldir = os.path.join("./models", datetime.datetime.now().strftime("%Y%m%d-%H%M%s"))
  except:  
    modeldir = os.path.join("/kaggle/working/models", datetime.datetime.now().strftime("%Y%m%d-%H%M%s")) 
  model_path = modeldir + "-" + suffix + ".h5"

  print(f"Saving model to: {model_path}...")
  model.save(model_path)
  
  return model_path

def load_model(model_path):
  """
  Loads the model from the .h5 file under 'model_path'

  Returns model
  """
  print(f"Loading saved model from: {model_path}...")
  model = tf.keras.models.load_model(model_path,  custom_objects={"KerasLayer": hub.KerasLayer})
  
  return model

def submission_maker(predictions):
    """This function takes predictions array and along with the breed names and image names puts them into a Kaggle ready DataFrame """
    # We start by creating a list of all the test images names, without the extension which starts at index -4
    global unique_labels
    index_names = [name[:-4] for name in os.listdir("./data/test/")]
    try:
        index_names.remove("test")
    except:
        print("No 'test.txt' located, preparing index_names...")

    submission = pd.DataFrame(predictions, columns=unique_labels, index=index_names)

    submission.index.name = "id"
    return submission

def unique_labels_maker(labels_csv_path):
  """
  This function takes path to the 'labels.csv' file. 

  Returns a list of unique labels
  """
  labels_csv = pd.read_csv(labels_csv_path)
  unique_labels = np.unique(np.array(labels_csv["breed"]))

  return unique_labels

def export_labels(unique_labels):
  """
  This function exports all unique labels into a .txt file. 
  Save path is 'IdentiBreed/resources/'.
  It takes an 'unique_labels' NumPy array type object.
  """
  with open("./resources/unique_labels.txt",                                              "w") as file:
    for label in unique_labels:
      file.writelines(label + "\n")
