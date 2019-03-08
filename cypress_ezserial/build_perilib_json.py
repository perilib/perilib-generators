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
    group_id = group_def["id"]
    print("    %s: %s" % (group_id, group_def["name"]))
    
    # step through each command/response pair in this group, if any
    if "commands" in group_def:
        print("        commands:")

        # add dictionary key for this class ID in the command set
        if group_id not in json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"]:
            json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"][group_id] = OrderedDict()

        # add/update relevant class details
        json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"][group_id]["name"] = group_def["name"]

        for command_def in group_def["commands"]:
            command_id = command_def["id"]
            command_def_json = OrderedDict({ "name": command_def["name"] })

            # identify command parameters
            if command_def["parameters"] is None:
                command_def_json["command_args"] = []
                param_str = ""
            else:
                command_def_json["command_args"] = [OrderedDict({ "name": param["name"], "type": param["type"] }) for param in command_def["parameters"]]
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
                    command_def_json["response_args"] = []
                    param_str = ""
                else:
                    command_def_json["response_args"] = [OrderedDict({ "name": param["name"], "type": param["type"] }) for param in command_def["returns"]]
                    param_str = ', '.join(["%s %s" % (param["type"], param["name"]) for param in command_def["returns"]])
                print("            %s/%s: ezs_rsp_%s_%s(%s)" % (
                        group_id,
                        command_id,
                        group_def["name"],
                        command_def["name"],
                        param_str))
            else:
                print("            %d/%d: NOTE: COMMAND HAS NO RESPONSE" % (int(group_def["id"]), int(command_def["id"])))
                
            # add/update command definition in JSON structure
            json_definition["protocols"]["cypress-ezserial"]["packets"]["commands"][group_id][command_id] = command_def_json

    # step through each event in this class, if any
    if "events" in group_def:
        print("        events:")

        # add dictionary key for this class ID in the event set
        if group_id not in json_definition["protocols"]["cypress-ezserial"]["packets"]["events"]:
            json_definition["protocols"]["cypress-ezserial"]["packets"]["events"][group_id] = OrderedDict()

        # add/update relevant class details
        json_definition["protocols"]["cypress-ezserial"]["packets"]["events"][group_id]["name"] = group_def["name"]

        for event_def in group_def["events"]:
            event_id = event_def["id"]
            event_def_json = OrderedDict({ "name": event_def["name"] })

            # identify event parameters
            if event_def["parameters"] is None:
                event_def_json["event_args"] = []
                param_str = ""
            else:
                event_def_json["event_args"] = [OrderedDict({ "name": param["name"], "type": param["type"] }) for param in event_def["parameters"]]
                param_str = ', '.join(["%s %s" % (param["type"], param["name"]) for param in event_def["parameters"]])
            print("            %s/%s: ezs_evt_%s_%s(%s)" % (
                    group_id,
                    event_id,
                    group_def["name"],
                    event_def["name"],
                    param_str))
                    
            # add/update command definition in JSON structure
            json_definition["protocols"]["cypress-ezserial"]["packets"]["events"][group_id][event_id] = event_def_json

# write modified definitions back into file
with open("../../perilib-definitions/cypress_ezserial.json", "w") as f:
    json.dump(json_definition, f, indent=4)
