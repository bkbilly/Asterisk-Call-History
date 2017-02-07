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

    def getCallHistory(self, limit):
        with open(self.configuration['options']['callDataFile'], 'rb') as f:
            reader = csv.reader(f)
            asteriskCalls = list(reader)
            asteriskCalls.reverse()  # Read log botton up
        if limit:
            asteriskCalls = asteriskCalls[:limit]

        callHistoryExternal = []
        callHistoryInternal = []
        callHistoryUnknown = []

        for callLog in asteriskCalls:
            callFromType = "unknown"
            callToType = "unknown"
            log_from = callLog[1]
            log_to = callLog[2]
            log_time = callLog[9]
            log_duration = int(callLog[13])
            log_callStatus = callLog[14]
            log_result = callLog[7] + ' ' + callLog[8]

            if self.isInListType(log_from, self.configuration['options']['externalNumbers']):
                callFromType = "external"
            elif self.isInListType(log_from, self.configuration['options']['internalNumbers']):
                callFromType = "internal"
            else:
                callFromType = "unknown"

            if self.isInListType(log_to, self.configuration['options']['externalNumbers']):
                callToType = "external"
            elif self.isInListType(log_to, self.configuration['options']['internalNumbers']):
                callToType = "internal"
            else:
                callToType = "unknown"

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
                "callTo": log_to,
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

        return callHistoryExternal, callHistoryInternal, callHistoryUnknown

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
