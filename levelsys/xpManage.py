try:
    import utils
except:
    import levelsys.utils as utils

async def add_experience(users, user, exp):
    users[str(user.id)]['experience'] += exp
    return users

async def registerMember(users, member):
    users[str(member.id)] = {}
    users[str(member.id)]['experience'] = 0
    users[str(member.id)]['level'] = 1
    return users

async def CheckLevel_up(users, user):
    experience = users[str(user.id)]['experience']
    lvl_start = users[str(user.id)]['level']
    lvl_end = int((await utils.XPtoLevel(experience))[0])
    if lvl_start < lvl_end:
        users[str(user.id)]['level'] = lvl_end
        return [True, lvl_end, experience]

    return [False]