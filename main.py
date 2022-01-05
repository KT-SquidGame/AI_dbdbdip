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
from threading import Thread

app = Flask(__name__)
CORS(app)

global result
global answer
global start_condition
global frame
start_condition = False
result = '0'
answer = '0'
model = load_model('keras_model.h5')


camera = cv2.VideoCapture(0)
success, frame = camera.read()


def timer():
    global start_condition
    global frame
    time_limit = time.time() + 4
    while time.time() < time_limit:
        remain_time = round(time_limit - time.time())
        cv2.putText(frame, str(remain_time), (200, 100), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 0, 0), 2)
    start_condition = True
    return


def gen_frames():
    global result
    global answer
    global start_condition
    start_condition = False
    global frame

    camera = cv2.VideoCapture(0)
    
    answer = random.randint(0,3) # 정답 label
    answer = str(answer+1)
    thread = Thread(target=timer, args=())
    thread.start()

    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # time.sleep(4)
            if start_condition == True :
                cv2.imwrite('./image/image.png',frame)
                
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
        
                
                if (answer==np.argmax(prediction[0])) or np.argmax(prediction[0])==3: #실패한 경우
                    result = '1'
                else:
                    result = '2'
                return
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame1 = buffer.tobytes()
            yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n')




# def video_print():
#     #global end_time
#     camera = cv2.VideoCapture(0)
    
#     while True:
#         success, frame = camera.read()  # read the camera frame
#         if not success:
#             break
#         else:   
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




@app.route("/", methods=['GET', 'POST'])
def index():
   return render_template('index.html')

# @app.route('/video_print_out')
# def video_print_out():
#     return Response(video_print(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/result')
def rr():
    global result
    return result

@app.route('/answer')
def answer_function():
    global answer
    return answer

if __name__ == '__main__':
    app.run(debug=False, host="172.30.1.16", port=5200)
    #app.run(debug=False, host="127.0.0.1", port=5200)