from flask import Flask, escape, request, render_template, Response
from robotClass import robot
import time
from picamera import PiCamera

#maybe???
#https://raspberrypi.stackexchange.com/questions/42759/streaming-raspberry-pi-camera-to-html-webpage-using-picamera-and-flask

# This is the real one:
# https://blog.miguelgrinberg.com/post/video-streaming-with-flask

app = Flask(__name__)
rc = robot()
#fwd 3, right 0.75, fwd 1.75, rev 0.8, right 0.75, fwd 3.05
@app.route('/plswork')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    #Create an in-memory stream
    my_stream = BytesIO()
    camera = PiCamera()
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    camera.capture(my_stream, 'jpeg')

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
    
app.run(host= '0.0.0.0', port=8080)
