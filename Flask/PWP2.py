from flask import Flask, escape, request, render_template, Response
from robotClass import robot
import time
import socket
import io
import logging
import os
import cv2
import threading
from threading import Condition
# call camera_pi file
from camera_pi import VideoCamera


app=Flask(__name__)
rc = robot()
arrows = [0,0]
# a=1

class NoParsingFilter(logging.Filter):
    def filter(self, record):
        return not record.getMessage().__contains__('log_stream')

with open("loggingfile.txt", "w+") as loggingfile:
    blacklist = ""
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
    rootLogger = logging.getLogger()
    fileHandler = logging.FileHandler("loggingfile.txt")
    fileHandler.setFormatter(logFormatter)
    consoleHandler = logging.StreamHandler()
    fileHandler.addFilter(NoParsingFilter())
    # rootLogger.addFilter(streamFilter())
    rootLogger.addHandler(consoleHandler)
    rootLogger.addHandler(fileHandler)

@app.route('/log_stream')
def log_stream():
    with open("loggingfile.txt", "r") as loggingfile:
        return "".join(loggingfile.readlines()[-25:])

#HOME HTML TEMPLATE
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('home.html')

def gen(camera):
    while True:
        left = arrows[-1]
        right = arrows[-2]
        frame = camera.get_frame(left, right)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# move the robot fwd
@app.route('/fwd', methods=['GET'])
def fwd():
   arrows.append(1)
   rc.forward(0.1, 30)
   return "JUST WORK OK"

# move the robot rev
@app.route('/rev', methods=['GET'])
def rev():
   arrows.append(3)
   rc.reverse(0.1, 30)
   return "JUST WORK OK"

# move the robot left
@app.route('/left', methods=['GET'])
def left():
    arrows.append(2)
    rc.left(0.05)
    return "JUST WORK OK"

# move the robot right
@app.route('/right', methods=['GET'])
def right():
   arrows.append(4)
   rc.right(0.05)
   return "JUST WORK OK"

# run the predetermined course
@app.route('/run')
def run():
    a = request.args.get('a')
    b = request.args.get('b')
    c = request.args.get('c')
    d = request.args.get('d')
    e = request.args.get('e')
    f = request.args.get('f')
    rc.forward(float(a), 15)
    time.sleep(0.5)
    rc.right(float(b))
    time.sleep(0.5)
    rc.forward(float(c), 15)
    time.sleep(0.5)
    rc.reverse(float(d), 15)
    time.sleep(0.5)
    rc.right(float(e))
    time.sleep(0.5)
    rc.forward(float(f), 15)
    return "robot work yes"


app.run(host= '0.0.0.0', port=8080, debug=True, threaded=True)
