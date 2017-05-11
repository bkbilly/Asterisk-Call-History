#!/usr/bin/env python
from datetime import datetime
import json

import csv
import re


class AsteriskCallHistory():
    """docstring for AsteriskCallHistory"""

    def __init__(self, configfile):
        # Global Variables
        self.configfile = configfile
        self.configuration = self.ReadConfig()
        self.callHistory = []

    def getCallHistory(self, limit):
        with open(self.configuration['options']['callDataFile'], 'rb') as f:
            reader = csv.reader(f)
            asteriskCalls = list(reader)
            asteriskCalls.reverse()  # Read log botton up
        if limit:
            asteriskCalls = asteriskCalls[:limit]

        self.callHistory = []
        for callLog in asteriskCalls:
            callFromType = "unknown"
            callToType = "unknown"
            log_from = callLog[1]
            log_to = callLog[2]
            log_time = callLog[9]
            log_duration = int(callLog[13])
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

            self.callHistory.append({
                "callFrom": log_from,
                "callFromType": callFromType,
                "callTo": log_to,
                "callToType": callToType,
                "callDuration": log_duration,
                "callDate": log_time,
                "callStatus": log_callStatus,
                "callResult": log_result
            })
        return self.callHistory

    def ReadConfig(self):
        with open(self.configfile) as data_file:
            configuration = json.load(data_file)
        return configuration

    def isInListType(self, numberToCheck, listCallRegExp):
        inListType = False
        for callRegExp in listCallRegExp:
            if callRegExp[0] == "_":
                callRegExp = callRegExp.replace("_", "")
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
