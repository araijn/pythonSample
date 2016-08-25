from tornado.ioloop import IOLoop
from tornado_json.routes import get_routes
from tornado_json.application import Application
import json

def make_app():
    import helloworld
    routes = get_routes(helloworld)
    print("Routes\n=======\n\n" +
           json.dumps([(url, repr(rh)) for url, rh in routes], indent=2)
          )
    settings = {"debug":True }
    return Application(routes=routes, settings=settings, generate_docs=True)

if __name__ == "__main__":
   app = make_app()
   app.listen(8888)
   IOLoop.instance().start() 
