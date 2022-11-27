import random, config, discord
import bankman.balManage as balManage

casinoAccount = config.config["CasinoAccount"]
Cointicker = config.config["BotCoinName"]

async def gamble(ctx, amount):
    won = random.choice([casinoAccount, str(ctx.author.id)]) == str(ctx.author.id)

    if amount < await balManage.balance(casinoAccount) / 1.25 or amount == await balManage.balance(casinoAccount) / 1.25 or amount < await balManage.balance(ctx.author.id) or amount == await balManage.balance(ctx.author.id):
        if won:
            embed = discord.Embed(title="You won " + str(amount) + " " + Cointicker + " :tada:")
            embed.add_field(name="Your balance: ", value=str(await balManage.balance(str(ctx.author.id))) + " " + Cointicker)
        else:
            embed = discord.Embed(title="You lost " + str(amount) + " " + Cointicker + " :money_with_wings:")
            embed.add_field(name="Your balance: ", value=str(await balManage.balance(str(ctx.author.id))) + " " + Cointicker)

    if amount > await balManage.balance(casinoAccount) / 1.25:
        embed = discord.Embed(title=":x: Casino out of money, please try again later. :x:")

    if amount > await balManage.balance(ctx.author.id):
        embed = discord.Embed(title=":x: Insufficient funds. :x:")

    await ctx.send(embed=embed)