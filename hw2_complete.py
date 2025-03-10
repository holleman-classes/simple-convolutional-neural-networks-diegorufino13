# -*- coding: utf-8 -*-
"""hw2_complete

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17IjTtIzOX932lVm8UC-6udtyiBQmHNgl
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Conv2D, BatchNormalization, MaxPooling2D, Flatten, Dense, SeparableConv2D, Input, Dropout, Add
from tensorflow.keras.datasets import cifar10
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical

if tf.test.gpu_device_name():
  print('GPU device found: ', tf.test.gpu_device_name())

else:
  print("No GPU found. Make sure to enable GPU in the Colab runtime settings.")

def build_model1():
    model = Sequential()

    # Conv2D layer with 32 filters, 3x3 kernel, stride=2, and "same" padding
    model.add(Conv2D(32, (3, 3), strides=(2, 2), padding='same', activation='relu', input_shape=(32, 32, 3)))
    model.add(BatchNormalization())

    # Conv2D layer with 64 filters, 3x3 kernel, stride=2, and "same" padding
    model.add(Conv2D(64, (3, 3), strides=(2, 2), padding='same', activation='relu'))
    model.add(BatchNormalization())

    # Conv2D layer with 128 filters, 3x3 kernel, stride=2, and "same" padding
    model.add(Conv2D(128, (3, 3), strides=(2, 2), padding='same', activation='relu'))
    model.add(BatchNormalization())

    # Four more pairs of Conv2D+Batchnorm with no striding option
    for _ in range(4):
        model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
        model.add(BatchNormalization())

    # Conv2D layer with 128 filters, 3x3 kernel, "same" padding
    model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
    model.add(BatchNormalization())

    # MaxPooling layer with 4x4 pooling size and 4x4 stride
    model.add(MaxPooling2D(pool_size=(4, 4), strides=(4, 4)))

    # Flatten layer
    model.add(Flatten())

    # Dense layer with 128 units
    model.add(Dense(128, activation='relu'))
    model.add(BatchNormalization())

    # Dense layer with 10 units (output layer)
    model.add(Dense(10, activation='softmax'))

    return model

def build_model2():
  model = Sequential()

  # Standard Conv2D layer with 32 filters, 3x3 kernel, stride=2, and "same" padding
  model.add(Conv2D(32, (3, 3), strides=(2, 2), padding='same', activation='relu', input_shape=(32, 32, 3)))
  model.add(BatchNormalization())

  # Depthwise separable Conv2D layer with 64 filters, 3x3 kernel, stride=2, and "same" padding
  model.add(SeparableConv2D(64, (3, 3), strides=(2, 2), padding='same', activation='relu'))
  model.add(BatchNormalization())

  # Depthwise separable Conv2D layer with 128 filters, 3x3 kernel, stride=2, and "same" padding
  model.add(SeparableConv2D(128, (3, 3), strides=(2, 2), padding='same', activation='relu'))
  model.add(BatchNormalization())

  # Four more pairs of Depthwise separable Conv2D+Batchnorm with no striding option
  for _ in range(4):
    model.add(SeparableConv2D(128, (3, 3), padding='same', activation='relu'))
    model.add(BatchNormalization())

    # Depthwise separable Conv2D layer with 128 filters, 3x3 kernel, "same" padding
    model.add(SeparableConv2D(128, (3, 3), padding='same', activation='relu'))
    model.add(BatchNormalization())

    # MaxPooling layer with 4x4 pooling size and 4x4 stride
    model.add(MaxPooling2D(pool_size=(4, 4), strides=(4, 4)))

    # Flatten layer
    model.add(Flatten())

    # Dense layer with 128 units
    model.add(Dense(128, activation='relu'))
    model.add(BatchNormalization())

    # Dense layer with 10 units (output layer)
    model.add(Dense(10, activation='softmax'))

    return model

def build_model3():
    input_layer = Input(shape=(32, 32, 3))

    # First Convolutional Block
    x = Conv2D(32, (3, 3), strides=(2, 2), padding='same', activation='relu')(input_layer)
    x = BatchNormalization()(x)

    # Second Convolutional Block with Skip Connection
    residual = Conv2D(64, (1, 1), strides=(2, 2), padding='same', activation='relu')(x)
    x = Conv2D(64, (3, 3), strides=(2, 2), padding='same', activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    x = Add()([x, residual])  # Skip connection

    # Third Convolutional Block with Skip Connection
    residual = Conv2D(128, (1, 1), strides=(2, 2), padding='same', activation='relu')(x)
    x = Conv2D(128, (3, 3), strides=(2, 2), padding='same', activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)
    x = Add()([x, residual])  # Skip connection

    # Four more pairs of Conv2D+Batchnorm with dropout, followed by residual connections
    for _ in range(4):
        residual = x  # Store the current state for the residual connection

        x = Conv2D(128, (3, 3), padding='same', activation='relu')(x)
        x = BatchNormalization()(x)
        x = Dropout(0.2)(x)

        x = Conv2D(128, (3, 3), padding='same', activation='relu')(x)
        x = BatchNormalization()(x)
        x = Dropout(0.2)(x)

        # Check if the number of channels in the residual and main path differ
        if residual.shape[-1] != x.shape[-1]:
            residual = Conv2D(x.shape[-1], (1, 1), padding='same', activation='relu')(residual)

        x = Add()([x, residual])  # Residual connection

    # Last Convolutional Block
    x = Conv2D(128, (3, 3), padding='same', activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)

    # MaxPooling layer with 4x4 pooling size and 4x4 stride
    x = MaxPooling2D(pool_size=(4, 4), strides=(4, 4))(x)

    # Flatten layer
    x = Flatten()(x)

    # Dense layer with 128 units
    x = Dense(128, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(0.2)(x)

    # Dense layer with 10 units (output layer)
    output_layer = Dense(10, activation='softmax')(x)

    model = Model(inputs=input_layer, outputs=output_layer, name='model3')
    return model

def build_model50k():
  model = Sequential() # Add code to define model 1.

  # Convolutional Block 1
  model.add(Conv2D(16, (3, 3), activation='relu', input_shape=(32, 32, 3)))
  model.add(BatchNormalization())
  model.add(MaxPooling2D(pool_size=(2, 2)))

  # Fully Connected Layer
  model.add(Flatten())
  model.add(Dense(10, activation='softmax'))

  return model

# no training or dataset construction should happen above this line
if __name__ == '__main__':

  ########################################
  ## Add code here to Load the CIFAR10 data set

# Loading CIFAR-10 dataset
 (train_images, train_labels), (test_images, test_labels) = cifar10.load_data()

# Splitting training set into training and validation set
train_images, val_images, train_labels, val_labels = train_test_split( train_images, train_labels, test_size = 0.2, random_state = 42)

# Normalize pixel values between 0 and 1
train_images, val_images, test_images = train_images / 255,  val_images / 255, test_images / 255

# Convert labels to one-hot encoding
train_labels = to_categorical(train_labels, num_classes=10)
val_labels = to_categorical(val_labels, num_classes=10)
test_labels = to_categorical(test_labels, num_classes=10)

print("Training set shapes:")
print("Images:", train_images.shape)
print("Labels:", train_labels.shape)

print("\nValidation set shapes:")
print("Images:", val_images.shape)
print("Labels:", val_labels.shape)

print("\nTest set shapes:")
print("Images:", test_images.shape)
print("Labels:", test_labels.shape)
  ########################################

from google.colab import files

uploaded = files.upload()

## Build model 1
  model1 = build_model1()

  # Display the model summary
  model1.summary()

  # compile model 1
  model1.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

  # Train the model for 50 epochs
  history1 = model1.fit(train_images, train_labels, epochs=50, validation_data=(val_images, val_labels))

  # Evaluate the model on the test set
  test_loss, test_accuracy = model1.evaluate(test_images, test_labels)

  print("\nTest Accuracy:", test_accuracy)

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import matplotlib.pyplot as plt

# Load the pre-trained model
model = build_model1()  # Use the function you defined to build the model


# Load and preprocess the uploaded image
img_path = '/content/' + list(uploaded.keys())[0]  # Get the path of the uploaded file
img = image.load_img(img_path, target_size=(32, 32))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)

# Make predictions
predictions = model.predict(img_array)

# Decode and print the prediction
predicted_class = np.argmax(predictions[0])
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
predicted_class_name = class_names[predicted_class]

print(f"The predicted class is: {predicted_class_name}")

# Display the image
plt.imshow(img)
plt.axis('off')
plt.show()

## Build model 2
  model2 = build_model2()

  # Display the model summary
  model2.summary()

  # compile model 2
  model2.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

  # Train the model for 50 epochs
  history2 = model2.fit(train_images, train_labels, epochs=50, validation_data=(val_images, val_labels))

  # Evaluate the model on the test set
  test_loss, test_accuracy = model2.evaluate(test_images, test_labels)

  print("\nTest Accuracy:", test_accuracy)

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import matplotlib.pyplot as plt

# Load the pre-trained model
model = build_model2()  # Use the function you defined to build the model


# Load and preprocess the uploaded image
img_path = '/content/' + list(uploaded.keys())[0]  # Get the path of the uploaded file
img = image.load_img(img_path, target_size=(32, 32))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)

# Make predictions
predictions = model.predict(img_array)

# Decode and print the prediction
predicted_class = np.argmax(predictions[0])
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
predicted_class_name = class_names[predicted_class]

print(f"The predicted class is: {predicted_class_name}")

# Display the image
plt.imshow(img)
plt.axis('off')
plt.show()

## Build model 3
  model3 = build_model3()

  # Display the model summary
  model3.summary()

  # compile model 2
  model3.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

  # Train the model for 50 epochs
  history3 = model3.fit(train_images, train_labels, epochs=50, validation_data=(val_images, val_labels))

  # Evaluate the model on the test set
  test_loss, test_accuracy = model3.evaluate(test_images, test_labels)

  print("\nTest Accuracy:", test_accuracy)

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import matplotlib.pyplot as plt

# Load the pre-trained model
model = build_model3()  # Use the function you defined to build the model


# Load and preprocess the uploaded image
img_path = '/content/' + list(uploaded.keys())[0]  # Get the path of the uploaded file
img = image.load_img(img_path, target_size=(32, 32))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)

# Make predictions
predictions = model.predict(img_array)

# Decode and print the prediction
predicted_class = np.argmax(predictions[0])
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
predicted_class_name = class_names[predicted_class]

print(f"The predicted class is: {predicted_class_name}")

# Display the image
plt.imshow(img)
plt.axis('off')
plt.show()

## Build model 50k
  model50k = build_model50k()

  # Display the model summary
  model50k.summary()

  from tensorflow.keras.optimizers import Adam

  # compile model
  model50k.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

  # Train the model for 50 epochs
  history50k = model50k.fit(train_images, train_labels, epochs=20, batch_size=64, validation_data=(val_images, val_labels))
  # Evaluate the model on the test set
  test_loss, test_accuracy = model50k.evaluate(test_images, test_labels)

  print("\nTest Accuracy:", test_accuracy)

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import matplotlib.pyplot as plt

# Load the pre-trained model
model = build_model50k()  # Use the function you defined to build the model


# Load and preprocess the uploaded image
img_path = '/content/' + list(uploaded.keys())[0]  # Get the path of the uploaded file
img = image.load_img(img_path, target_size=(32, 32))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)

# Make predictions
predictions = model.predict(img_array)

# Decode and print the prediction
predicted_class = np.argmax(predictions[0])
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
predicted_class_name = class_names[predicted_class]

print(f"The predicted class is: {predicted_class_name}")

# Display the image
plt.imshow(img)
plt.axis('off')
plt.show()