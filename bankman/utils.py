import json, config

file = config.config["BankDB"]


async def openFile(file = file):
    with open(file, 'r') as f:
        return json.load(f)

async def writeFile(data, file = file):
    with open(file, 'w') as f:
        json.dump(data, f)

