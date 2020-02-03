from __future__ import absolute_import, division, print_function, unicode_literals
import compile_training_data
import tensorflow as tf
from tensorflow import keras
import tensorflow_datasets as tfds
import tensorflow_hub as hub
import numpy as np

print("Version: ", tf.__version__)
print("Eager mode: ", tf.executing_eagerly())
print("Hub version: ", hub.__version__)
print("GPU is", "available" if tf.config.experimental.list_physical_devices("GPU") else "NOT AVAILABLE")

full_data = compile_training_data.get_dataset()
train_tuple = full_data[0]
test_tuple = full_data[1]


train_dataset = tf.data.Dataset.from_tensor_slices((train_tuple[0], train_tuple[1]))
test_dataset = tf.data.Dataset.from_tensor_slices((test_tuple[0], test_tuple[1]))


embedding = "https://tfhub.dev/google/tf2-preview/gnews-swivel-20dim/1"
hub_layer = hub.KerasLayer(embedding, input_shape=[], dtype=tf.string, trainable=True)


model = tf.keras.Sequential()
model.add(hub_layer)
model.add(tf.keras.layers.Dense(16, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

print(model.summary())

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_dataset.shuffle(len(train_tuple[0])).batch(300),
                    epochs=20,
                    validation_data=test_dataset.batch(129),
                    verbose=1)

results = model.evaluate(test_dataset.batch(300), verbose=2)

for name, value in zip(model.metrics_names, results):
    print("%s: %.3f" % (name, value))
