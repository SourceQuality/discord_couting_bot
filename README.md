Discord Counter Bot
This bot tracks specific phrases in Discord messages, updates a SQLite database with counts for each phrase, and maps phrases to custom responses. It also handles aliases for names to track variations of a name as one entry.

Features
Phrase Tracking: Track occurrences of specific phrases in Discord messages.
Alias Handling: Map multiple aliases to a single canonical name.
Custom Responses: Define custom responses based on the tracked phrases.
Case-Insensitive Storage: Store names in a case-insensitive manner in the SQLite database.
Requirements
Python 3.7 or later
discord.py library
SQLite database
Docker (for running the bot in a container)
Setup
Environment Variables
Ensure the following environment variables are set:

DISCORD_TOKEN: Your Discord bot token.
PHRASE: A comma-separated list of phrases to track.
RESPONSE_MAPPINGS: A JSON string mapping phrases to custom response templates.
ALIASES: A JSON string mapping canonical names to lists of aliases.
Example
Here is an example of a .env file:

plaintext
Copy code
DISCORD_TOKEN=your_discord_bot_token
PHRASE="great work,bad work"
RESPONSE_MAPPINGS={"great work": "{capital_name} has done {phrase_count} great works.", "bad work": "{capital_name} has messed up {phrase_count} times."}
ALIASES={"gene": ["danny", "daniel"], "ryan": ["ryguy", "ryannickname"]}
Docker Compose Setup
Create a docker-compose.yml file with the following content:

yaml
Copy code
version: "3.8"
services:
  discordcounter:
    image: discordcoutingbot:latest
    volumes:
      - discordcounter:/config
    environment:
      - DISCORD_TOKEN=your_discord_bot_token
      - PHRASE="great work,bad work"
      - RESPONSE_MAPPINGS={"great work": "{capital_name} has done {phrase_count} great works.", "bad work": "{capital_name} has messed up {phrase_count} times."}
      - ALIASES={"gene": ["danny", "daniel"], "ryan": ["ryguy", "ryannickname"]}
    restart: unless-stopped
volumes:
  discordcounter:
Running the Bot
Build and run the Docker container:

sh
Copy code
docker-compose up --build
The bot will connect to Discord and start tracking phrases based on your configuration.

Development
Debugging
The bot includes detailed debugging output to help you understand its operation. Debug messages are printed to standard error.

Code Modifications
Database: The SQLite database is created with case-insensitive columns for names and phrases.
Response Formatting: Custom responses are formatted based on phrase mappings, with support for placeholders like {capital_name} and {phrase_count}.
Contributing
Feel free to fork this repository and submit pull requests. For any issues or feature requests, please open an issue on the repository.

License
This project is licensed under the MIT License. See the LICENSE file for details.

This README should give users a clear understanding of how to set up, run, and modify your Discord bot. Let me know if there are any specific details you'd like to include or adjust!





Make the example generic
ChatGPT
Here's an updated README with a more generic example for environment variables:

Discord Counter Bot
This bot tracks specific phrases in Discord messages, updates a SQLite database with counts for each phrase, and maps phrases to custom responses. It also handles aliases for names to track variations of a name as one entry.

Features
Phrase Tracking: Track occurrences of specific phrases in Discord messages.
Alias Handling: Map multiple aliases to a single canonical name.
Custom Responses: Define custom responses based on the tracked phrases.
Case-Insensitive Storage: Store names in a case-insensitive manner in the SQLite database.
Requirements
Python 3.7 or later
discord.py library
SQLite database
Docker (for running the bot in a container)
Setup
Environment Variables
Ensure the following environment variables are set:

DISCORD_TOKEN: Your Discord bot token.
PHRASE: A comma-separated list of phrases to track.
RESPONSE_MAPPINGS: A JSON string mapping phrases to custom response templates.
ALIASES: A JSON string mapping canonical names to lists of aliases.
Example
Here is an example of a .env file:

plaintext
Copy code
DISCORD_TOKEN=your_discord_bot_token
PHRASE="example phrase one,example phrase two"
RESPONSE_MAPPINGS={"example phrase one": "{capital_name} has done {phrase_count} example tasks.", "example phrase two": "{capital_name} has performed {phrase_count} example actions."}
ALIASES={"canonical_name": ["alias_one", "alias_two"], "another_name": ["another_alias"]}
Docker Compose Setup
Create a docker-compose.yml file with the following content:

yaml
Copy code
version: "3.8"
services:
  discordcounter:
    image: discordcoutingbot:latest
    volumes:
      - discordcounter:/config
    environment:
      - DISCORD_TOKEN=your_discord_bot_token
      - PHRASE="example phrase one,example phrase two"
      - RESPONSE_MAPPINGS={"example phrase one": "{capital_name} has done {phrase_count} example tasks.", "example phrase two": "{capital_name} has performed {phrase_count} example actions."}
      - ALIASES={"canonical_name": ["alias_one", "alias_two"], "another_name": ["another_alias"]}
    restart: unless-stopped
volumes:
  discordcounter:
Running the Bot
Build and run the Docker container:

sh
Copy code
docker-compose up --build
The bot will connect to Discord and start tracking phrases based on your configuration.

Development
Debugging
The bot includes detailed debugging output to help you understand its operation. Debug messages are printed to standard error.

Code Modifications
Database: The SQLite database is created with case-insensitive columns for names and phrases.
Response Formatting: Custom responses are formatted based on phrase mappings, with support for placeholders like {capital_name} and {phrase_count}.
Contributing
Feel free to fork this repository and submit pull requests. For any issues or feature requests, please open an issue on the repository.