#%% import some useful modules
import h5py
import numpy as np
from keras import layers
from keras.layers import Input, Dense, Activation, BatchNormalization
from keras.models import Model, load_model
from keras.utils import layer_utils
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
from keras.utils import plot_model
from k_utils import *

import keras.backend as K


#%% Load datas
X_train, Y_train, X_test, Y_test = load_dataset()

print ("number of training examples = " + str(X_train.shape[0]))
print ("number of test examples = " + str(X_test.shape[0]))
print ("X_train shape: " + str(X_train.shape))
print ("Y_train shape: " + str(Y_train.shape))
print ("X_test shape: " + str(X_test.shape))
print ("Y_test shape: " + str(Y_test.shape))


#%% 
def model(input_shape):
    # 4 hidden layers
    # each layer has 11 hidden units.

    X_input = Input(input_shape)

    X = Dense(11, input_shape=(7,), init="uniform", name='fc0')(X_input)
    X = BatchNormalization(axis=0, name = 'bn0')(X)
    X = Activation("relu")(X)

    X = Dense(11, init="uniform", name='fc1')(X)
    X = BatchNormalization(axis=0, name = 'bn1')(X)
    X = Activation("relu")(X)

    X = Dense(11, init="uniform", name='fc2')(X)
    X = BatchNormalization(axis=0, name = 'bn2')(X)
    X = Activation("relu")(X)

    X = Dense(11, init="uniform", name='fc3')(X)
    X = BatchNormalization(axis=0, name = 'bn3')(X)
    X = Activation("relu")(X)

    X = Dense(1, init="uniform", name='fc')(X)
    X = BatchNormalization(axis=0, name = 'bn0')(X)
    X = Activation("sigmoid")(X)

    model = Model(inputs = X_input, outputs = X, name="DoS_detection_Model")
    return model


#%% train and test
DoS_detection_model = model((7))

DoS_detection_model.compile(optimizer='Adam', loss='mean_squared_logarithmic_error', metrics = ["accuracy"])
DoS_detection_model.fit(x = X_train, y = Y_train, epochs = 40, batch_size = 16)

preds = DoS_detection_model.evaluate(x = X_test, y = Y_test)

print ("Loss = " + str(preds[0]))
print ("Test Accuracy = " + str(preds[1]))

#%% Summerize and Save model
DoS_detection_model.summary()
plot_model(DoS_detection_model, to_file='DoS_detection_model.png')
SVG(model_to_dot(DoS_detection_model).create(prog='dot', format='svg'))

DoS_detection_model.save_weights("./DoS_detection_model.h5")