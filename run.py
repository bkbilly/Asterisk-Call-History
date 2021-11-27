#!/usr/bin/env python3

import json
import tornado.ioloop
import tornado.web
import tornado.httpserver
import os
import ssl
from CallHistory import AsteriskCallHistory


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        currentCalls = callhistory.getCurrentStatus()
        peers = callhistory.getPeers()
        mboxes = callhistory.getVoiceMails()
        contacts = callhistory.getContacts('cidname')
        self.render("home.html",
                    title="Call History",
                    currentCalls=currentCalls,
                    peers=peers,
                    mboxes=mboxes)


class ContactsHandler(tornado.web.RequestHandler):
    def get(self):
        dbtable = 'cidname'
        contacts = callhistory.getContacts(dbtable)
        self.render("contacts.html",
                    title="Call History",
                    contacts=contacts)

    def post(self):
        dbtable = 'cidname'
        method = self.get_argument('method', '')
        if method == 'new':
            name = self.get_argument('cnt_name', '')
            number = self.get_argument('cnt_number', '')
            if not name:
                login_response = {
                    'error': True,
                    'msg': 'Please enter a name.'
                }
            elif not number:
                login_response = {
                    'error': True,
                    'msg': 'Please enter a number.'
                }
            else:
                print("add:", number, name)
                msg = callhistory.addContact(dbtable, number, name)
                login_response = {
                    'error': False,
                    'msg': msg
                }
        elif method == 'del':
            number = self.get_argument('cnt_number', '')
            print("del:", number)
            if not number:
                login_response = {
                    'error': True,
                    'msg': 'Please enter a number.'
                }
            else:
                msg = callhistory.delContact(dbtable, number)
                login_response = {
                    'error': False,
                    'msg': 'Thank You.'
                }
        else:
            login_response = {
                'error': True,
                'msg': 'Not supported.'
            }
        self.write(login_response)


class BlockedContactsHandler(tornado.web.RequestHandler):
    def get(self):
        dbtable = 'blockcaller'
        contacts = callhistory.getContacts(dbtable)
        self.render("blockedcontacts.html",
                    title="Call History",
                    contacts=contacts)

    def post(self):
        dbtable = 'blockcaller'
        method = self.get_argument('method', '')
        if method == 'new':
            name = self.get_argument('cnt_name', '')
            number = self.get_argument('cnt_number', '')
            if not name:
                login_response = {
                    'error': True,
                    'msg': 'Please enter a name.'
                }
            elif not number:
                login_response = {
                    'error': True,
                    'msg': 'Please enter a number.'
                }
            else:
                msg = callhistory.addContact(dbtable, number, name)
                login_response = {
                    'error': False,
                    'msg': msg
                }
        elif method == 'del':
            number = self.get_argument('cnt_number', '')
            print("del:", number)
            if not number:
                login_response = {
                    'error': True,
                    'msg': 'Please enter a number.'
                }
            else:
                msg = callhistory.delContact(dbtable, number)
                login_response = {
                    'error': False,
                    'msg': 'Thank You.'
                }
        else:
            login_response = {
                'error': True,
                'msg': 'Not supported.'
            }
        self.write(login_response)


class HistoryExternalHandler(tornado.web.RequestHandler):
    def get(self):
        historyExternal, historyInternal, historyAll = callhistory.getCallHistory(int(1000))
        #print(historyExternal)
        #print(historyInternal)
        self.render("history_external.html",
                    title="Call History",
                    external=historyExternal)


class HistoryInternalHandler(tornado.web.RequestHandler):
    def get(self):
        historyExternal, historyInternal, historyAll = callhistory.getCallHistory(int(1000))
        self.render("history_internal.html",
                    title="Call History",
                    internal=historyInternal)


class HistoryHandler(tornado.web.RequestHandler):
    def get(self):
        historyExternal, historyInternal, historyAll = callhistory.getCallHistory(int(1000))
        self.render("history.html",
                    title="Call History",
                    historyall=historyInternal)


def make_app(cert, key):
    settings = {
        "debug": True,
        "template_path": webDirectory,
        "static_path": webDirectory
    }

    application = tornado.web.Application([
        (r"/", HomeHandler),
        (r"/home.html", HomeHandler),
        (r"/contacts.html", ContactsHandler),
        (r"/blockedcontacts.html", BlockedContactsHandler),
        (r"/history_external.html", HistoryExternalHandler),
        (r"/history_internal.html", HistoryInternalHandler),
        (r"/history.html", HistoryHandler)
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application,
        ssl_options={
            "certfile": cert,
            "keyfile": key
        }
    )

    return http_server



if __name__ == "__main__":
    wd = os.path.dirname(os.path.realpath(__file__))
    webDirectory = os.path.join(wd, 'web')
    configfile = os.path.join(wd, "configuration.json")
    with open(configfile) as data_file:
        configuration = json.load(data_file)

    callhistory = AsteriskCallHistory(configuration)

    app = make_app(configuration['options']['cert'], configuration['options']['key'])
    app.listen(5002)
    tornado.ioloop.IOLoop.current().start()
