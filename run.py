#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import os
from CallHistory import AsteriskCallHistory


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        historyExternal, historyInternal, historyUnknown = callhistory.getCallHistory(int(10))
        self.render("index.html",
                    title="Call History",
                    external=historyExternal,
                    internal=historyInternal,
                    unknown=historyUnknown)


def make_app():
    settings = {
        "debug": True,
        "template_path": webDirectory,
        "static_path": webDirectory
    }

    return tornado.web.Application([
        (r"/", MainHandler),
    ], **settings)


if __name__ == "__main__":
    wd = os.path.dirname(os.path.realpath(__file__))
    webDirectory = os.path.join(wd, 'web')
    configfile = os.path.join(wd, "configuration.json")
    callhistory = AsteriskCallHistory(configfile)

    app = make_app()
    app.listen(5002)
    tornado.ioloop.IOLoop.current().start()
