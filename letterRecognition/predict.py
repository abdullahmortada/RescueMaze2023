import tensorflow as tf 
import cv2 

# import tensorflow.keras.backend as K
# # to set the image order
# K.set_image_data_format('channels_first')

img_size = 128

def char_to_num(char):
    if char == "H":
        return 0 
    if char == "I":
        return 1

    return 2

def num_to_char(num):
    if num == 1:
        return "H"
    if num == 2:
        return "I"

    return "U"

model = tf.keras.models.load_model('./training/cp-0014.ckpt')
# pred_mod = tf.keras.models.Model(model.get_layer(name="image").input, model.get_layer(name="dense2").output)
def filter(path):
    img = tf.io.read_file(path)
    img = tf.io.decode_png(img, channels=1)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.transpose(img, perm=[1, 0, 2])
    img = tf.reshape(img, (1, 32,32,1))
    return img

img = cv2.imread("./newS.png")
img = cv2.resize(img, (32,32))
img = 255 - img
cv2.imwrite('./newS.png', img)
# img = cv2.imread("/home/abdullah/Downloads/U.png")
# img = cv2.resize(img, (32,32))
# cv2.imwrite('./newU.png', img)
# img = cv2.imread("/home/abdullah/Downloads/H3.png")
# img = cv2.resize(img, (128,128))
# cv2.imshow('3', img)
# cv2.imwrite('./newH3.png', img)
# cv2.waitKey(0)
imgs = [filter("./newS.png")]
dset = tf.data.Dataset.from_tensor_slices(imgs)

preds = model.predict(dset)
print(preds)
