#!/usr/bin/env python3

import datetime
import json

import csv
import re
import subprocess
import collections
import operator


class AsteriskCallHistory():
    """docstring for AsteriskCallHistory"""

    def __init__(self, configfile):
        # Global Variables
        self.configfile = configfile
        self.configuration = self.ReadConfig()
        self.timezone = 3

    def getCallHistory(self, limit):
        self.contacts = self.readContacts('cidname')
        with open(self.configuration['options']['callDataFile'], newline='') as f:
            reader = csv.reader(f)
            asteriskCalls = list(reader)
            asteriskCalls.reverse()  # Read log botton up
        # if limit:
        #    asteriskCalls = asteriskCalls[:limit]

        callHistoryExternal = []
        callHistoryInternal = []

        for callLog in asteriskCalls:
            callFromType = "unknown"
            callToType = "unknown"
            log_from = callLog[1]
            log_to = callLog[2]
            log_time = callLog[9]
            log_time = datetime.datetime.strptime(callLog[9], '%Y-%m-%d %H:%M:%S')  # change it!
            log_time += datetime.timedelta(hours=self.timezone)
            log_time = log_time.strftime("%H:%M:%S %d-%m-%Y")
            log_duration = str(datetime.timedelta(seconds=int(callLog[13])))
            log_callStatus = callLog[14]
            log_result = callLog[7] + ' ' + callLog[8]

            if self.isInListType(log_to, self.configuration['options']['internalNumbers']):
                callToType = "internal"
            else:
                callToType = "external"

            if self.isInListType(log_from, self.configuration['options']['internalNumbers']):
                callFromType = "internal"
            else:
                callFromType = "external"

            if "Dial" in log_result:
                log_result = ''
            elif "VoiceMail" in log_result:
                log_callStatus = 'VOICEMAIL'
                log_result = ''
            elif "Hangup" in log_result:
                log_callStatus = 'HANGUP'
                log_result = ''
            elif "hangup" in log_result:
                log_callStatus = 'HANGUP'
                log_result = ''
            elif "telemarket" in log_result:
                log_callStatus = 'BLOCKED'
                log_result = ''
            elif "WaitExten" in log_result:
                log_callStatus = 'BLOCKED'
                log_result = ''
            else:
                log_callStatus = 'Unknown'

            log_from_id = self.getCallerID(log_from)
            log_to_id = self.getCallerID(log_to)

            if log_callStatus == "ANSWERED":
                callStatusColor = "#030"
            elif log_callStatus == "NO ANSWER":
                callStatusColor = "#321"
            elif log_callStatus == "BUSY":
                callStatusColor = "#122"
            elif log_callStatus == "FAILED":
                callStatusColor = "#330000"
            elif log_callStatus == "HANGUP":
                callStatusColor = "#200"
            elif log_callStatus == "VOICEMAIL":
                callStatusColor = "#060"
            elif log_callStatus == "BLOCKED":
                callStatusColor = "#004"
            else:
                callStatusColor = ""

            callHistoryTmp = ({
                "callFrom": log_from,
                "callFromID": log_from_id,
                "callFromType": callFromType,
                "callTo": log_to,
                "callToID": log_to_id,
                "callToType": callToType,
                "callDuration": log_duration,
                "callDate": log_time,
                "callStatus": log_callStatus,
                "callResult": log_result,
                "callColor": callStatusColor
            })

            if callFromType == "internal" and callToType == "internal":
                callHistoryInternal.append(callHistoryTmp)
            elif callFromType == "external" or callToType == "external":
                callHistoryExternal.append(callHistoryTmp)

        if limit:
            callHistoryExternal = callHistoryExternal[:limit]
            callHistoryInternal = callHistoryInternal[:limit]
        return callHistoryExternal, callHistoryInternal

    def getCurrentStatus(self):
        self.contacts = self.readContacts('cidname')
        currentCalls = []
        cmd = "asterisk -vvvvvrx 'core show channels concise'"
        out = subprocess.getoutput(cmd)
        for row in out.split('\n'):
            m = re.search(r'(.*)!(.*)!(.*)!(.*)!(.*)!(.*)!(.*)!(.*)!(.*)!(.*)!(.*)!(.*)!(.*)!(.*)$', row)
            if m:
                currentCalls.append({
                    "Channel": m.group(1),
                    "Context": m.group(2),
                    "Extension": m.group(3),
                    "ExtensionName": self.getCallerID(m.group(3)),
                    "Prio": m.group(4),
                    "State": m.group(5),
                    "Application": m.group(6),
                    "Data": m.group(7),
                    "CallerID": m.group(8),
                    "CallerIDName": self.getCallerID(m.group(8)),
                    "Duration": str(datetime.timedelta(seconds=int(m.group(12)))),
                    "Accountcode": m.group(10),
                    "PeerAccount": m.group(9),
                    "BridgedTo": m.group(13),
                    "???": m.group(11),
                    "????": m.group(14)
                })
        return currentCalls

    def ReadConfig(self):
        with open(self.configfile) as data_file:
            configuration = json.load(data_file)
        return configuration

    def isInListType(self, numberToCheck, listCallRegExp):
        inListType = False
        for callRegExp in listCallRegExp:
            if callRegExp[0] == "_":
                callRegExp = callRegExp.replace("_", "")
                callRegExp = callRegExp.replace(".", "+")
                callRegExp = callRegExp.replace("X", "\d") + "$"
                pattern = re.compile(callRegExp)
                if pattern.match(numberToCheck):
                    inListType = True
                    break
            elif callRegExp == numberToCheck:
                inListType = True
                break
            else:
                inListType = False
        return inListType

    def getVoiceMails(self):
        mailboxes = []
        cmd = "asterisk -rx 'voicemail show users'"
        out = subprocess.getoutput(cmd)
        for row in out.split('\n'):
            if len(row) >= 55:
                mailboxes.append({
                    "context": row[0:10].strip(),
                    "mbox": row[10:16].strip(),
                    "user": row[16:42].strip(),
                    "zone": row[42:53].strip(),
                    "newMsg": row[53:].strip()
                })
        mailboxes.pop(0)
        mailboxes.pop(-1)
        return mailboxes

    def getPeers(self):
        peers = []
        cmd = "asterisk -rx 'sip show peers'"
        out = subprocess.getoutput(cmd)
        for row in out.split('\n'):
            if len(row) >= 105:
                peers.append({
                    "user": row[0:25].strip(),
                    "host": row[25:65].strip(),
                    "port": row[84:93].strip(),
                    "status": row[93:105].strip()
                })
        peers.pop(0)
        return peers

    def getContacts(self, table):
        self.contacts = self.readContacts(table)
        return self.contacts

    def delContact(self, table, number):
        cmd = "asterisk -rx 'database del {table} {number}'".format(table=table, number=number)
        out = subprocess.getoutput(cmd)
        return "done"

    def addContact(self, table, number, name):
        cmd = "asterisk -rx 'database put {table} {number} \"{name}\"'".format(table=table, number=number, name=name)
        out = subprocess.getoutput(cmd)
        return "done"

    def readContacts(self, table):
        contacts = {}
        cmd = "asterisk -rx 'database show {table}'".format(table=table)
        out = subprocess.getoutput(cmd)
        for row in out.split('\n'):
            m = re.search(r'/.+/([^\s]+)\s+:\s(.*)', row)
            if m:
                number = m.group(1).strip()
                name = m.group(2).strip()
                contacts[number] = name
        oContacts = collections.OrderedDict(sorted(contacts.items(), key=operator.itemgetter(1)))
        return oContacts

    def getCallerID(self, number):
        callerID = number
        if number in self.contacts:
            callerID = self.contacts[number]

        return callerID
