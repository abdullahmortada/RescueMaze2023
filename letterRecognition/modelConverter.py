import tensorflow as tf

savedPath = "./training/cp-0014.ckpt"
toSave = "./lite/liteModel.tflite"

converter = tf.lite.TFLiteConverter.from_saved_model(savedPath)
tflite_model = converter.convert()
with open(toSave, 'wb') as f:
    f.write(tflite_model)
