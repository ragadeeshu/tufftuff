import os
import uuid
import _thread
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import json
import connections
import sys

from command_queue import CommandQueue

if len(sys.argv) > 1 and sys.argv[1] == "--real":
    type = 'real'
else:
    type = 'dummy'
print(type)
clients = connections.Connections()
commands = CommandQueue(clients, type)

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(request):
        request.render("index.html")

class WSHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        clients.add_conneciton(self)
        self.write_message(json.dumps(commands.get_state()))

    def on_message(self, message):
        parsed_json = json.loads(message)
        commands.queue(parsed_json)

    def on_close(self):
        print('connection closed')
        clients.close_connection(self)

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([(r'/ws', WSHandler), (r'/', IndexHandler)], **settings)


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    myIP = socket.gethostbyname(socket.gethostname())
    print('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.instance().start()
