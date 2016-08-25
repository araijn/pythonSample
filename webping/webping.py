from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from argparse import ArgumentParser
import os

class WebPing(RequestHandler):
    def get(self):
        self.write("ok")

def make_app(host, apipath):
     if host is None:
        return Application(
                 [(apipath, WebPing)]
               )

     app = Application()
     app.add_handlers(host, [(apipath, WebPing)])
     return app


if __name__ == "__main__":

   parser = ArgumentParser()
   parser.add_argument('--host', help='hostname')
   parser.add_argument('-u', '--urlpath', help='webping urlpath', default='/webping')
   parser.add_argument('-p', '--port', type=int, help='listen port', default=8888)
   args = parser.parse_args()
   
   port = args.port
   host = args.host
   urlpath = args.urlpath
   app = make_app(host, urlpath)
   app.listen(port)

   if args.host is None:
      host = os.uname()[1]
 
   print("Now waiting request : http://{}:{}{}".format(host, port, urlpath))
   IOLoop.current().start()

