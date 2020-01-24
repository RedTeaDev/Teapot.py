import json
from discord.ext import commands
import teapot


def __init__(bot):
    """ Initialize events """
    join(bot)
    leave(bot)
    on_command_error(bot)
    message_edit(bot)
    message_delete(bot)


def join(bot):
    @bot.event
    async def on_member_join(member):
        if teapot.config.storage_type() == "mysql":
            try:
                database = teapot.database.__init__()
                db = teapot.database.db(database)
                db.execute("INSERT INTO " + str(
                    member.guild.id) + "_logs" + "(timestamp, guild_id, channel_id, user_id, action_type) VALUES(%s, %s, %s, %s, %s)",
                           (teapot.time(), member.guild.id, member.channel.id, member.id, "MEMBER_JOIN"))
                database.commit()
            except Exception as e:
                print(e)


def leave(bot):
    @bot.event
    async def on_member_remove(member):
        if teapot.config.storage_type() == "mysql":
            try:
                database = teapot.database.__init__()
                db = teapot.database.db(database)
                db.execute("INSERT INTO " + str(
                    member.guild.id) + "_logs" + "(timestamp, guild_id, channel_id, user_id, action_type) VALUES(%s, %s, %s, %s, %s)",
                           (teapot.time(), member.guild.id, member.channel.id, member.id, "MEMBER_REMOVE"))
                database.commit()
            except Exception as e:
                print(e)


def on_command_error(bot):
    @bot.event
    async def on_command_error(ctx, error):
        if teapot.config.storage_type() == "mysql":
            try:
                database = teapot.database.__init__()
                db = teapot.database.db(database)
                db.execute("INSERT INTO " + str(
                    ctx.guild.id) + "_logs" + "(timestamp, guild_id, channel_id, message_id, user_id, action_type, message) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                           (teapot.time(), ctx.guild.id, ctx.message.channel.id, ctx.message.id, ctx.message.author.id,
                            "CMD_ERROR", str(error)))
                database.commit()
            except Exception as e:
                print(e)


def message_edit(bot):
    @bot.event
    async def on_raw_message_edit(ctx):
        guild_id = json.loads(json.dumps(ctx.data))['guild_id']
        channel_id = json.loads(json.dumps(ctx.data))['channel_id']
        message_id = json.loads(json.dumps(ctx.data))['id']
        try:
            author_id = json.loads(json.dumps(json.loads(json.dumps(ctx.data))['author']))['id']
            content = json.loads(json.dumps(ctx.data))['content']
            if teapot.config.storage_type() == "mysql":
                try:
                    database = teapot.database.__init__()
                    db = teapot.database.db(database)
                    db.execute("INSERT INTO " + str(
                        guild_id) + "_logs" + "(timestamp, guild_id, channel_id, message_id, user_id, action_type, message) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                               (teapot.time(), guild_id, channel_id, message_id, author_id, "MESSAGE_EDIT", content))
                    database.commit()
                except Exception as e:
                    print(e)
            elif teapot.config.storage_type() == "flatfile":
                pass
        except:
            content = str(json.loads(json.dumps(ctx.data))['embeds'])
            if teapot.config.storage_type() == "mysql":
                try:
                    database = teapot.database.__init__()
                    db = teapot.database.db(database)
                    db.execute("INSERT INTO " + str(
                        guild_id) + "_logs" + "(timestamp, guild_id, channel_id, message_id, action_type, message) VALUES(%s, %s, %s, %s, %s, %s)",
                               (teapot.time(), guild_id, channel_id, message_id, "MESSAGE_EDIT", content))
                    database.commit()
                except Exception as e:
                    print(e)
            elif teapot.config.storage_type() == "flatfile":
                pass


def message_delete(bot):
    @bot.event
    async def on_message_delete(ctx):
        if teapot.config.storage_type() == "mysql":
            try:
                database = teapot.database.__init__()
                db = teapot.database.db(database)
                db.execute("INSERT INTO " + str(
                    ctx.guild.id) + "_logs" + "(timestamp, guild_id, channel_id, message_id, user_id, action_type) VALUES(%s, %s, %s, %s, %s, %s)",
                           (teapot.time(), ctx.guild.id, ctx.channel.id, ctx.id, ctx.author.id, "MESSAGE_DELETE"))
                database.commit()
            except Exception as e:
                print(e)
        elif teapot.config.storage_type() == "flatfile":
            pass
