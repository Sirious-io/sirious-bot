import discord, calendar, time


#Local config
from config import config

#Local files
import mod.utils as utils
from mod.logs import main as modlogs




# TODO: Add appeals

async def lock_channel(client, ctx, db, reason):
    role = discord.utils.get(ctx.guild.roles, id=config["roles"]["Member"])
    await ctx.channel.set_permissions(role, send_messages=False)

    embed=discord.Embed()
    embed.add_field(name="🔐 **Channel locked** 🔐", value=reason)
    embed.set_thumbnail(url=ctx.author.avatar_url)

    await ctx.reply(embed=embed)

async def delete_message_contextMenu(client, ctx):
    await modlogs.deleted_message(client, ctx.target_message.author, ctx.author.mention, ctx.channel, ctx.target_message)
    await ctx.target_message.delete()

    embed=discord.Embed()
    embed.add_field(name="👀 **Message deleted** 👀", value="Censorship!!!")
    embed.set_thumbnail(url=ctx.author.avatar_url)

    await ctx.reply(embed=embed)

# User moderation
    
async def warn_member(client, db, ctx, moderator, target, reason):

    utils.update_case(db, case_id=None, data={"Moderator": str(moderator.id), "Reason": reason, "Target": str(target.id), "Time": int(time.time()), "Type": "Warn", "is_valid": True}) #case_id= because easier to read
    await client.get_channel(config["mod_log"]).send(embed=discord.Embed(title="Warn issued", description="> **Moderator:** " + moderator.mention + "\n\n> **Target:** " + target.mention + "\n\n> **Reason:** " + reason + "\n\n> [**Review appeal**](https://google.com)", color=0xf0fc03).set_thumbnail(url=moderator.avatar_url))
    dm = await target.create_dm(); await dm.send(embed=discord.Embed(title="You have been warned!", description="> **Moderator:** " + moderator.mention + "\n\n> **Reason:** " + reason + "\n\n> [**Appeal your warn**](https://google.com)", color=0xed5555).set_thumbnail(url=moderator.avatar_url))

    embed=discord.Embed()
    embed.add_field(name="⚠ **Warned member** ⚠", value= target.mention + ", " + reason)
    embed.set_thumbnail(url=moderator.avatar_url)

    await ctx.reply(embed=embed)

async def kick_member(client, db, ctx, moderator, target, reason):

    utils.update_case(db, case_id=None, data={"Moderator": str(moderator.id), "Reason": reason, "Target": str(target.id), "Time": int(time.time()), "Type": "Kick", "is_valid": True}) #case_id= because easier to read
    await client.get_channel(config["mod_log"]).send(embed=discord.Embed(title="Kick issued", description="> **Moderator:** " + moderator.mention + "\n\n> **Target:** " + target.mention + "\n\n> **Reason:** " + reason + "\n\n> [**Review appeal**](https://google.com)", color=0xf0fc03).set_thumbnail(url=moderator.avatar_url))
    dm = await target.create_dm(); await dm.send(embed=discord.Embed(title="You have been warned!", description="> **Moderator:** " + moderator.mention + "\n\n> **Reason:** " + reason + "\n\n> [**Appeal your kick**](https://google.com)", color=0xed5555).set_thumbnail(url=moderator.avatar_url))
    await target.kick()

    embed=discord.Embed()
    embed.add_field(name="👢 **Kicked member** 👢", value= target.mention + ", " + reason)
    embed.set_thumbnail(url=moderator.avatar_url)

    await ctx.reply(embed=embed)



async def ban_member(client, db, ctx, moderator, target, reason):

    utils.update_case(db, case_id=None, data={"Moderator": str(moderator.id), "Reason": reason, "Target": str(target.id), "Time": int(time.time()), "Type": "Ban", "is_valid": True}) #case_id= because easier to read
    await client.get_channel(config["mod_log"]).send(embed=discord.Embed(title="Ban issued", description="> **Moderator:** " + moderator.mention + "\n\n> **Target:** " + target.mention + "\n\n> **Reason:** " + reason + "\n\n> [**Review appeal**](https://google.com)", color=0xf0fc03).set_thumbnail(url=moderator.avatar_url))
    dm = await target.create_dm(); await dm.send(embed=discord.Embed(title="You have been banned from ``" + config["server_name"] + "``!", description="> **Moderator:** " + moderator.mention + "\n\n> **Reason:** " + reason + "\n\n> [**Appeal your ban**](https://google.com)", color=0xed5555).set_thumbnail(url=moderator.avatar_url))
    await target.ban()

    embed=discord.Embed()
    embed.add_field(name="🔨 **Banned member** 🔨", value= target.mention + ", " + reason)
    embed.set_thumbnail(url=moderator.avatar_url)

    await ctx.reply(embed=embed)

async def mute_member(client, db, ctx, moderator, target, reason):
    
    utils.update_case(db, case_id=None, data={"Moderator": str(moderator.id), "Reason": reason, "Target": str(target.id), "Time": int(time.time()), "Type": "Mute", "is_valid": True}) #case_id= because easier to read
    await client.get_channel(config["mod_log"]).send(embed=discord.Embed(title="Mute issued", description="> **Moderator:** " + moderator.mention + "\n\n> **Target:** " + target.mention + "\n\n> **Reason:** " + reason + "\n\n> [**Review appeal**](https://google.com)", color=0xf0fc03).set_thumbnail(url=moderator.avatar_url))
    dm = await target.create_dm(); await dm.send(embed=discord.Embed(title="You have been muted!", description="> **Moderator:** " + moderator.mention + "\n\n> **Reason:** " + reason + "\n\n> [**Appeal your mute**](https://google.com)", color=0xed5555).set_thumbnail(url=moderator.avatar_url))

    role = discord.utils.get(target.guild.roles, id=config["roles"]["Muted"])
    await target.add_roles(role)

    embed=discord.Embed()
    embed.add_field(name="🔉 **Muted member** 🔉", value= target.mention + ", " + reason)
    embed.set_thumbnail(url=moderator.avatar_url)

    await ctx.reply(embed=embed)




async def view_background(client, db, ctx, member):

    invalid, valid = "‍", "‍"
    if db.collection("target_links").document(str(member.id)).get().exists:
        for case in db.collection("target_links").document(str(member.id)).get().to_dict().values():
            case_info = db.collection("cases").document(case).get().to_dict()

            if case_info["Type"] == "Mute": emoji = "🔇"
            elif case_info["Type"] == "Warn": emoji = "⚠"
            elif case_info["Type"] == "Kick": emoji = "🥾"
            elif case_info["Type"] == "Ban": emoji = "🔨"
            

            if case_info["is_valid"]:
                valid += "\n> **" + emoji + " " + case_info["Reason"] + ":**\n> <t:" + str(case_info["Time"]) + ":F> • <@" + str(case_info["Moderator"]) + ">"

            elif not case_info["is_valid"]:
                invalid += "\n> **" + emoji + " " + case_info["Reason"] + ":**\n> <t:" + str(case_info["Time"]) + ":F> • <@" + str(case_info["Moderator"]) + ">"

    else:
        valid, invalid = "‍", "‍"


    embed=discord.Embed()
    embed.add_field(name="ℹ️ **User Info**", value=f"**User ID:** {member.id}\n**Created:** <t:{calendar.timegm(member.created_at.utctimetuple())}:D> (<t:{calendar.timegm(member.created_at.utctimetuple())}:R>)\n**Joined:** <t:{calendar.timegm(member.joined_at.utctimetuple())}:D> (<t:{calendar.timegm(member.joined_at.utctimetuple())}:R>)")
    if not valid == "‍":   embed.add_field(name="🟢 Valid cases:", value=valid, inline=False)
    if not invalid == "‍": embed.add_field(name="‍\n🔴 Invalid cases:", value=invalid, inline=False)
    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)

