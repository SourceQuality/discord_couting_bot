# Basic Discord Vulgar Phrase counter
This is just a small discord bot that is used to count how many times a person has been ******

This bot will count how many times a phrase has been said, and will repeat it back into the chat.

Usage:

Docker run command:

```
docker run -d \
    -e DISCORD_TOKEN= "Your discord bot token" \
    -e PHRASE="comma, seperated, list" \
    -v /path/to/config:config \
ghcr.io/sourcequality/discord_couting_bot:latest
```

Docker compose:

```
discordcounter:
    image: 
```
