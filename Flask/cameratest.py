import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

PAGE="""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Random</title>
</head>
<style>
    html, body { height:100%; margin:0; padding:0 }
    div { position:fixed; border: 1px solid #000; border-color: black; width:50%; height:50% }
    #NW { top:0;   left:0   }
    #NE { top:0;   left:50%; }
    #SW { top:50%; left:0;   }
    #SE { top:50%; left: 50% }
    .grid {
        display: flex;                       /* establish flex container */
        flex-wrap: wrap;                     /* enable flex items to wrap */
        justify-content: space-around;
        left: 0%;
        top: 50%;
       }

.btn-group {
          flex: 0 0 32%;
          background-color: #d93ddb;  /* Green background */
          border: 1px solid black; /* Green border */
          color: white; /* White text */
          padding: 10px 24px; /* Some padding */
          cursor: pointer; /* Pointer/hand icon */
          float: none; /* Float the buttons side by side */
          font-size: 50px;
          box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
          font-family: calibri;
          width: 33%;
          height: 33%;
          <!--resize: horizontal;-->
          overflow: auto;
          position: absolute;
        }
        .btn-empty {
          flex: 0 0 32%;
          background-color: #ffffff;  /* Green background */
          border: 1px solid black; /* Green border */
          color: white; /* White text */
          padding: 10px 24px; /* Some padding */
          cursor: pointer; /* Pointer/hand icon */
          float: none; /* Float the buttons side by side */
          font-size: 50px;
          box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
          font-family: calibri;
          width: 33%;
          height: 33%;
          <!--resize: horizontal;-->
          overflow: auto;
          position: absolute;
        }

        .btn-fwd {
            left: 33%;
           }

        .btn-rev {
            left: 33%;
            top: 66%;
           }

        .btn-left {
            top: 33%;
            left:0%
           }

        .btn-right {
            left: 66%;
            top: 33%;
           }

        .btn-play {
            left: 33%;
            top: 33%;
           }

    .btn-group button:not(:last-child) {
      border-right: none; /* Prevent double borders */
    }

    /* Clear floats (clearfix hack) */
    .btn-group:after {
      content: "";
      clear: both;
      display: table;
    }

    /*background color on hover */
    .btn-group button:hover {
      background-color: #00bfff;
    }
</style>
<body>
    <div id="NW"></div>
     <img src="stream.mjpg" width="50%" height="50%"></div>
    <div id="NE"></div>
    <div id="SE"></div>​
    <div id="SW"></div>
        <div class="grid">
        <button class="btn-group btn-fwd">Forward</button>
        <button class="btn-group btn-left">Left</button>
        <button class="btn-group btn-play">Play</button>
        <button class="btn-group btn-right">Right</button>
        <button class="btn-group btn-rev">Backwards</button>
        </div></div>
</body>
</html>


"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='1280x720', framerate=60) as camera:
    output = StreamingOutput()
    camera.rotation = 180
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('192.168.1.116', 8080)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
