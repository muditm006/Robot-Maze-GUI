from flask import Flask, escape, request, render_template, Response
from robotClass import robot
import time
import picamera
import socket
import io
import logging


app = Flask(__name__)
rc = robot()
camera = picamera.camera

#fwd 3, right 0.75, fwd 1.75, rev 0.8, right 0.75, fwd 3.05

@app.route('/streamtest')
def stream():
    with picamera.PiCamera() as camera:
        with picamera.PiCameraCircularIO(camera, splitter_port=2) as stream:
            camera.start_recording(stream, format='mjpeg', splitter_port=2)
            camera.wait_recording(10, splitter_port=2)
            camera.stop_recording(splitter_port=2)

#if the html img src link doesnt work try <img src="{{ url_for('video_feed') }}" width="50%"> instead

@app.route('/')
def home():
    return render_template("home.html")

# move the robot fwd
@app.route('/fwd', methods=['POST'])
def fwd():
    rc.forward(0.1, 30)
    return render_template("home.html")

# move the robot rev
@app.route('/rev', methods=['POST'])
def rev():
    rc.reverse(0.1, 30)
    return render_template("home.html")

# move the robot left
@app.route('/left', methods=['POST'])
def left():
    rc.left(0.05)
    return render_template("home.html")

# move the robot right
@app.route('/right', methods=['POST'])
def right():
    rc.right(0.05)
    return render_template("home.html")

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

# @app.route('/streamlog')
# def terminal():
#     logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
#     rootLogger = logging.getLogger()

#     fileHandler = logging.FileHandler(loggingfile)
#     fileHandler.setFormatter(logFormatter)

#     consoleHandler = logging.StreamHandler()

#     rootLogger.addHandler(consoleHandler)
#     rootLogger.addHandler(fileHandler)


app.run(host= '0.0.0.0', port=8080)
