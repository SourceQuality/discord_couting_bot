import os
import discord
import sqlite3
import string
import json
import sys

# Debugging initialization
print("Starting the bot script...", file=sys.stderr)
print("Debugging: Initializing variables...", file=sys.stderr)

# Function to retrieve environment variable with default value and log warnings
def get_env_var(name, default=None):
    value = os.environ.get(name, default)
    if value is None:
        print(f"Warning: Environment variable '{name}' is not set.", file=sys.stderr)
    return value

# Environment variables
tracked_phrases_str = get_env_var("PHRASE", "default_phrase")
tracked_phrases = [phrase.strip() for phrase in tracked_phrases_str.split(",") if phrase.strip()]
discord_api_token = get_env_var("DISCORD_TOKEN")
db_location = "/config/count_data.db"
response_mappings_str = get_env_var("RESPONSE_MAPPINGS", "{}")
response_mappings = json.loads(response_mappings_str)
aliases_str = get_env_var("ALIASES", "{}")
aliases = json.loads(aliases_str)

# Debugging print statements
print(f"Tracked phrases: {tracked_phrases}", file=sys.stderr)
print(f"Response mappings: {response_mappings}", file=sys.stderr)
print(f"Aliases: {aliases}", file=sys.stderr)

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

# Create the SQLite3 database
def initialize_database():
    with sqlite3.connect(db_location) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS count_data
                     (server_id TEXT, channel TEXT, name TEXT COLLATE NOCASE, phrase_name TEXT COLLATE NOCASE, phrase_count INTEGER)''')
        conn.commit()

initialize_database()

# Use the Discord client
client = discord.Client(intents=intents)

# Connect to Discord
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!', file=sys.stderr)

# Extract canonical name considering aliases
def get_canonical_name(name):
    for canonical, names in aliases.items():
        if name.lower() in [n.lower() for n in names]:
            return canonical
    return name

# Listen for messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    username = message.author.display_name.split("#")[0]
    channel_name = message.channel.name
    user_message = message.content.lower()

    print(f'{username} said "{message.content}" in {channel_name}', file=sys.stderr)

    phrase_name = None
    name = None

    print(f"User message: {user_message}", file=sys.stderr)

    for phrase in tracked_phrases:
        if phrase in user_message:
            phrase_name = phrase
            name_part = user_message.replace(phrase, "").strip().strip(",.!?")  # Remove the phrase and punctuation
            print(f"Extracted name part: {name_part}", file=sys.stderr)
            for alias in aliases.values():
                for possible_name in alias:
                    if possible_name.lower() in name_part.lower():
                        name = possible_name
                        break
                if name:
                    break
            if not name:
                name = name_part.split()[0] if name_part else None
            print(f"Name extracted: {name}", file=sys.stderr)
            break

    if phrase_name and name:
        canonical_name = get_canonical_name(name)
        capital_name = string.capwords(canonical_name)
        print(f"Canonical name: {canonical_name}", file=sys.stderr)
        print(f"Capitalized name: {capital_name}", file=sys.stderr)

        with sqlite3.connect(db_location) as conn:
            c = conn.cursor()
            server_id = str(message.guild.id)
            channel_id = str(message.channel.id)

            print(f"Checking database for phrase: '{phrase_name}' and name: '{canonical_name}'", file=sys.stderr)
            c.execute('''SELECT phrase_count FROM count_data
                         WHERE server_id = ? AND phrase_name = ? AND name = ? COLLATE NOCASE''',
                      (server_id, phrase_name, canonical_name))
            result = c.fetchone()

            if result is None:
                phrase_count = 1
                c.execute('''INSERT INTO count_data (server_id, channel, name, phrase_name, phrase_count)
                             VALUES (?, ?, ?, ?, ?)''',
                          (server_id, channel_id, canonical_name, phrase_name, phrase_count))
                print(f"Inserted new entry: {canonical_name} with count {phrase_count}", file=sys.stderr)
            else:
                phrase_count = result[0] + 1
                c.execute('''UPDATE count_data SET phrase_count = ?
                             WHERE server_id = ? AND phrase_name = ? AND name = ? COLLATE NOCASE''',
                          (phrase_count, server_id, phrase_name, canonical_name))
                print(f"Updated entry: {canonical_name} with new count {phrase_count}", file=sys.stderr)

            conn.commit()

        print(f"Response Mappings for '{phrase_name}': {response_mappings.get(phrase_name, 'Not found')}", file=sys.stderr)

        if phrase_name in response_mappings:
            response_template = response_mappings[phrase_name]
            required_placeholders = ['{phrase_count}']
            for placeholder in required_placeholders:
                if placeholder not in response_template:
                    print(f"Error: Placeholder '{placeholder}' missing in response template for phrase '{phrase_name}'", file=sys.stderr)
                    return
            try:
                bot_response = response_template.format(
                    username=username, capital_name=capital_name, phrase_count=phrase_count, name=name
                )
                bot_response = bot_response.replace("{name}", capital_name)
                print(f"Sending response: {bot_response}", file=sys.stderr)
                await message.channel.send(bot_response)
            except KeyError as e:
                print(f"KeyError while formatting response: {e}", file=sys.stderr)
        else:
            print(f"Error: Phrase '{phrase_name}' not found in response mappings", file=sys.stderr)
    else:
        print("No matching phrase or name found in message.", file=sys.stderr)

client.run(discord_api_token)
