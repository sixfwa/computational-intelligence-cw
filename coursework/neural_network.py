import matplotlib.pyplot as plt
from tools import load_data
from keras import models, layers
import numpy as np

# Load the training data
training_data, training_targets = load_data("cwk_train")
# Load the test data
test_data, test_targets = load_data("cwk_test")

# Normalising the data
mean = training_data.mean(axis=0)
training_data -= mean
std = training_data.std(axis=0)
training_data /= std

test_data -= mean
test_data /= std

# Building the Network


def build_model():
    model = models.Sequential()
    model.add(layers.Dense(64, activation='relu',
                           input_shape=(training_data.shape[1],)))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    return model


# K-fold validation
k = 4
num_val_samples = len(training_data) // k
num_epochs = 500
all_mae_histories = []

for i in range(k):
    print('Processing Fold #{}'.format(i))
    # Prepares the validation data: data from partition #k
    val_data = training_data[i * num_val_samples: (i + 1) * num_val_samples]
    val_targets = training_targets[i *
                                   num_val_samples: (i + 1) * num_val_samples]

    partial_train_data = np.concatenate(
        [training_data[:i * num_val_samples],
         training_data[(i + 1) * num_val_samples:]],
        axis=0
    )

    partial_train_targets = np.concatenate(
        [training_targets[:i * num_val_samples],
         training_targets[(i + 1) * num_val_samples:]],
        axis=0
    )

    model = build_model()
    history = model.fit(partial_train_data, partial_train_targets,
                        validation_data=(val_data, val_targets),
                        epochs=num_epochs, batch_size=1, verbose=0)
    mae_history = history.history['val_mean_absolute_error']
    all_mae_histories.append(mae_history)

average_mae_history = [
    np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)
]


def smooth_curve(points, factor=0.9):
    smoothed_points = []
    for point in points:
        if smoothed_points:
            previous = smoothed_points[-1]
            smoothed_points.append(previous * factor + point * (1 - factor))
        else:
            smoothed_points.append(point)
    return smoothed_points


smooted_mae_history = smooth_curve(average_mae_history[10:])
plt.plot(range(1, len(smooted_mae_history) + 1), smooted_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()

# epoch 76