#TODO: make this use firebase


try:
    import utils
except:
    import bankman.utils as utils


async def addBal(user, amount):
    bank = await utils.openFile()
    try:
        bank[str(user)] += amount
        result = [bank[str(user)]-amount, bank[str(user)]]
    except KeyError:
        bank[str(user)] = amount
        result = [0, amount]

    await utils.writeFile(bank)
    return result

async def moveBal(fromAcc, toAcc, amount):

    if await balance(fromAcc) > amount or await balance(fromAcc) == amount:
        await removeBal(fromAcc, amount)
        await addBal(toAcc, amount)
        result = True
    else:
        result = False

    return result


async def removeBal(user, amount):
    bank = await utils.openFile()
    result = [False]
    try:
        if amount < await balance(user):
            bank[str(user)] -= amount
            await utils.writeFile(bank)
            result = [True]
    except KeyError:
        result = [False]

    return result    


async def balance(user):
    bank = await utils.openFile()
    try:
        return bank[str(user)]
    except KeyError:
        return 0 


