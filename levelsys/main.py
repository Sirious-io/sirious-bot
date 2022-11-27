import discord

#Imports from dir
try:
    import utils, xpManage
except:
    import levelsys.utils as utils
    import levelsys.xpManage as xpManage


async def memberJoin(member):
    users = await xpManage.registerMember(await utils.openFile(), member)
    await utils.writeFile(users)

async def onMessage(client, message):
    guild = message.guild
    memberList = guild.members

    users = await utils.openFile()
    for member in memberList:
        if not message.guild.get_member(member.id).bot and not str(member.id) in users:
            users = await xpManage.registerMember(users, member)
    await utils.writeFile(users)



    if message.author.bot == False:
        users = await utils.openFile()
        users = await xpManage.add_experience(users, message.author, 5)
        data = await xpManage.CheckLevel_up(users, message.author)
        await utils.writeFile(users)
        if data[0]:
            await levelup(message, data[1])


    await client.process_commands(message)

async def rank(ctx, member):
    users = await utils.openFile()

    id = member.id
    xp = users[str(id)]['experience']
    level = users[str(id)]['level']

    xpEnd = (await utils.levelToXP(level))[1]
    xpStart = (await utils.levelToXP(level))[0]

    percentage = float(str('{:.1%}'.format(float(xp - xpStart)/float(xpEnd - xpStart))).replace("%", ""))
    blocksShown = 15
    blocks = int(round(percentage, 0) / (100 /blocksShown))

    embed=discord.Embed(title=member.name + "'s stats")
    embed.add_field(name="Name", value=member.mention, inline=True)
    embed.add_field(name="XP", value=str(xp - xpStart) + " / " + str(xpEnd - xpStart), inline=True)
    embed.add_field(name="Level", value="lvl " + str(level), inline=True)
    embed.add_field(name="Progress Bar", value=(blocks*":blue_square:") + ((blocksShown - blocks)*":black_large_square:") + " " + str(percentage) + "%", inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)

async def leaderBoard(ctx, client):
    leaders = await utils.getLeaders(10)
    embed=discord.Embed(title=ctx.guild.name + "'s leaderboard")
    rank = 0

    for i in range(len(list(leaders.keys()))):
        rank +=1 # message.guild.get_member(int(list(leaders.keys())[i])).bot
        id = int(list(leaders.keys())[i])
        user = ctx.guild.get_member(id)
        userXP = leaders[str(id)][0]
        embed.add_field(name="‍", value="> | **" + str(rank) + ".** ``" + user.name + "#" + user.discriminator + "``\n> |    ``" + str(userXP) + " XP, lvl " + str(int((await utils.XPtoLevel(userXP))[0])) + "``", inline=False)

    embed.set_thumbnail(url=ctx.guild.icon_url)
    
    await ctx.send(embed=embed)

async def levelup(ctx, level):
    await ctx.reply(ctx.author.mention + " leveled up to level " + str(level) + "!")




# mod funcs

async def addLevel(ctx):
    users = await utils.openFile()
    data = [False]
    while not data[0]:
        users = await xpManage.add_experience(users, ctx.author, 5)
        data = await xpManage.CheckLevel_up(users, ctx.author)
    await utils.writeFile(users)
    await ctx.send("Leveled up to: " + str(data[1]) + ", XP: " + str(data[2]))

async def addExp(ctx, amount: int = 100):
    users = await utils.openFile()
    ogExp = users[str(ctx.author.id)]['experience']
    await xpManage.add_experience(users, ctx.author, amount)
    await xpManage.CheckLevel_up(users, ctx.author)
    await utils.writeFile(users)
    await ctx.send(str(ogExp) + " XP --> " + str(ogExp + amount) + " XP")
