#!/usr/bin/env python3

from collections import OrderedDict
import xmltodict
import pprint

api = OrderedDict()

# Bluetooth Low Energy: Bluegiga BLE112, BLE113, BLE121LR
with open("bleapi.xml", "r") as f:
    api["ble"] = xmltodict.parse(f.read(), force_list=['class', 'command', 'event', 'param'])
    
# Wi-Fi: Bluegiga WF121
with open("wifiapi-wf121.xml", "r") as f:
    api["wifi121"] = xmltodict.parse(f.read(), force_list=['class', 'command', 'event', 'param'])
    
# Wi-Fi: Silicon Labs WGM110
with open("wifiapi-wgm110.xml", "r") as f:
    api["wifi110"] = xmltodict.parse(f.read(), force_list=['class', 'command', 'event', 'param'])
    
# Bluetooth Smart Ready: Bluegiga BT121
with open("dumoapi.xml", "r") as f:
    api["dumo"] = xmltodict.parse(f.read(), force_list=['class', 'command', 'event', 'param'])

# Bluetooth Low Energy (no mesh): Silicon Labs Blue Gecko BGMxxx
with open("gecko.xml", "r") as f:
    api["gecko"] = xmltodict.parse(f.read(), force_list=['class', 'command', 'event', 'param'])

# step through each API definition
for technology in api:
    print("%s (%s)" % (technology, api[technology]["api"]["@device_id"]))
    
    # step through each class
    for class_def in api[technology]["api"]["class"]:
        class_id = class_def["@index"]
        print("    %s: %s" % (class_id, class_def["@name"]))
        
        # step through each command/response pair in this class, if any
        if "command" in class_def:
            print("        commands:")

            for command_def in class_def["command"]:
                command_id = command_def["@index"]

                # identify command parameters
                if command_def["params"] is None:
                    param_str = ""
                else:
                    param_str = ', '.join(["%s %s" % (param["@type"], param["@name"]) for param in command_def["params"]["param"]])
                print("            %s/%s: %s_cmd_%s_%s(%s)" % (
                        class_id,
                        command_id,
                        technology, class_def["@name"],
                        command_def["@name"],
                        param_str))
                        
                # identify response parameters, if any
                if "returns" in command_def:
                    if command_def["returns"] is None:
                        param_str = ""
                    else:
                        param_str = ', '.join(["%s %s" % (param["@type"], param["@name"]) for param in command_def["returns"]["param"]])
                    print("            %s/%s: %s_rsp_%s_%s(%s)" % (
                            class_id,
                            command_id,
                            technology, class_def["@name"],
                            command_def["@name"],
                            param_str))
                else:
                    print("            %d/%d: NOTE: COMMAND HAS NO RESPONSE" % (int(class_def["@index"]), int(command_def["@index"])))

        # step through each event in this class, if any
        if "event" in class_def:
            print("        events:")

            for event_def in class_def["event"]:
                event_id = event_def["@index"]

                # identify command parameters
                if event_def["params"] is None:
                    param_str = ""
                else:
                    param_str = ', '.join(["%s %s" % (param["@type"], param["@name"]) for param in event_def["params"]["param"]])
                print("            %s/%s: %s_evt_%s_%s(%s)" % (
                        class_id,
                        event_id,
                        technology, class_def["@name"],
                        event_def["@name"],
                        param_str))
