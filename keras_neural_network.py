from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Input, MaxPooling2D, Conv2D, BatchNormalization, Activation
from keras.optimizers import Adam

import numpy as np

import os

class KerasConvNeuralNetwork:

    def __init__(self, input_shape, hidden_level_units):

        self.model = None
        self.input_shape = input_shape
        self.hidden_level_units = hidden_level_units

        self.weights_file = 'keras_conv_neural_network_weights.h5'
        self.weights_file_backup = 'keras_conv_neural_network_weights_backup.h5'


    def createModel(self):

        self.LeNet5Custom()

    def LeNet5Custom(self):

        input_layer = Input(self.input_shape)

        # layer 1: CONV -> BN -> RELU Block
        layer_1 = Conv2D(6, (5, 5), strides=(1, 1), name='conv0')(input_layer)
        layer_1 = BatchNormalization(axis=3, name='bn0')(layer_1)
        layer_1 = Activation('relu')(layer_1)

        # layer 2: MAXPOOL
        layer_2 = MaxPooling2D((2, 2), strides=(2, 2), name='max_pool0')(layer_1)

        # layer 3: CONV -> BN -> RELU Block
        layer_3 = Conv2D(16, (5, 5), strides=(1, 1), name='conv1')(layer_2)
        layer_3 = BatchNormalization(axis=3, name='bn1')(layer_3)
        layer_3 = Activation('relu')(layer_3)

        # layer 4: MAXPOOL
        layer_4 = MaxPooling2D((2, 2), strides=(2, 2), name='max_pool0')(layer_3)

        # layer 5: Fully connected layer
        layer_5 = Dense(120, kernel_initializer='normal')(layer_4)

        # layer 6: Fully connected layer
        layer_6 = Dense(84, kernel_initializer='normal')(layer_5)

        # output
        output = Dense(1, kernel_initializer='normal')(layer_6)

        # define model
        self.model = Model(inputs=input_layer, outputs=output)

        optimizer = Adam(lr=0.2)

        self.model.compile(optimizer=optimizer, loss='mse')
        self.model.summary()


    def loadWeights(self):

        if os.path.isfile(self.weights_file) == False:
            return

        self.model.load_weights(self.weights_file)


    def saveWeights(self):

        self.model.save_weights(self.weights_file)
        self.model.save_weights(self.weights_file_backup)


    def trainModel(self, trainX, trainY, epochs, batch_size = None):

        # fit model
        self.model.fit(x=trainX,
                  y=trainY,
                  epochs=epochs,
                       batch_size=batch_size,
                  verbose=2,
                  shuffle=False)

    def trainModelAfterOneGame(self, train_data, batch_size, epochs):

        input = []
        output = []
        size = len(train_data)

        if size == 0: return

        for data in train_data:
            input.append(data[0])
            output.append(data[1])

        trainX = np.asarray(input).reshape(size, 1, -1)
        trainY = np.asarray(output).reshape(size, 1, -1)

        self.trainModel(trainX, trainY, epochs, batch_size)


    def predictWithModel(self, X):

        return self.model.predict(X)

