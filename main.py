from flask import Flask, render_template, Response
import cv2
from numpy.core.multiarray import result_type
import tensorflow
import tensorflow.keras
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import time
import random
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

global result
result = '0'

def gen_frames():
    global result
    
    camera = cv2.VideoCapture(0)
    model = load_model('keras_model.h5')
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            time.sleep(10)
            
            cv2.imwrite('./image/image.png',frame)
            answer = random.randint(0,3) # 정답 label
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            image = Image.open('./image/image.png')
            size = (224, 224)
            image = ImageOps.fit(image, size, Image.ANTIALIAS)
            
            image_array = np.asarray(image)
            normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image_array
            
            # run the inference
            prediction = model.predict(data)
            print(prediction[0])
            print(np.argmax(prediction[0]))
    
            
            if (answer==np.argmax(prediction[0])) or np.argmax(prediction[0])==4: #실패한 경우
                result = '1'
            else:
                result = '2'
            
            break
            # ret, buffer = cv2.imencode('.jpg', frame)
            # frame = buffer.tobytes()
            # yield (b'--frame\r\n'
            # b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        



def video_print():
    #global end_time
    camera = cv2.VideoCapture(0)
    
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:   
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




@app.route("/", methods=['GET', 'POST'])
def index():
   return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_print_out')
def video_print_out():
    return Response(video_print(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/result')
def rr():
    global result
    return result

if __name__ == '__main__':
    app.run(debug=False, host="127.0.0.1", port=5200)