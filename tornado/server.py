# -*- coding: utf-8 -*-
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
from tornado.escape import json_decode
from os import path, getcwd
from tornado import gen
from tornado.httpclient import AsyncHTTPClient

class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello, world")

class Person:
    def __init__(self, id, name, age):
        self.id   = id
        self.name = name
        self.age  = age
    def hello(self):
        return "Hello! " + self.name

class UrlMatchSampleHandler(RequestHandler):
    def get(self, id):
        person = Person(id, "Nanasi Gonbei", "25")
        # varsはオブジェクトをdictに変換する
        # RequestHandler.writeはdictを渡すと応答としてjson形式で返す
        self.write(vars(person))

class PostSampleHandler(RequestHandler):
    def get(self):
        id = self.get_query_argument("id", default=9999)
        self.render("post_form.html", id=id)

    def post(self):
        self.render("result.html", 
                      id = self.get_body_argument("id"),
                    name = self.get_body_argument("name"),
                    age  = self.get_body_argument("age"))

class JsonSampleHandler(RequestHandler):
    def post(self):
        json = json_decode(self.request.body)
        self.render("result.html", id = json["id"], name = json["name"], age = json["age"])

class HeavyWorkHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        yield gen.sleep(10)
        self.write("ok")

class AsyncSampleHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("http://localhost:8888/heavy")
        self.write("respose is {} ".format(response.body))

def make_app():
    return Application([
        (r"/hello", MainHandler),
        (r"/user/(?P<id>[0-9]+)", UrlMatchSampleHandler),
        (r"/post/user", PostSampleHandler),
        (r"/json", JsonSampleHandler),
        (r"/heavy", HeavyWorkHandler),
        (r"/async", AsyncSampleHandler),
       ], debug=True, template_path=path.join(getcwd(), "templates"))

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    IOLoop.current().start()
  
