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
model = load_model('keras_model.h5') #학습 모델 불러오기

camera = cv2.VideoCapture(1) #카메라 설정
success, frame = camera.read() #카메라 읽어오기


def timer(): #사진 촬영을 위한 타이머 함수 구현
    global start_condition
    global frame
    time_limit = time.time() + 4
    while time.time() < time_limit:
        remain_time = round(time_limit - time.time())
        cv2.putText(frame, str(remain_time), (200, 100), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 0, 0), 2)
    start_condition = True
    return


def gen_frames(): #동영상을 읽어와서 AI 모델을 적용하여 결과를 반환하는 함수 구현
    global result
    global answer
    global start_condition
    start_condition = False
    global frame

    camera = cv2.VideoCapture(1) #카메라 설정
    
    answer = random.randint(1,3) #정답 label random 생성
    answer = str(answer)
    thread = Thread(target=timer, args=()) #타이머 함수 실행을 위한 Thread 불러오기
    thread.start() #Thread 함수 호출

    while True:
        success, frame = camera.read() #카메라 읽어오기
        if not success: 
            break
        else:
            # time.sleep(4)
            if start_condition == True :
                cv2.imwrite('./image/image.png',frame) #사진 촬영
                
                data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32) #teachable machine으로 생성한 모델에 적용하기 위한 data format 생성
                image = Image.open('./image/image.png') #사진 불러오기
                size = (224, 224)
                image = ImageOps.fit(image, size, Image.ANTIALIAS)
                
                image_array = np.asarray(image)
                normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
                data[0] = normalized_image_array
                
                # run the inference
                prediction = model.predict(data) #학습 모델 실행
                print(prediction[0]) #클래스 예측 값
                print(np.argmax(prediction[0])) #Classification class 값 반환
        
                
                if (answer==str(np.argmax(prediction[0])+1)) or np.argmax(prediction[0])==3: #실패한 경우
                    #time.sleep(1)
                    result = '1'
                else:
                    #time.sleep(1)
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
    #app.run(debug=False, host="172.30.1.16", port=5200)
    app.run(debug=False, host="127.0.0.1", port=5200)