# -*- coding: utf-8 -*-
"""Alien_Vs_Predator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Y1zzYf4RcGjHbnLYkd1GTvcL-hmkp2kS
"""

!pip install kaggle

!mkdir .kaggle

import json
token = {'username':,'key':}
with open('/content/.kaggle/kaggle.json', 'w') as file:
    json.dump(token, file)

!cp /content/.kaggle/kaggle.json ~/.kaggle/kaggle.json

!kaggle config set -n path -v{/content}

!chmod 600 /root/.kaggle/kaggle.json

!kaggle datasets list -s Alien

!kaggle datasets download -d pmigdal/alien-vs-predator-images -p /content

!unzip \*.zip

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D,Flatten,Dense

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32,(3,3),activation='relu',input_shape = (150,150,3)),
    tf.keras.layers.MaxPooling2D(2,2),
    
    tf.keras.layers.Conv2D(64,(3,3),activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    
    tf.keras.layers.Conv2D(64,(3,3),activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    
     tf.keras.layers.Flatten(),
     tf.keras.layers.Dense(units=32,activation='relu'),
     tf.keras.layers.Dense(units=1,activation='sigmoid')
])

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

model.summary()

from keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=0.3)
test_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory('data/train/',
                                               target_size=(150, 150),
                                               batch_size=32,
                                               class_mode='binary')
validation_generator = test_datagen.flow_from_directory('data/validation/',
                                                target_size=(150, 150),
                                               batch_size=32,
                                               class_mode='binary',
                                               shuffle=False)

history = model.fit_generator(train_generator,
                             steps_per_epoch=300,
                             epochs=10,
                             validation_data=validation_generator,
                             validation_steps=200)

train_generator.class_indices

import numpy as np
from keras.preprocessing import image
test_image= image.load_img('data/validation/predator/1.jpg'
                           ,target_size =(150,150))


import matplotlib.pyplot as plt
plt.figure(figsize=(10,10))
plt.imshow(test_image)


test_image = image.img_to_array(test_image)
test_image=np.expand_dims(test_image,axis=0)
test_image=test_image.reshape(1,150,150,3)
result = model.predict(test_image)

if result[0][0] == 0:
    prediction = 'Alien'
else:
    prediction = 'Predator'

print(f'Predicted is {prediction}')



