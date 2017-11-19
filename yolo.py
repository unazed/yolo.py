import discord
import asyncio
import json
import sys
import aiohttp
import os
import importlib
import copy
import time


try:
    with open("config.json") as config:
        config = json.load(config)
except IOError:
    print("{*} 'config.json' doesn't exist, please create it with a 'token' field")
    sys.exit(1)

client = discord.Client()

command_prefix =    config['prefix']
command_map =       config['command_map']
default_channel =   config['default_channel']
api_link =          config['api_link']
command_folder =    config['commands_folder']

timeout = 10
if 'timeout' in config:
    timeout = int(config['timeout'])

global_last_cmd = time.time() - timeout

if not os.path.exists(command_folder):
    print("{*} %r doesn't exist, please create it." % command_folder)
    sys.exit(1)
elif not os.listdir(command_folder):
    print("{*} %r doesn't have any commands/files inside." % command_folder)
    sys.exit(1)
elif "__init__.py" not in os.listdir(command_folder):
    print("{*} %r doesn't have an __init__.py inside, please create it." % command_folder)
    sys.exit(1)

command_modules = {
    command: importlib.import_module("%s.%s" % (command_folder, command))  for command in command_map
}

command_modules = {
    k: getattr(v, k) for k, v in command_modules.items()
}


@client.event
async def on_message(message):
    global global_last_cmd
    
    try:
        content = message.content
        author = message.author
        name = author.name
        channel = message.channel
        ranks = [role.name for role in author.roles]
    except Exception as exc:
        print("{*} %s" % exc)
        return

    if not content.startswith(command_prefix):
        return

    if time.time() - global_last_cmd <= timeout:
        await client.send_message(message.channel, "<@%s>! Please wait at least %d seconds before executing another command." % 
            (author.id, timeout)
        )
        return

    global_last_cmd = time.time()
    command = content[len(command_prefix):].split()[0]

    if command not in command_modules:
        return
    elif not list(filter(lambda role: role in command_map[command], ranks)):
        await client.send_message(channel, "<@%s>, you have insufficient permissions!" % author.id)
        return

    print("%r entered a command, %s" % (name, command))

    _config = copy.deepcopy(config)
    _config['token'] = ''  # don't allow module to access token

    await command_modules[command](
        config=_config,
        bot=client,
        sender=author,
        channel=channel,
        content=content
    )


@client.event
async def on_member_join(member):
    server = member.server
    channel = server.get_channel(default_channel)

    await client.send_message(channel, "<@%s>, welcome to %s!" % (member.id, server.name))


client.run(config['token'])