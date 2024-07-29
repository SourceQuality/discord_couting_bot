import json
import os
import discord
import sqlite3
import string
import sys

# Print a startup message to ensure script execution
print("Starting the bot script...", file=sys.stdout)

# Add more debugging prints throughout your script
print("Debugging: Initializing variables...", file=sys.stdout)


# Environment variables
tracked_phrases_str = os.environ.get("PHRASE", "")
tracked_phrases = tracked_phrases_str.split(",") if tracked_phrases_str else []
discord_api_token = os.environ.get("DISCORD_TOKEN", "")
response_mappings_str = os.environ.get("RESPONSE_MAPPINGS", "{}")
response_mappings = json.loads(response_mappings_str) if response_mappings_str else {}
aliases_str = os.environ.get("ALIASES", "{}")
aliases = json.loads(aliases_str) if aliases_str else {}
db_location = "/config/count_data.db"  # Make sure this is the correct path

# Debugging: Print loaded environment variables
print(f"Tracked Phrases: {tracked_phrases}")
print(f"Discord API Token: {discord_api_token[:10]}...")  # Masked for security
print(f"Response Mappings: {response_mappings}")
print(f"Aliases: {aliases}")
print(f"Database Location: {db_location}")

# Function to get the canonical name from an alias
def get_canonical_name(name):
    print(f"Resolving canonical name for: {name}")
    for canonical, alias_list in aliases.items():
        if name.lower() == canonical.lower() or name.lower() in map(str.lower, alias_list):
            print(f"Found canonical name: {canonical} for alias: {name}")
            return canonical
    print(f"No canonical name found for: {name}. Returning original.")
    return name

# Discord intents
intents = discord.Intents.default()
intents.message_content = True

# Create the SQLite3 database
def create_database():
    with sqlite3.connect(db_location) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS count_data
                     (server_id TEXT, channel TEXT, name TEXT, phrase_name TEXT, phrase_count INTEGER)''')
        conn.commit()
    print("Database schema created.")

create_database()

# Use the Discord client
client = discord.Client(intents=intents)

# Connect to Discord
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# Listen for messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    username = message.author.display_name.split("#")[0]
    channel_name = message.channel.name
    user_message = message.content.lower()

    # Print the message to the log
    print(f'{username} said "{message.content}" in {channel_name}')

    # Check for tracked phrases and extract the name
    phrase_name = None
    name = None

    print(f"User message: {user_message}")

    for phrase in tracked_phrases:
        if phrase in user_message:
            phrase_name = phrase
            name_part = user_message.replace(phrase, "").strip().strip(",.!?")  # Remove the phrase and punctuation
            name = name_part.split()[0] if name_part else None
            print(f"Matched phrase: {phrase}")
            print(f"Extracted name part: {name_part}")
            print(f"Name extracted: {name}")
            break

    if phrase_name and name:
        canonical_name = get_canonical_name(name)
        capital_name = string.capwords(canonical_name)
        print(f"Canonical name: {canonical_name}")
        print(f"Capitalized name: {capital_name}")

        # Connect to DB
        with sqlite3.connect(db_location) as conn:
            c = conn.cursor()
            server_id = str(message.guild.id)
            channel_id = str(message.channel.id)

            print(f"Checking database for phrase: '{phrase_name}' and name: '{canonical_name}'")
            c.execute('''SELECT phrase_count FROM count_data
                         WHERE server_id = ? AND phrase_name = ? AND name = ?''',
                      (server_id, phrase_name, canonical_name))
            result = c.fetchone()

            if result is None:
                phrase_count = 1
                c.execute('''INSERT INTO count_data (server_id, channel, name, phrase_name, phrase_count)
                             VALUES (?, ?, ?, ?, ?)''',
                          (server_id, channel_id, canonical_name, phrase_name, phrase_count))
                print(f"Inserted new entry: {canonical_name} with count {phrase_count}")
            else:
                phrase_count = result[0] + 1
                c.execute('''UPDATE count_data SET phrase_count = ?
                             WHERE server_id = ? AND phrase_name = ? AND name = ?''',
                          (phrase_count, server_id, phrase_name, canonical_name))
                print(f"Updated entry: {canonical_name} with new count {phrase_count}")

            conn.commit()

        # Debug output to check response_mappings
        print(f"Response Mappings for '{phrase_name}': {response_mappings.get(phrase_name, 'Not found')}")

        # Ensure placeholders are in response mapping
        if phrase_name in response_mappings:
            response_template = response_mappings[phrase_name]
            # Check for required placeholders
            required_placeholders = ['{name}', '{phrase_count}']
            for placeholder in required_placeholders:
                if placeholder not in response_template:
                    print(f"Error: Placeholder '{placeholder}' missing in response template for phrase '{phrase_name}'")
                    return
            try:
                bot_response = response_template.format(
                    username=username, capital_name=capital_name, phrase_count=phrase_count
                )
                print(f"Sending response: {bot_response}")
                await message.channel.send(bot_response)
            except KeyError as e:
                print(f"KeyError while formatting response: {e}")
        else:
            print(f"Error: Phrase '{phrase_name}' not found in response mappings")
    else:
        print("No matching phrase or name found in message.")

client.run(discord_api_token)
