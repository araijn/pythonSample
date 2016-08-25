from tornado_json.requesthandlers import APIHandler
from tornado_json import schema

class HelloWorldHandler(APIHandler):

    @schema.validate(
        output_schema={"type":"string"},
    )
    def get(self):
        return "Hello world!"

class UrlParamHandler(APIHandler):
   
    @schema.validate(
        output_schema={"type":"string"},
    )
    def get(self, fname, lname):
        return "Hi! {}.{} How are you?".format(fname, lname)

class UrlPatternHandler(APIHandler):

    __urls__ = [r"/api/user/(?P<id>[0-9]+)/group"]
    __url_names__ = []
    @schema.validate(
        output_schema={
           "type":"object",
           "properties": {
              "id": { "type":"number"},
              "gtype": { "type":"string"},
           }
        },
    )
    def get(self, id):
        return {
           "id" : int(id),
           "gtype": self.get_query_argument("type", default="none")
        }

class PostHandler(APIHandler):
    @schema.validate(
        input_schema={
             "type": "object",
             "properties": {
                "title": {"type": "string"},
                "body":  {"type": "string"},
                "index": {"type": "number"},
              },
              "required": ["title", "body"]
        },
        output_schema={
             "type": "object",
             "properties": {
                 "message": {"type": "string"},
             }
        },
    )
    def post(self):
        return {
          "message": "{} was posted.".format(self.body["title"]),
        }
