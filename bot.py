from discord.ext import commands
from discord import Intents, Message
from openai_functions import generate_text
import asyncio
import random
import json

# command handling ----------------------------------
class ErrorHandler(commands.Cog):
    """
    A cog for global error handling.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """
        This function handles all the unexpected errors.
        """
        if isinstance(error, commands.CommandNotFound):
            return  # Return because we don't want to show an error for every command not found
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = "You are missing the required permissions to run this command!"
        elif isinstance(error, commands.UserInputError):
            message = "Something about your input was wrong, please check your input and try again!"
        else:
            print(error)
            message = "Oh no! Something went wrong while running the command!"

        await ctx.send(message, delete_after=5)

def create_bot():
    """
    Setup the bot
    @returns: The discord bot
    """

    bot = commands.Bot(
    command_prefix='$',
    intents = Intents.default()
    )

    bot.add_cog(ErrorHandler(bot))

    return bot

class DiscordBot():
    """
    This class is the discord bot.
    """
    bot = create_bot()
    running = False
    story_telling = {}
    
    def __init__(self, token):
        # Return if the bot is already running
        if DiscordBot.running:
            return
        
        # From here only static vars
        with open('configuration.json', 'r+') as json_file:
            settings = json.load(json_file)            
            DiscordBot.message_timeout = settings.get("message_timeout", 60)
            DiscordBot.typing_time_min = settings.get("typing_time_min", 0)
            DiscordBot.typing_time_max = settings.get("typing_time_max", 0)
            DiscordBot.prompt_start = settings.get("prompt start", "Tell a story containing the following information")
            DiscordBot.start_messages = settings.get("start", ["Start story"])
            DiscordBot.error_message = settings.get("error", ["Error"])
            DiscordBot.trigger_words = settings.get("trigger_words", {})
            DiscordBot.blacklist = settings.get("blacklist", [])
            DiscordBot.questions = settings.get("questions", {})
            DiscordBot.chat_bot_role = settings.get("chat_bot_role", "Story teller")

        DiscordBot.running = True
        self.bot.run(token)

    # bot funcions--------------------------------------------
    @bot.event
    async def on_ready():
        """
        This function triggers when the bot is started.
        """
        print('Logged in as:')
        print(DiscordBot.bot.user.name)

    @bot.event
    async def on_message(message):
        # Return if message is from the bot itself to prevent the bot talking to itself
        # Also return if the user is engaged in story creation
        if message.author == DiscordBot.bot.user or DiscordBot.story_telling.get(message.author.id):
            return  

        # Responses to messages are defined here
        content = str(message.content).lower()

        await DiscordBot.process_trigger_words(message)    

        if content.__contains__('story'): 
            await DiscordBot.process_story(message)

        # Check for aditional commands
        await DiscordBot.bot.process_commands(message)

    @staticmethod
    async def reply(message: Message, response: str):
        """
        Make the bot respond to a message. The message is send with a random delay to make the bot feel more natural.
        """
        async with message.channel.typing():
            timeout = random.uniform(DiscordBot.typing_time_min, DiscordBot.typing_time_max)
            await asyncio.sleep(timeout)
            await message.channel.send(response) 

    @staticmethod
    async def process_trigger_words(message: Message):
        """
        This function looks for cerain trigger words in the user messages. When a trigger word is found, an appropriate response is send.
        """
        for trigger_word, responses in DiscordBot.trigger_words.items():
            # If no trigger word is found in the message, continue to the next trigger word
            if not str(message.content).lower().__contains__(trigger_word):
                continue
                
            # When a trigger word is found, give an appropriate response
            await DiscordBot.reply(message=message, response=random.choice(responses))

    @staticmethod
    async def process_story(message: Message):
        """
        This function defines the flow of the story
        """
        DiscordBot.story_telling[message.author.id] = True
        def check(m: Message):
            # Checks if the response comes from the right person
            return m.author.id == message.author.id and m.channel.id == message.channel.id 
        
        story_promt = {}
        
        try:
            # Randomise the order of the topics so the conversation does not feel as scripted
            topics = list(DiscordBot.questions.items())
            random.shuffle(topics)

            for parameter, questions in topics:
                await DiscordBot.reply(message=message, response=random.choice(questions))

                # Store the awnser to the question
                msg = await DiscordBot.bot.wait_for("message", check=check, timeout=DiscordBot.message_timeout)
                story_promt[parameter] = msg.content.replace(DiscordBot.bot.user.mention, '', 1)

        finally:
            # Send message that the prompt is loading
            start_message = random.choice(DiscordBot.start_messages)
            await DiscordBot.reply(message=message, response=start_message)

            try:
                # Generate story
                async with message.channel.typing():
                    # Combine the gathered parameters to prompt for opengbt
                    prompt = f"{DiscordBot.prompt_start}:{story_promt}"
                    story = generate_text(
                        prompt=prompt, 
                        role=DiscordBot.chat_bot_role, 
                        blacklist=DiscordBot.blacklist)
                    
                    await message.channel.send(story)
            except:
                # Send a message that the prompt failed to generate
                error_message = random.choice(DiscordBot.error_message)
                await DiscordBot.reply(message=message, response=error_message)
                await message.channel.send(error_message)
            finally:
                DiscordBot.story_telling[message.author.id] = False
