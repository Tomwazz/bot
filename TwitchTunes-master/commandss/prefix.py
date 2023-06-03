import json

def get_prefix(bot, message):
    with open('prefix.json', 'r') as file:
        prefixes = json.load(file)
    channel_name = message.channel.name
    return prefixes.get(channel_name, "<")

def change_prefix(channel_name, new_prefix):
    with open('prefix.json', 'r') as file:
        prefixes = json.load(file)
    prefixes[channel_name] = new_prefix
    with open('prefix.json', 'w') as file:
        json.dump(prefixes, file)