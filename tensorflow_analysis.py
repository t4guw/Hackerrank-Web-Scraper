from __future__ import absolute_import, division, print_function, unicode_literals
import compile_training_data
import tensorflow as tf
from tensorflow import keras
import tensorflow_datasets as tfds
import tensorflow_hub as hub
import numpy as np

# print("Version: ", tf.__version__)
# print("Eager mode: ", tf.executing_eagerly())
# print("Hub version: ", hub.__version__)
# print("GPU is", "available" if tf.config.experimental.list_physical_devices("GPU") else "NOT AVAILABLE")

full_data = compile_training_data.get_dataset()

train_tuple = full_data[0]
test_tuple = full_data[1]

# train_dataset = tf.data.Dataset.from_tensor_slices((train_tuple[0], train_tuple[1]))
lens = []
for i in range(len(train_tuple)):
    lens.append(len(train_tuple[0][i]))
lens = np.array(lens)

print(lens.max(), lens.min(), lens.mean(), len(lens > 300))
print('\n\n\n', type(train_tuple[0][10]), "-->", type(train_tuple[1]))

train_data = tf.data.Dataset.from_tensor_slices((train_tuple[0], train_tuple[1]))
test_data = tf.data.Dataset.from_tensor_slices((test_tuple[0], test_tuple[1]))

print(tf.shape(train_data))
print(tf.shape(test_data))
exit()

embedding = "https://tfhub.dev/google/tf2-preview/gnews-swivel-20dim/1"
model = keras.Sequential()
model.add(keras.layers.Embedding(4708, 16))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation=tf.nn.relu))
model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

model.summary()



model.compile(optimizer='adam', loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), metrics=['accuracy'])

history = model.fit(train_data.shuffle(10000).batch(512), 
                    train_tuple[1], 
                    epochs=1000, 
                    batch_size=32, 
                    validation_data=(test_data, test_tuple[1]), 
                    verbose=1)

results = model.evaluate(test_data, test_tuple[1])
print(results)
