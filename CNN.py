import pandas as pd
import numpy as np
import os
import keras
import keras.backend as K
import matplotlib.pyplot as plt
from keras.layers import Dense,GlobalAveragePooling2D
from keras.applications import MobileNetV2
from keras.preprocessing import image
from keras.applications.mobilenet import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from sklearn.metrics import confusion_matrix,plot_confusion_matrix

model = Sequential()
model.add(Convolution2D(32, (3, 3), input_shape=(50, 50, 3), padding='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(48, (3, 3), padding='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(64, (3, 3), padding='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(96, (3, 3), padding='valid'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(256))
model.add(Dropout(0.25))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(3))
model.add(Activation('softmax'))
train_datagen=ImageDataGenerator(preprocessing_function=preprocess_input) #included in our dependencies
test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
train_generator=train_datagen.flow_from_directory('N_train',
                                                 target_size=(50,50),
                                                 color_mode='rgb',
                                                 batch_size=32,
                                                 class_mode='categorical',
                                                 shuffle=True)
validation_generator = test_datagen.flow_from_directory('N_test',
                                                        target_size=(50, 50),
                                                        batch_size=32,
                                                        class_mode='categorical'
                                                        ,shuffle=False)

model.compile(optimizer='Adam',loss='categorical_crossentropy',metrics=['accuracy'])
# Adam optimizer
# loss function will be categorical cross entropy
# evaluation metric will be accuracy

step_size_train=train_generator.n//train_generator.batch_size
step_size_val=validation_generator.n//validation_generator.batch_size
model.fit_generator(generator=train_generator,
                   steps_per_epoch=step_size_train, validation_data=validation_generator,
                    validation_steps=step_size_val,
                   epochs=7)

Y_pred = model.predict_generator(validation_generator, validation_generator.n // validation_generator.batch_size + 1)
y_pred = np.argmax(Y_pred, axis=1)
print(confusion_matrix(validation_generator.classes, y_pred))