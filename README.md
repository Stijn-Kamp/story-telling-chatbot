# Story telling chatbot
Introducing our new story telling Discord chatbot - the perfect companion for children's bedtime stories! Our chatbot is designed to generate personalized stories for kids based on their interests and preferences.
With our storytelling chatbot, children can enjoy endless hours of entertainment and learning. Say goodbye to boring bedtime stories and hello to a world of imagination and adventure!

## Usage
The bot will start the creation of the stories when a user pings a the bot with a message containing the word story. The bot can be pinged with the '@' sign followed by the bots name in the server.
```
[@ChatBot] Could you please tell me a story.
```
When the story telling is initiated, the bot will ask a couple of questions to the user. These questions will be deciding how the story will play out. They can be awnsered by pinging the bot followed by the awnser. The questions can only be awnsered by the user who initiated the story creation. 
```
What should the story be about?
[@ChatBot] The story should be about a group of students, giving their A-game for a school project.
```
The Intents of the bot are set to Default by default. This means the bot only listens to awnsers where the bot is pinged. This way the bot only has access to the messages the users want the bot to have acces to.

## Configuration
The configuration of the chatbot is stored in `configuration.json`
| Setting | Description |
| ------ | ------ |
| message_timeout | Maximum time the chatbot should wait  for an awnser when asking a question |
| typing_time_min | The minimum amount the chatbot should display typing before sending a message |
| typing_time_max | The maximum amount the chatbot should display typing before sending a message |
| chat_bot_role | The personality of the chatbot |
| prompt_start | Start of the prompt message, this is followed by the promt of the user |
| start | List of sentences the chatbot can say before generating the story |
| error | List of sentencesthe chatbot can say when failing to generate the story |
| blacklist | List of words and sentances the chatbot should not mention |
| questions | List of parameters and questions the chatbot asks before generating a story |
| trigger_words | List of trigger words and responses to messages containing those words |

### Questions
Before generating a story, the chatbot will ask a couple of questions. The awnsers of which will be incorperated in the story. Each question contains a parameter and a list of sentences. 
```json
    "questions" : {
        "Main person": [
            "Who is the main person of the story?",
            "Could you elaberate who the main person of the story is?",
            "Tell me, who should be the main person?"
        ]
    }
```
### Triggers
Triggers work much like questions. The trigger words consists of a list of words and appropriate responses to messages containing those words.
```json
    "trigger words": {
        "wisdom": [
            "Treat others the way you want to be treated.",
            "Always be honest, even when it's hard."
        ],
    }
```

### Blacklist
The chatbot features a blacklist in the `configuration.json`. This is a list of all the topics the chatbot should not talk about. The user can add words or whole sentances to the list that should not be named in the stories. When the chatbot encounters one of the blacklisted items, it will stop generating the story and instead send one of the error sentances.
```json
    "blacklist": [
        "blood"
    ]
```

## Installation
### Creating the discord bot
1. Turn on “Developer mode” in your Discord account.
3. In the [Developer portal](https://discord.com/developers/applications) , click on “Applications”. 
4. Click on “New Application”.
5. Name the bot and then click “Create”.
6. Go to the “Bot” menu and generate a token using “Add Bot”.
7. Click on “OAuth2”, select "in-app authorisation" for "Authorization Method". Choose "bot" and select all the text permisions.
8. Go to "url-generator" under "OAuth2", activate “bot”, set the only the text permisions, and then click on “Copy”.
8. Enter the link in the url-bar and select your server to add your bot to it.

### Running the project
1. Install python version 3.11.2 from https://www.python.org/downloads/
2. Clone the repo
   ```sh
   https://gitlab.utwente.nl/s2690497/story-telling-bot
   ```
3. Go to the project root
    ```sh
   cd story-telling-robot
   ```
4. Install python libraries
   ```sh
   pip3 install -r requirements
   ```
5. Get the opengbt key from https://beta.openai.com/account/api-keys
6. Get the Discord key from https://discord.com/developers/applications/
7. Create a file called `.env` and add your API keys
   ```env
    DISCORD_TOKEN = "ENTER YOUR API"
    OPENGPT_TOKEN = "ENTER YOUR API"
   ```
8. Run the project
    ```sh
    python3 main.py
    ```
