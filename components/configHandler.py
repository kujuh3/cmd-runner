import json
from .colors import colors


def loadConfig(path):
    indexes = {}

    with open(f"{path}/conditions.json") as file:
        config = json.load(file)

    for i, item in enumerate(config):
        indexes[item["command"]] = i

    return config, indexes


def saveConfig(object, path):
    newConfig = loadConfig(path)
    newConfig.append(object)

    with open(f"{path}/conditions.json", "w") as file:
        file.write(json.dumps(newConfig, indent=4))


def addConfig(path):
    newConfig = {
        "name": "This is just a name for the configuration",
        "command": "This means the command that triggers the configuration",
        "depends": "This should include the command to be executed when trigger command was initiated",
        "condition": "Conditions based on which True or False should be returned. Separate by commas. \nEX: upon command 'echo hello world' I want depends command 'check hello-world' to determine truthy based on these conditions: 'mycondition1,mycondition2'.\nThese conditions are checked with an 'if in' statement, row by row from the depends commands output."
    }
    for i in newConfig:
        while True:
            try:
                print(f"\n{colors.WARNING}{newConfig[i]}")
                value = input(
                    f"{colors.INPUT}Input value for configuration '{i}'{colors.ENDC}: ")
                newConfig[i] = value
                break
            except Exception as e:
                print(e)

    newConfig["condition"] = newConfig["condition"].split(",")
    saveConfig(newConfig, path)
