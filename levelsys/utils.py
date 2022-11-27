import json, config

#TODO: make this use firebase

file = config.config["levelDB"]

# Utils
async def levelToXP(level):
    return level ** 4, (level+1) ** 4

async def XPtoLevel(xp):
    return xp ** 0.25, (xp ** 0.25) + 1

async def openFile(file = file):
    with open(file, 'r') as f:
        return json.load(f)

async def writeFile(data, file = file):
    with open(file, 'w') as f:
        json.dump(data, f)

async def getLeaders(amount):
    users = await openFile()

    if amount > len(users.keys()):
        amount = len(users.keys())

    leaders = {}

    for i in range(amount):
        userXP = {}
        for user in users:
            if user not in leaders:
                userXP[user] = users[user]["experience"]

        name = str(list(userXP.keys())[list(userXP.values()).index(max(list(userXP.values())))])

        leaders[name] = [max(list(userXP.values()))]

    return leaders
