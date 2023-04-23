import os
import discord
import sqlite3
import string

#Env variables
tracked_phrases_str = os.environ.get("PHRASE")
tracked_phrases = tracked_phrases_str.split(",")
discord_api_token = os.environ["DISCORD_TOKEN"]
db_location = "/config/count_data.db"
bot_response_template = os.environ["RESPONSE"]


#discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

#Creat the sqlite3 database
conn = sqlite3.connect(db_location)
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

#listen for messages
@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)
    phrase_name = None

    #Print the message to the log
    print(f' {username} said "{user_message}" in {channel}')

    #Loop through each tracked phrase and check if it exists in the tracked phrases variable
    for phrase in tracked_phrases:
        if phrase in user_message.lower():
            phrase_name = phrase
            break
  #Do nothing if the user is the bot itself
    if message.author == client.user:
        return



    if phrase_name is not None:
        #Connect to DB
        conn = sqlite3.connect(db_location)
        c = conn.cursor()
        server_id = str(message.guild.id)
        channel = str(message.channel.id)
        name = phrase_name.split(' ', 1)[1]
        capital_name = string.capwords(name)
        #Select name from table
        c.execute('''SELECT phrase_count FROM count_data
                      WHERE server_id = ? AND phrase_name = ? AND name = ?''', (server_id, phrase_name, name))
        result = c.fetchone()
        #Create data and set count to 1 if it doesn't exist
        if result is None:
            phrase_count = 1
            c.execute('''INSERT INTO count_data (server_id, phrase_name, name, phrase_count)
                          VALUES (?, ?, ?, ?)''', (server_id, phrase_name, name, phrase_count))
        #Update count + 1 if the value exists
        else:
            phrase_count = result[0] + 1
            c.execute('''UPDATE count_data SET phrase_count = ?
                          WHERE server_id = ? AND phrase_name = ?''', (phrase_count, server_id, phrase_name))
        conn.commit()
        conn.close()
        #Format the varaible so the bot sends the actual variables and not just the string.
        bot_response = bot_response_template.format(username=username, capital_name=capital_name, phrase_count=phrase_count)
        #Send message into discord channel
        await message.channel.send(bot_response)
    return


client.run(discord_api_token)
