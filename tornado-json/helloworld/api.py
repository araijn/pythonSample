from tornado_json.requesthandlers import APIHandler
from tornado_json import schema
from tornado_json.exceptions import APIError

def is_validationError(error_str):
    return 'Failed validating' in error_str

class ErrorResponse:
    def __init__(self, error_type, reason, detail=None):
        self.error_type = error_type
        self.reason = reason
        self.detail  = detail

    def toDict(self):
        dict = vars(self)
        if dict['detail'] is None:
           del dict['detail']
        return vars(self)

class MyAPIHandler(APIHandler):
    def success(self, data):
        self.write(data)
        self.finish()
    
    def fail(self, data):
        
        if is_validationError(data):
           error_type = 'validation'
           errors = data.split('\n\n')
           reason = errors[0]
        else:
           error_type = 'api'
           reason = data

        detail = data if self.settings.get("debug") else None
        self.write(ErrorResponse(error_type, reason, detail).toDict())
        self.finish()           

    def error(self, message, data=None, code=None):
        
        self.write(ErrorResponse('api', message, data).toDict())
        self.finish()

class HelloWorldHandler(MyAPIHandler):

    @schema.validate(
        output_schema={"type":"string"},
    )
    def get(self):
        return "Hello world!"

class UrlParamHandler(MyAPIHandler):
   
    @schema.validate(
        output_schema={"type":"string"},
    )
    def get(self, fname, lname):
        return "Hi! {}.{} How are you?".format(fname, lname)

class UrlPatternHandler(MyAPIHandler):

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

        id_int = int(id)
        if id_int == 9999:
           raise APIError(404, '{} is not found'.format(id))

        return {
           "id" : id_int, 
           "gtype": self.get_query_argument("type")
        }

class PostHandler(MyAPIHandler):
    @schema.validate(
        input_schema={
             "type": "object",
             "properties": {
                "title": {"type": "string"},
                "body":  {"type": "string"},
                "index": {"type": "number"},
              },
              "required": ["title"]
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
