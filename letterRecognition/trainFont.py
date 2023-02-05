from pathlib import Path
import random
import tensorflow as tf 
from tensorflow.keras import layers

def char_to_num(char):
    if char == "H":
        return 0 
    if char == "S":
        return 1

    return 2

def num_to_char(num):
    if num == 1:
        return "H"
    if num == 2:
        return "S"

    return "U"


data_dir = Path("../../dataFonts/")
images_or = sorted(list(map(str, list(data_dir.glob("*/*.png")))))
labels_or = ["H" for _ in range(14991)] + ["S" for _ in range(14991)] + ["U" for _ in range(14991)]
indices = list(range(len(images_or)))
random.shuffle(indices)
images = []
labels = []

for i in indices:
    images.append(images_or[i])
    labels.append(labels_or[i])

print(labels)
print(images)

batch_size = 16

img_size = 32

train_split = 0.9 
train_samples = int(train_split * len(images))


x_train, y_train = images[:train_samples], labels[:train_samples]
x_dev, y_dev = images[train_samples:], labels[train_samples:]


def encode(im_path, label):
    img = tf.io.read_file(im_path)
    img = tf.io.decode_png(img, channels=1)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize(img, [img_size, img_size])
    img = tf.transpose(img, perm=[1, 0, 2])
    label = char_to_num(label)
    return (img, label)



train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))
train_dataset = (
        train_dataset.map(
            encode, num_parallel_calls=tf.data.experimental.AUTOTUNE
            )
        .batch(batch_size)
        .prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
        )
print(train_dataset)
validation_dataset = tf.data.Dataset.from_tensor_slices((x_dev, y_dev))
validation_dataset = (
        validation_dataset.map(
            encode, num_parallel_calls=tf.data.experimental.AUTOTUNE
            )
        .batch(batch_size)
        .prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
        )


input_img = layers.Input(shape=(img_size,img_size, 1), name="image", dtype="float32")
x = layers.Conv2D(
        32, (3,3), activation="relu",
        kernel_initializer="he_normal",
        padding="same",
        name="Conv1"
        )(input_img)
x = layers.MaxPooling2D((2,2), name="pool1")(x)
x = layers.Conv2D(
        64, (3,3), activation="relu",
        kernel_initializer="he_normal",
        padding="same",
        name="Conv2"
        )(x)
x = layers.MaxPooling2D((2,2), name="pool2")(x)
new_shape=((img_size // 4), (img_size // 4) * 64)
x = layers.Flatten(name="flatten")(x)
x = layers.Dropout(0.2)(x)
x = layers.Dense(64, activation="relu", name="dense1")(x)
x = layers.Dense(3, activation="softmax", name="dense2")(x)
model = tf.keras.Model(input_img, x)
model.compile(
        loss= tf.keras.losses.SparseCategoricalCrossentropy(),
        metrics=['sparse_categorical_accuracy'],
        optimizer='adam'
        )
model.summary()

checkpoint_path = "training/cp-{epoch:04d}.ckpt"
early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=10, restore_best_weights=True
        )

cp_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path,
        save_freq=5*batch_size
        )

model.fit(train_dataset, validation_data=validation_dataset, epochs=60, callbacks=[early_stopping, cp_callback])
