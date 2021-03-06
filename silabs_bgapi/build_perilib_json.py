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
    "ble": "silabs-bgapi-ble1xx",
    "gecko": "silabs-bgapi-bgm1xx",
    "dumo": "silabs-bgapi-bt121",
    "wifi121": "silabs-bgapi-wf121",
    "wifi110": "silabs-bgapi-wgm110",
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
                json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id] = OrderedDict()

            # add/update relevant class details
            json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id]["name"] = class_def["@name"]

            for command_def in class_def["command"]:
                command_id = command_def["@index"]
                if command_id not in json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id]:
                    # event does not exist in definition
                    json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id] = OrderedDict()

                # update name
                json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id]["name"] = command_def["@name"]

                # identify command parameters
                if command_def["params"] is None:
                    json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id]["command_args"] = []
                    param_str = ""
                else:
                    if "command_args" not in json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id]:
                        json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id]["command_args"] = []
                    for index, param in enumerate(command_def["params"]["param"]):
                        if len(json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id]["command_args"]) == index:
                            # argument does not exist in list
                            json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id]["command_args"].append(OrderedDict())
                        json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id]["command_args"][index]["name"] = param["@name"]
                        json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id]["command_args"][index]["type"] = param["@type"]
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
                        json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id]["response_args"] = []
                        param_str = ""
                    else:
                        if "response_args" not in json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id]:
                            json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id]["response_args"] = []
                        for index, param in enumerate(command_def["returns"]["param"]):
                            if len(json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id]["response_args"]) == index:
                                # argument does not exist in list
                                json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id]["response_args"].append(OrderedDict())
                            json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id]["response_args"][index]["name"] = param["@name"]
                            json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id]["response_args"][index]["type"] = param["@type"]
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
                json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id] = json_definition["protocols"][id_map[technology]]["packets"]["commands"]["entities"][class_id][command_id]

        # step through each event in this class, if any
        if "event" in class_def:
            print("        events:")

            # add dictionary key for this class ID in the event set
            if class_id not in json_definition["protocols"][id_map[technology]]["packets"]["events"]:
                json_definition["protocols"][id_map[technology]]["packets"]["events"]["entities"][class_id] = OrderedDict()

            # add/update relevant class details
            json_definition["protocols"][id_map[technology]]["packets"]["events"]["entities"][class_id]["name"] = class_def["@name"]

            for event_def in class_def["event"]:
                event_id = event_def["@index"]
                if event_id not in json_definition["protocols"][id_map[technology]]["packets"]["events"]["entities"][class_id]:
                    # event does not exist in definition
                    json_definition["protocols"][id_map[technology]]["packets"]["events"]["entities"][class_id][event_id] = OrderedDict()

                # update name
                json_definition["protocols"][id_map[technology]]["packets"]["events"]["entities"][class_id][event_id]["name"] = event_def["@name"]

                # identify event parameters
                if event_def["params"] is None:
                    json_definition["protocols"][id_map[technology]]["packets"]["events"]["entities"][class_id][event_id]["event_args"] = []
                    param_str = ""
                else:
                    if "event_args" not in json_definition["protocols"][id_map[technology]]["packets"]["events"]["entities"][class_id][event_id]:
                        json_definition["protocols"][id_map[technology]]["packets"]["events"]["entities"][class_id][event_id]["event_args"] = []
                    for index, param in enumerate(event_def["params"]["param"]):
                        if len(json_definition["protocols"][id_map[technology]]["packets"]["events"]["entities"][class_id][event_id]["event_args"]) == index:
                            # argument does not exist in list
                            json_definition["protocols"][id_map[technology]]["packets"]["events"]["entities"][class_id][event_id]["event_args"].append(OrderedDict())
                        json_definition["protocols"][id_map[technology]]["packets"]["events"]["entities"][class_id][event_id]["event_args"][index]["name"] = param["@name"]
                        json_definition["protocols"][id_map[technology]]["packets"]["events"]["entities"][class_id][event_id]["event_args"][index]["type"] = param["@type"]
                    param_str = ', '.join(["%s %s" % (param["@type"], param["@name"]) for param in event_def["params"]["param"]])
                print("            %s/%s: %s_evt_%s_%s(%s)" % (
                        class_id,
                        event_id,
                        technology, class_def["@name"],
                        event_def["@name"],
                        param_str))

# write modified definitions back into file
with open("../../perilib-definitions/silabs_bgapi.json", "w") as f:
    json.dump(json_definition, f, indent=4)
    f.write("\n")
