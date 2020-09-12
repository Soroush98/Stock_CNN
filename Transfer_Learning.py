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
from keras.models import Model
from keras.optimizers import Adam
from sklearn.metrics import confusion_matrix,plot_confusion_matrix

base_model=MobileNetV2(weights='imagenet',include_top=False)

x=base_model.output
x=GlobalAveragePooling2D()(x)
x=Dense(1024,activation='relu')(x)
x=Dense(1024,activation='relu')(x) #dense layer 2
x=Dense(512,activation='relu')(x) #dense layer 3
preds=Dense(2,activation='softmax')(x)
model=Model(inputs=base_model.input,outputs=preds)
# for layer in model.layers:
#     layer.trainable=False
train_datagen=ImageDataGenerator(preprocessing_function=preprocess_input) #included in our dependencies
test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
train_generator=train_datagen.flow_from_directory('File3',
                                                 target_size=(50,50),
                                                 color_mode='rgb',
                                                 batch_size=32,
                                                 class_mode='categorical',
                                                 shuffle=True)
validation_generator = test_datagen.flow_from_directory('Test3',
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
                   epochs=10)

Y_pred = model.predict_generator(validation_generator, validation_generator.n // validation_generator.batch_size+1)
y_pred = np.argmax(Y_pred, axis=1)
print(confusion_matrix(validation_generator.classes, y_pred))
