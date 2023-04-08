import os
import discord
import sqlite3
import string

#Env variables
channel_name = os.environ("CHANNEL_NAME")
tracked_phrases = os.environ("PHRASE")
discord_api_token = os.environ("DISCORD_TOKEN")


#discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

#Creat the sqlite3 database
conn = sqlite3.connect('/data/count_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS count_data
             (server_id text, channel text, name text, phrase_name text, phrase_count integer)''')
conn.commit()
conn.close()


#Use the discord client
client = discord.Client(intents=intents)

#Connect to discord
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
    phrase_name = None

    print(f' {username} said "{user_message}" in {channel}')

    for phrase in tracked_phrases:
        if phrase in user_message.lower():
            phrase_name = phrase
            break
  
    if message.author == client.user:
        return


    if channel == channel_name:
        if phrase_name is not None:
            conn = sqlite3.connect('/data/count_data.db')
            c = conn.cursor()
            server_id = str(message.guild.id)
            channel = str(message.channel.id)
            name = phrase_name.split(' ', 1)[1]
            capital_name = string.capwords(name)
            c.execute('''SELECT phrase_count FROM count_data
                          WHERE server_id = ? AND phrase_name = ? AND name = ?''', (server_id, phrase_name, name))
            result = c.fetchone()
            if result is None:
                phrase_count = 1
                c.execute('''INSERT INTO count_data (server_id, phrase_name, name, phrase_count)
                              VALUES (?, ?, ?, ?)''', (server_id, phrase_name, name, phrase_count))
            else:
                phrase_count = result[0] + 1
                c.execute('''UPDATE count_data SET phrase_count = ?
                              WHERE server_id = ? AND phrase_name = ?''', (phrase_count, server_id, phrase_name))
            conn.commit()
            conn.close()
            await message.channel.send(f"{capital_name} has been fucked {phrase_count} times.")
        return


client.run(discord_api_token)
