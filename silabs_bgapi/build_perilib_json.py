#!/usr/bin/env python3

from collections import OrderedDict
import json
import xmltodict

api = OrderedDict()

# read original definitions from file
with open("../../perilib-definitions/silabs_bgapi.json", "r") as f:
    json_definition = json.load(f, object_pairs_hook=OrderedDict)
    
# Bluetooth Low Energy: Bluegiga BLE112, BLE113, BLE121LR
with open("bleapi.xml", "r") as f:
    api["ble"] = xmltodict.parse(f.read(), force_list=['class', 'command', 'event', 'param'])
    
# Bluetooth Low Energy (no mesh): Silicon Labs Blue Gecko BGMxxx
with open("gecko.xml", "r") as f:
    api["gecko"] = xmltodict.parse(f.read(), force_list=['class', 'command', 'event', 'param'])

# Bluetooth Smart Ready: Bluegiga BT121
with open("dumoapi.xml", "r") as f:
    api["dumo"] = xmltodict.parse(f.read(), force_list=['class', 'command', 'event', 'param'])

# Wi-Fi: Bluegiga WF121
with open("wifiapi-wf121.xml", "r") as f:
    api["wifi121"] = xmltodict.parse(f.read(), force_list=['class', 'command', 'event', 'param'])
    
# Wi-Fi: Silicon Labs WGM110
with open("wifiapi-wgm110.xml", "r") as f:
    api["wifi110"] = xmltodict.parse(f.read(), force_list=['class', 'command', 'event', 'param'])
    
# protocol ID mapping
id_map = {
    "ble": "silabs-bgapi-ble-ble1xx",
    "gecko": "silabs-bgapi-ble-gecko",
    "dumo": "silabs-bgapi-dumo-bt121",
    "wifi121": "silabs-bgapi-wifi-wf121",
    "wifi110": "silabs-bgapi-wifi-wgm110",
}

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

            # add dictionary key for this class ID in the command set
            if class_id not in json_definition["protocols"][id_map[technology]]["packets"]["commands"]:
                json_definition["protocols"][id_map[technology]]["packets"]["commands"][class_id] = OrderedDict()

            # add/update relevant class details
            json_definition["protocols"][id_map[technology]]["packets"]["commands"][class_id]["name"] = class_def["@name"]

            for command_def in class_def["command"]:
                command_id = command_def["@index"]
                command_def_json = OrderedDict({ "name": command_def["@name"] })

                # identify command parameters
                if command_def["params"] is None:
                    command_def_json["command_args"] = []
                    param_str = ""
                else:
                    command_def_json["command_args"] = [OrderedDict({ "name": param["@name"], "type": param["@type"] }) for param in command_def["params"]["param"]]
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
                        command_def_json["response_args"] = []
                        param_str = ""
                    else:
                        command_def_json["response_args"] = [OrderedDict({ "name": param["@name"], "type": param["@type"] }) for param in command_def["returns"]["param"]]
                        param_str = ', '.join(["%s %s" % (param["@type"], param["@name"]) for param in command_def["returns"]["param"]])
                    print("            %s/%s: %s_rsp_%s_%s(%s)" % (
                            class_id,
                            command_id,
                            technology, class_def["@name"],
                            command_def["@name"],
                            param_str))
                else:
                    print("            %d/%d: NOTE: COMMAND HAS NO RESPONSE" % (int(class_def["@index"]), int(command_def["@index"])))
                    
                # add/update command definition in JSON structure
                json_definition["protocols"][id_map[technology]]["packets"]["commands"][class_id][command_id] = command_def_json

        # step through each event in this class, if any
        if "event" in class_def:
            print("        events:")

            # add dictionary key for this class ID in the event set
            if class_id not in json_definition["protocols"][id_map[technology]]["packets"]["events"]:
                json_definition["protocols"][id_map[technology]]["packets"]["events"][class_id] = OrderedDict()

            # add/update relevant class details
            json_definition["protocols"][id_map[technology]]["packets"]["events"][class_id]["name"] = class_def["@name"]

            for event_def in class_def["event"]:
                event_id = event_def["@index"]
                event_def_json = OrderedDict({ "name": event_def["@name"] })

                # identify event parameters
                if event_def["params"] is None:
                    event_def_json["event_args"] = []
                    param_str = ""
                else:
                    event_def_json["event_args"] = [OrderedDict({ "name": param["@name"], "type": param["@type"] }) for param in event_def["params"]["param"]]
                    param_str = ', '.join(["%s %s" % (param["@type"], param["@name"]) for param in event_def["params"]["param"]])
                print("            %s/%s: %s_evt_%s_%s(%s)" % (
                        class_id,
                        event_id,
                        technology, class_def["@name"],
                        event_def["@name"],
                        param_str))
                        
                # add/update command definition in JSON structure
                json_definition["protocols"][id_map[technology]]["packets"]["events"][class_id][event_id] = event_def_json

# write modified definitions back into file
with open("../../perilib-definitions/silabs_bgapi.json", "w") as f:
    json.dump(json_definition, f, indent=4)
