import numpy as np
import tflite_runtime.interpreter as tflite
import cv2 
import findLetters

def filter(img):
    img = cv2.resize(img, (32, 32))
    img = cv2.transpose(img)
    img = img.astype(np.float32)
    img = img.reshape((1, 32, 32, 1))
    return img

model_path = "./lite/liteModel.tflite"

def runModel(img):
    interpreter = tflite.Interpreter(model_path)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    img = filter(img)
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_details[0]['index'])
    predNums = np.argmax(preds, axis=-1)
    return predNums

img = cv2.imread("/home/abdullah/Downloads/H2.jpg", cv2.IMREAD_GRAYSCALE)
img = findLetters.findLetters(img)
img = cv2.resize(img, (32, 32))
img = cv2.transpose(img)

print(runModel(img))
