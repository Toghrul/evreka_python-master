# Equvalent of "tail -f" as a webpage using websocket
# Usage: webtail.py PORT FILENAME
# Tested with tornado 2.1

# Thanks to Thomas Pelletier for it's great introduction to tornado+websocket
# http://thomas.pelletier.im/2010/08/websocket-tornado-redis/

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import sys
import os

PORT = int(sys.argv[1])
FILENAME = sys.argv[2]
FILENAME_2 = sys.argv[3]

REQUEST_LISTENERS = []
INPUT_LISTENERS = []

TEMPLATE = """
<!DOCTYPE>
<html>
<head>
    <title>WebTail: %s</title>
</head>
<body>
    <div id="file"></div>
    <script type="text/javascript" charset="utf-8">
        function write_line(l) {
            document.getElementById('file').innerHTML += '<p>' + l + '</p>';
        }

        if ("MozWebSocket" in window) {
            WebSocket = MozWebSocket;
        }

        if (WebSocket) {
            var ws = new WebSocket("ws://%s/request_logs/");
            ws.onopen = function() {};
            ws.onmessage = function (evt) {
                write_line(evt.data);
            };
            ws.onclose = function() {};
        } else {
            alert("WebSocket not supported");
        }
    </script>
</body>
</html>
"""

tailed_file_input = open(FILENAME)
tailed_file_input.seek(os.path.getsize(FILENAME))

tailed_file_request = open(FILENAME_2)
tailed_file_request.seek(os.path.getsize(FILENAME_2))



def check_file():
    global tailed_file_input
    where = tailed_file_input.tell()
    line = tailed_file_input.readline()
    if not line:
        tailed_file_input.seek(where)
    else:
        print "File refresh:"
        for element in INPUT_LISTENERS:
            element.write_message(line)
        print "Current Bytes:", tailed_file_input.tell()

    if tailed_file_input.tell() >= 1024*1024:
        tailed_file_input.close()
        print "File switch happened :)"
        tailed_file_input = open(FILENAME)
        tailed_file_input.seek(os.path.getsize(FILENAME))
        
    global tailed_file_request
    where = tailed_file_request.tell()
    line = tailed_file_request.readline()
    if not line:
        tailed_file_request.seek(where)
    else:
        print "File refresh:"
        for element in REQUEST_LISTENERS:
            element.write_message(line)
        print "Current Bytes:", tailed_file_request.tell()

    if tailed_file_request.tell() >= 1024*1024:
        tailed_file_request.close()
        print "File switch happened :)"
        tailed_file_request = open(FILENAME_2)
        tailed_file_request.seek(os.path.getsize(FILENAME_2))


class RequestTailHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print "WebSocket open"
        REQUEST_LISTENERS.append(self)

    def on_message(self, message):
        pass

    def on_close(self):
        print "WebSocket close"
        try:
            REQUEST_LISTENERS.remove(self)
        except:
            pass

    def check_origin(self, origin):
        return True

class InputTailHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print "WebSocket open"
        INPUT_LISTENERS.append(self)

    def on_message(self, message):
        pass

    def on_close(self):
        print "WebSocket close"
        try:
            INPUT_LISTENERS.remove(self)
        except:
            pass

    def check_origin(self, origin):
        return True

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(TEMPLATE % (FILENAME, self.request.host))


application = tornado.web.Application([
    #(r'/', MainHandler),
    (r'/request_logs/', RequestTailHandler),
    (r'/input_logs/', InputTailHandler),
])

if __name__ == '__main__':
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(PORT)

    tailed_callback = tornado.ioloop.PeriodicCallback(check_file, 500)
    tailed_callback.start()

    io_loop = tornado.ioloop.IOLoop.instance()
    try:
        io_loop.start()
    except SystemExit, KeyboardInterrupt:
        io_loop.stop()
        tailed_file_request.close()
        tailed_file_input.close()