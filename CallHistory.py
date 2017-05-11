#!/usr/bin/env python
import datetime
import json

import csv
import re
import subprocess

class AsteriskCallHistory():
    """docstring for AsteriskCallHistory"""

    def __init__(self, configfile):
        # Global Variables
        self.configfile = configfile
        self.configuration = self.ReadConfig()

    def getCallHistory(self, limit):
        with open(self.configuration['options']['callDataFile'], 'rb') as f:
            reader = csv.reader(f)
            asteriskCalls = list(reader)
            asteriskCalls.reverse()  # Read log botton up
        #if limit:
        #    asteriskCalls = asteriskCalls[:limit]

        self.allCallerIDs = self.getAllCallerIDs()
        callHistoryExternal = []
        callHistoryInternal = []
        callHistoryUnknown = []

        for callLog in asteriskCalls:
            callFromType = "unknown"
            callToType = "unknown"
            log_from = callLog[1]
            log_to = callLog[2]
            log_time = callLog[9]
            log_duration = str(datetime.timedelta(seconds=int(callLog[13])))
            log_callStatus = callLog[14]
            log_result = callLog[7] + ' ' + callLog[8]

            if self.isInListType(log_from, self.configuration['options']['internalNumbers']):
                callFromType = "internal"
            else:
                callFromType = "external"

            if self.isInListType(log_to, self.configuration['options']['internalNumbers']):
                callToType = "internal"
            else:
                callToType = "external"

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
            else:
                callHistoryUnknown.append(callHistoryTmp)

        if limit:
            callHistoryExternal = callHistoryExternal[:limit]
            callHistoryInternal = callHistoryInternal[:limit]
        return callHistoryExternal, callHistoryInternal, callHistoryUnknown

    def getCurrentStatus(self):
        currentCalls = []
        cmd = "asterisk -vvvvvrx 'core show channels concise'"
        out, err = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
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

    def getAllCallerIDs(self):
        allCallerIDs = {}
        cmd = "asterisk -rx 'database show cidname'"
        out, err = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
        for row in out.split('\n'):
            m = re.search(r'/.+/([^\s]+)\s+:\s(.*)', row)
            if m:
                allCallerIDs[m.group(1)] = m.group(2)
        return allCallerIDs

    def getCallerID(self, number):
        callerID = number
        if number in self.allCallerIDs:
            callerID = self.allCallerIDs[number]

        return callerID

