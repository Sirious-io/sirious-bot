import discord, config

Cointicker = config.config["BotCoinName"]

try:
    import balManage
except:
    import bankman.balManage as balManage


async def balance(ctx, user):
    embed = discord.Embed()

    embed.set_author(name=str(user) + "'s", icon_url=(user).avatar_url)
    embed.add_field(name='Balance is:', value=str(float(await balManage.balance(user.id))) + str(" ") +  str(Cointicker))
    await ctx.reply(embed=embed)


async def addBal(ctx, acc, amount):
    embed = discord.Embed()

    await balManage.addBal(acc, amount)
    embed.set_author(name=str(acc) + "'s")
    embed.add_field(name='Balance is:', value=str(float(await balManage.balance(acc))) + str(" ") +  str(Cointicker))
    await ctx.reply(embed=embed)
    
    



