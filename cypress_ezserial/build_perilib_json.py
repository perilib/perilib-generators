#!/usr/bin/env python3

from collections import OrderedDict
import json

# read original definitions from file
with open("../../perilib-definitions/cypress_ezserial.json", "r") as f:
    json_definition = json.load(f, object_pairs_hook=OrderedDict)
    
# Bluetooth Low Energy: PSoC 4 BLE, WICED Smart
with open("ezsapi.json", "r") as f:
    api = json.load(f, object_pairs_hook=OrderedDict)
    
print("EZ-Serial Protocol")

# step through each class
for group_def in api["groups"]:
    group_id = str(group_def["id"])
    print("    %s: %s" % (group_id, group_def["name"]))
    
    # step through each /response pair in this group, if any
    if "commands" in group_def:
        print("        commands:")

        # add dictionary key for this class ID in the command set
        if group_id not in json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"]:
            json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id] = OrderedDict()

        # add/update relevant class details
        json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id]["name"] = group_def["name"]

        for command_def in group_def["commands"]:
            command_id = str(command_def["id"])
            if command_id not in json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id]:
                # command does not exist in definition
                json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id] = OrderedDict()

            # update name
            json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["name"] = command_def["name"]

            # identify command parameters
            if command_def["parameters"] is None:
                json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["command_args"] = []
                param_str = ""
            else:
                if "command_args" not in json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]:
                    json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["command_args"] = []
                for index, param in enumerate(command_def["parameters"]):
                    if len(json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["command_args"]) == index:
                        # argument does not exist in list
                        json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["command_args"].append(OrderedDict())
                    json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["command_args"][index]["name"] = param["name"]
                    json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["command_args"][index]["type"] = param["type"]
                    if "format" in param:
                        json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["command_args"][index]["format"] = param["format"]
                    if "shortdesc" in param:
                        json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["command_args"][index]["shortdesc"] = param["shortdesc"]
                param_str = ', '.join(["%s %s" % (param["type"], param["name"]) for param in command_def["parameters"]])
            print("            %s/%s: ezs_cmd_%s_%s(%s)" % (
                    group_id,
                    command_id,
                    group_def["name"],
                    command_def["name"],
                    param_str))
                    
            # identify response parameters, if any
            if "returns" in command_def:
                if command_def["returns"] is None:
                    json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["response_args"] = []
                    param_str = ""
                else:
                    if "response_args" not in json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]:
                        json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["response_args"] = []
                    for index, param in enumerate(command_def["returns"]):
                        if len(json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["response_args"]) == index:
                            # argument does not exist in list
                            json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["response_args"].append(OrderedDict())
                        json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["response_args"][index]["name"] = param["name"]
                        json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["response_args"][index]["type"] = param["type"]
                        if "format" in param:
                            json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["response_args"][index]["format"] = param["format"]
                        if "shortdesc" in param:
                            json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]["entities"][group_id][command_id]["response_args"][index]["shortdesc"] = param["shortdesc"]
                    param_str = ', '.join(["%s %s" % (param["type"], param["name"]) for param in command_def["returns"]])
                print("            %s/%s: ezs_rsp_%s_%s(%s)" % (
                        group_id,
                        command_id,
                        group_def["name"],
                        command_def["name"],
                        param_str))
            else:
                print("            %d/%d: NOTE: COMMAND HAS NO RESPONSE" % (int(group_def["id"]), int(command_def["id"])))
                
    # step through each event in this class, if any
    if "events" in group_def:
        print("        events:")

        # add dictionary key for this class ID in the event set
        if group_id not in json_definition["protocols"]["cypress-ezserial"]["packets"]["events"]["entities"]:
            json_definition["protocols"]["cypress-ezserial"]["packets"]["events"]["entities"][group_id] = OrderedDict()

        # add/update relevant class details
        json_definition["protocols"]["cypress-ezserial"]["packets"]["events"]["entities"][group_id]["name"] = group_def["name"]

        for event_def in group_def["events"]:
            event_id = str(event_def["id"])
            print(type(event_id))
            if event_id not in json_definition["protocols"]["cypress-ezserial"]["packets"]["events"]["entities"][group_id]:
                # event does not exist in definition
                json_definition["protocols"]["cypress-ezserial"]["packets"]["events"]["entities"][group_id][event_id] = OrderedDict()

            # update name
            json_definition["protocols"]["cypress-ezserial"]["packets"]["events"]["entities"][group_id][event_id]["name"] = event_def["name"]

            # identify event parameters
            if event_def["parameters"] is None:
                json_definition["protocols"]["cypress-ezserial"]["packets"]["events"]["entities"][group_id][event_id]["event_args"] = []
                param_str = ""
            else:
                if "event_args" not in json_definition["protocols"]["cypress-ezserial"]["packets"]["events"]["entities"][group_id][event_id]:
                    json_definition["protocols"]["cypress-ezserial"]["packets"]["events"]["entities"][group_id][event_id]["event_args"] = []
                for index, param in enumerate(event_def["parameters"]):
                    if len(json_definition["protocols"]["cypress-ezserial"]["packets"]["events"]["entities"][group_id][event_id]["event_args"]) == index:
                        # argument does not exist in list
                        json_definition["protocols"]["cypress-ezserial"]["packets"]["events"]["entities"][group_id][event_id]["event_args"].append(OrderedDict())
                    json_definition["protocols"]["cypress-ezserial"]["packets"]["events"]["entities"][group_id][event_id]["event_args"][index]["name"] = param["name"]
                    json_definition["protocols"]["cypress-ezserial"]["packets"]["events"]["entities"][group_id][event_id]["event_args"][index]["type"] = param["type"]
                    if "format" in param:
                        json_definition["protocols"]["cypress-ezserial"]["packets"]["events"]["entities"][group_id][event_id]["event_args"][index]["format"] = param["format"]
                    if "shortdesc" in param:
                        json_definition["protocols"]["cypress-ezserial"]["packets"]["events"]["entities"][group_id][event_id]["event_args"][index]["shortdesc"] = param["shortdesc"]
                param_str = ', '.join(["%s %s" % (param["type"], param["name"]) for param in event_def["parameters"]])
            print("            %s/%s: ezs_evt_%s_%s(%s)" % (
                    group_id,
                    event_id,
                    group_def["name"],
                    event_def["name"],
                    param_str))

# write modified definitions back into file
with open("../../perilib-definitions/cypress_ezserial.json", "w") as f:
    json.dump(json_definition, f, indent=4)
    f.write("\n")
