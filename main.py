from bot import DiscordBot
from discord import LoginFailure
from utilities import get_token

# Main entry point for the bot.
if __name__ == '__main__':
    DISCORD_TOKEN = get_token("DISCORD_TOKEN")
    if DISCORD_TOKEN is None:
        print("Please make sure that the token is stored in the right place.")
        exit(-1)

    # Start the bot.
    try:
        DiscordBot(DISCORD_TOKEN)
    except LoginFailure:
        print("Improper token has been passed.")
        exit(-1)
    finally:
        exit(0)
