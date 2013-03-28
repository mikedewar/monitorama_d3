import tornado
import json
import os
import tornado.web
import tornado.websocket
import tornado.options
import logging


class EchoWebSocket(tornado.websocket.WebSocketHandler):

    # this websocket is opened by the client

    def open(self):
        print "WebSocket opened"
        global websocket_callbacks
        # add the write_message handler to the socket list
        websocket_callbacks.append(self)

    def on_message(self, message):
        # log anything that gets sent by the client 
        #(not expecting anything)
        logging.info(message)

    def on_close(self):
        global websocket_callbacks
        print websocket_callbacks.pop(websocket_callbacks.index(self))
        print "WebSocket closed"

class PutHandler(tornado.web.RequestHandler):
    def post(self):
        msg = self.request.body
        # call each socket's .write_message() handler
        global data_buffer
        data_buffer.append(json.loads(msg))
        print len(data_buffer)
        if len(data_buffer) == 5:
            logging.info('sending buffer to %s websockets'%len(websocket_callbacks))
            for callback in websocket_callbacks:
                callback.write_message(json.dumps(data_buffer))
            # empty the buffer
            data_buffer = []

class PingHandler(tornado.web.RequestHandler):
    def get(self):
        # this endpoint only for sanity checking
        self.finish('pong')

class TalkHandler(tornado.web.RequestHandler):
    # render the talk
    def get(self):
        self.render('talk.html')

class BasicHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('basic.html')

class CirclesHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('circles.html')

class Circles1Handler(tornado.web.RequestHandler):
    def get(self):
        self.render('circles1.html')

class Map0Handler(tornado.web.RequestHandler):
    def get(self):
        self.render('map0.html')

class MapHandler(tornado.web.RequestHandler):
    # render the map
    def get(self):
        self.render('map.html')

class AnimatedMapHandler(tornado.web.RequestHandler):
    # render the map
    def get(self):
        self.render('animated_map.html')

if __name__ == "__main__":

    websocket_callbacks = []
    data_buffer = []
    settings = {
        'debug': True,
        'static_path':os.path.join(
            os.path.dirname(__file__), 
            "static"
        ),
    }
    application = tornado.web.Application(
        [
            (r"/", EchoWebSocket),
            (r"/put", PutHandler),
            (r"/ping", PingHandler),
            (r"/map", MapHandler),
            (r"/talk", TalkHandler),
            (r"/basic", BasicHandler),
            (r"/circles", CirclesHandler),
            (r"/circles1", Circles1Handler),
            (r"/map0", Map0Handler),
            (r"/animated_map", AnimatedMapHandler),
        ],
        **settings
    )

    application.listen(8888)

    tornado.options.parse_command_line()
    logging.info("starting torando web server")

    tornado.ioloop.IOLoop.instance().start()
