from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application
import asyncio
import json

class StartupHandler(RequestHandler):
    def get(self):
        # self.write("Hello, world !!!")  # for raw data
        # self.render("html page")    # for html page
        self.write({"item": 12})

class EchoHandler(RequestHandler):
    def post(self):
        # self.write({'message' : self.request.body})
        self.write({"message": json.loads(self.request.body)})

    def get(self):
        self.write("HTTP GET query")

    def delete(self, id):
        pass


# Mappped Routes to specific controller classes


def makeRoutes():
    urls = [
        (r"/", StartupHandler),
        (r"/msg/echo", EchoHandler)
    ]

    # restarts the server automatically ( not for production purpose when debug = True )
    return Application(urls, debug=True)


PORT = 3000

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    application = makeRoutes()
    application.listen(PORT)

    # excute the application
    # tornado.ioloop.IOLoop.current().start()
    IOLoop.instance().start()
