import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense, Flatten,Dropout
X = []
Y = []
total_class = 43
cur_directory = os.getcwd()

for index in range(total_class):
  path = os.path.join(cur_directory, 'Train', str(index))
  images = os.listdir(path)
#iterating on all the images of the index folder
  for img in images:
    try:
      image = Image.open(path + '/'+ img)
      image = image.resize((30, 30))
      image = np.array(image)
      X.append(image)
      Y.append(index)
    except:
        print("Error loading image")
X = np.array(X)
Y = np.array(Y)
print(X.shape, Y.shape)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.5, random_state=42)
print("Shape of x_train: ", x_train.shape, " and y_train:",y_train.shape)
print("Shape of x_test: ", x_test.shape, " and y_test:",y_test.shape)
#one hot encoding the labels
y_train = to_categorical(y_train, 43)
y_test = to_categorical(y_test, 43)

model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu', input_shape=x_train.shape[1:]))
model.add(Conv2D(filters=32, kernel_size=(5, 5), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(rate=0.25))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPool2D(pool_size=(2, 2)))
model.add(Dropout(rate=0.25))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(rate=0.5))
model.add(Dense(43, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

epochs = 15
history = model.fit(x_train, y_train, batch_size=64, epochs=epochs, validation_data=(x_test, y_test))
model.save('traffic_recognition.h5')

from sklearn.metrics import accuracy_score
import pandas as pd
y_test = pd.read_csv('Test.csv')
labels = y_test["ClassId"].values
img_paths = y_test["Path"].values
test_data=[]
for path in img_paths:
  image = Image.open(path)
  image = image.resize((30,30))
  test_data.append(np.array(image))
test_data = np.array(test_data)
pred = model.predict_classes(test_data)
#Accuracy with the test data
from sklearn.metrics import accuracy_score
accuracy_score(labels, pred)