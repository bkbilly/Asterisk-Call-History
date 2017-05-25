#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import os
from CallHistory import AsteriskCallHistory


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        historyExternal, historyInternal = callhistory.getCallHistory(int(100))
        currentCalls = callhistory.getCurrentStatus()
        peers = callhistory.getPeers()
        contacts = callhistory.getContacts()
        self.render("index.html",
                    title="Call History",
                    external=historyExternal,
                    internal=historyInternal,
                    currentCalls=currentCalls,
                    peers=peers,
                    contacts=contacts)

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        currentCalls = callhistory.getCurrentStatus()
        peers = callhistory.getPeers()
        contacts = callhistory.getContacts()
        self.render("home.html",
                    title="Call History",
                    currentCalls=currentCalls,
                    peers=peers)

class ContactsHandler(tornado.web.RequestHandler):
    def get(self):
        contacts = callhistory.getContacts()
        self.render("contacts.html",
                    title="Call History",
                    contacts=contacts)

    def post(self):
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
                msg = callhistory.addContact(number, name)
                login_response = {
                    'error': False, 
                    'msg': msg
                }
        elif method == 'del':
            number = self.get_argument('cnt_number', '')
            print "del:", number
            if not number:
                login_response = {
                    'error': True, 
                    'msg': 'Please enter a number.'
                }
            else:
                msg = callhistory.delContact(number)
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
        contacts = callhistory.getContacts()
        self.render("blockedcontacts.html",
                    title="Call History",
                    contacts=contacts)

    def post(self):
        number = self.get_argument('blcnt_number', '')
        if not number:
            login_response = {
                'error': True, 
                'msg': 'Please enter a number.'
            }
        else:
            login_response = {
                'error': True, 
                'msg': 'not supported.'
            }
        self.write(login_response)


class HistoryExternalHandler(tornado.web.RequestHandler):
    def get(self):
        historyExternal, historyInternal = callhistory.getCallHistory(int(100))
        self.render("history_external.html",
                    title="Call History",
                    external=historyExternal)

class HistoryInternalHandler(tornado.web.RequestHandler):
    def get(self):
        historyExternal, historyInternal = callhistory.getCallHistory(int(100))
        self.render("history_internal.html",
                    title="Call History",
                    internal=historyInternal)

def make_app():
    settings = {
        "debug": True,
        "template_path": webDirectory,
        "static_path": webDirectory
    }

    return tornado.web.Application([
        (r"/", HomeHandler),
        (r"/home.html", HomeHandler),
        (r"/contacts.html", ContactsHandler),
        (r"/blockedcontacts.html", BlockedContactsHandler),
        (r"/history_external.html", HistoryExternalHandler),
        (r"/history_internal.html", HistoryInternalHandler)
    ], **settings)


if __name__ == "__main__":
    wd = os.path.dirname(os.path.realpath(__file__))
    webDirectory = os.path.join(wd, 'web')
    configfile = os.path.join(wd, "configuration.json")
    callhistory = AsteriskCallHistory(configfile)

    app = make_app()
    app.listen(5002)
    tornado.ioloop.IOLoop.current().start()
