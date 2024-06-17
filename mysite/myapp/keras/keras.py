from sklearn.preprocessing import StandardScaler # type: ignore 
from sklearn.model_selection import train_test_split # type: ignore 
import tensorflow as tf
from tensorflow.keras.models import Sequential  # type: ignore 
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization # type: ignore 
from tensorflow.keras import Input # type: ignore 
import keras_tuner as kt
import numpy as np
from django.conf import settings

# read data and drop identification columns
data = settings.DATAFRAME
data = data.drop(columns=['CP_numero', 'CP_codigo', 'CP', 'incidencia'])
attributes = data.drop(columns=['meses']).values
target = data['meses'].values
target = np.array(target)

# scale data and build model
scaler = StandardScaler()
attributes_scaled = scaler.fit_transform(attributes)

# data augmentation by adding noise


def augment_data(data, noise_level=0.1):
    noise = np.random.normal(0, noise_level, data.shape)
    return data + noise


attributes_scaled_augmented = augment_data(attributes_scaled)
# combine original and augmented data
attributes_combined = np.vstack(
    (attributes_scaled, attributes_scaled_augmented))
target_combined = np.concatenate([target, target])

# split data into training and test sets
attributes_train, attributes_test, target_train, target_test = train_test_split(
    attributes_combined, target_combined, test_size=0.2)

# detect if TPU is available
try:
    resolver = tf.distribute.cluster_resolver.TPUClusterResolver()  # TPU detection
    tf.config.experimental_connect_to_cluster(resolver)
    tf.tpu.experimental.initialize_tpu_system(resolver)
    strategy = tf.distribute.TPUStrategy(resolver)
    print('Running on TPU')
except ValueError:
    # if TPU not available, fallback to GPU or CPU
    # this works for single-GPU or multi-GPU setups
    strategy = tf.distribute.MirroredStrategy()
    print('Running on GPU' if tf.config.list_physical_devices(
        'GPU') else 'Running on CPU')


# kerastuner expects a class with a build method
class RegressionHyperModel(kt.HyperModel):
    def build(self, hp):
        with strategy.scope():
            model = Sequential()
            # add input layer with Input:
            model.add(Input(shape=(attributes_train.shape[1],)))
            # hidden layer tuned with kerastuner and regularization (elastic net) to avoid overfitting
            model.add(Dense(units=hp.Int('units1', min_value=16, max_value=128, step=4),
                            activation='relu',
                            kernel_regularizer=tf.keras.regularizers.l1_l2(l1=hp.Float('l1_1', 1e-5, 1e-1, sampling='LOG'),
                                                                           l2=hp.Float('l2_1', 1e-5, 1e-1, sampling='LOG'))))
            # normalize the input of the following layer
            model.add(BatchNormalization())
            # dropout layer to avoid overfitting
            model.add(Dropout(rate=hp.Float(
                'dropout1', min_value=0.2, max_value=0.5, step=0.1)))

            # hidden layer tuned with kerastuner and regularization to avoid overfitting
            model.add(Dense(units=hp.Int('units2', min_value=16, max_value=128, step=4),
                            activation='relu',
                            kernel_regularizer=tf.keras.regularizers.l1_l2(l1=hp.Float('l1_1', 1e-5, 1e-1, sampling='LOG'),
                            l2=hp.Float('l2_1', 1e-5, 1e-1, sampling='LOG'))))
            # normalize the input of the following layer
            model.add(BatchNormalization())
            # dropout layer to avoid overfitting
            model.add(Dropout(rate=hp.Float(
                'dropout2', min_value=0.2, max_value=0.5, step=0.1)))

            # output layer (adam optimizer with default inertia works better than custom)
            model.add(Dense(1, activation='linear'))
            model.compile(optimizer="adam", loss='mean_squared_error')
        return model


# instantiate the hypermodel
hypermodel = RegressionHyperModel()

# instantiate the tuner (no directory specified so it will be saved in the current one)
tuner = kt.BayesianOptimization(
    hypermodel,
    objective='val_loss',
    max_trials=20,
    project_name='regression_tuning'
)

# perform the search
tuner.search(attributes_train, target_train, epochs=50,
             validation_split=0.2, batch_size=32)

# get the best hyperparameters
best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]

# build the model with the best hyperparameters (wrapped to avoid warning)
model = tuner.hypermodel.build(best_hps)

# train the model
history = model.fit(attributes_train, target_train,
                    epochs=500, validation_split=0.2, batch_size=32)

# save the model
model.save('model.keras')
