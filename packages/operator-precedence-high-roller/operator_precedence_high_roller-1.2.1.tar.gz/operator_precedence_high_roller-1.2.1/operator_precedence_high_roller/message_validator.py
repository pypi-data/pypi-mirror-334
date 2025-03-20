import discord
def channel_valid(message: discord.Message):
    keywords = [
        'dnd',
        "dice",
        "rolls",
        "dumpster",
        "box-of-doom",
        "gamblers"
    ]
    valid = False
    for word in keywords:
        if word in message.channel.name: valid = True
    return valid

def message_is_command(message: discord.Message):
    return (
        len(message.content) > 0 and (
            message.content[0] == '!' or 
            message.content in ['odds', 'evens']
        )
    )