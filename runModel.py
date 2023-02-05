import tensorflow as tf 
import cv2 

def filter(img):
    img = tf.convert_to_tensor(img)
    img = tf.image.convert_image_dtype(img, tf.float32)
    # img = tf.transpose(img, perm=[1, 0, 2])
    img = tf.reshape(img, (1, 128,128,1))
    return img

model_path = "./lite/liteModel.tflite"

interpreter = tf.lite.Interpreter(model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

#get input 
img = cv2.imread("./im.png", cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (128, 128))
img = cv2.transpose(img)
img = filter(img)

interpreter.set_tensor(input_details[0]['index'], img)
interpreter.invoke()
print(interpreter.get_tensor(output_details[0]['index']))
