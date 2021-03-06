#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hardware import HardwareHandler
import json

class Controller():
    """Controller"""
    def __init__(self):
        self.HardwareHandler = HardwareHandler()
        self.load("hardware.json")

    def load(self, filename):
        with open(filename) as f:
            hardware = json.load(f)
            for h in hardware:
                hardware_type = h['hardware_type'].encode('ascii', 'ignore')
                self.HardwareHandler.add(hardware_type, h['args'])

    def process(self, msg):
        print 'Received message: %s' % (msg)
        msg_parts = msg.split()
        resps = []

        if len(msg_parts)<2:
            return []
        req_type = msg_parts[0]
        targets = msg_parts[1] # target hardware

        if targets == "*":
            targets = self.HardwareHandler.list()
        else:
            targets = [targets]

        if req_type == "get":
            for hardware_name in targets:
                resp = hardware_name + " " + str(self.HardwareHandler.get(hardware_name))
                resps.append(resp)
        elif req_type == "describe":
            for hardware_name in targets:
                resp = hardware_name + " " + str(self.HardwareHandler.get(hardware_name))
                resp +=  " " + self.HardwareHandler.describe(hardware_name)
                resps.append(resp)
        elif req_type == "set":
            if len(msg_parts)<3:
                return []
            try:
                new_value = float(msg_parts[2])
            except:
                return []

            hardware_name = targets[0]
            self.HardwareHandler.set(hardware_name, new_value)
            resp = hardware_name + " " + str(self.HardwareHandler.get(hardware_name))
            resps.append(resp)

        return resps

    def cleanup(self):
        self.HardwareHandler.cleanup()
