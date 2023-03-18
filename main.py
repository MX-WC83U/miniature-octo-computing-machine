#Here's an updated version of the code that reads the Telegram bot token and Hugging Face API key from a `.env` file:



import os

from dotenv import load_dotenv

import requests 
import telegram 
import telegram.ext

from telegram import Update

#from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Load environment variables from .env file

load_dotenv()

# Set the Hugging Face API endpoint and model ID

HF_API_ENDPOINT = 'https://api-inference.huggingface.co/models/gpt2-xl'

# Get your Telegram bot token and Hugging Face API key from environment variables

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

HF_API_KEY = os.getenv('HF_API_KEY')

def start(update: Update, context):

    update.message.reply_text('Hello! I am a bot that uses the Hugging Face Inference API to generate text. Send me a message to get started.')

def generate_text(update: Update, context):

    # Get the user's message

    user_message = update.message.text

    # Use the Hugging Face Inference API to generate text based on the user's message

    headers = {'Authorization': f'Bearer {HF_API_KEY}'}

    data = {'inputs': user_message}

    response = requests.post(HF_API_ENDPOINT, headers=headers, json=data)

    if response.status_code == 200:

        generated_text = response.json()[0]['generated_text']

        # Send the generated text back to the user

        update.message.reply_text(generated_text)

    else:

        # Handle errors from the Hugging Face Inference API

        error_message = f'An error occurred while generating text: {response.text}'

        update.message.reply_text(error_message)

def main():

    # Create an Updater object with your bot's token

   # updater = Updater(TELEGRAM_BOT_TOKEN)
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

    updater = telegram.ext.Updater(bot.token, use_context=True)
    # Register handlers for different commands and messages

    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, generate_text))

    # Start polling for updates from Telegram

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':

    main()


"""
In this updated version of the code, we've added a call to `load_dotenv()` at the beginning of the script. This function reads environment variables from a `.env` file in the same directory as your script.

To use this code with your own Telegram bot and Hugging Face account:

1. Create a `.env` file in the same directory as your script.

2. Add your Telegram bot token and Hugging Face API key to this file using the following format:

```

TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE

HF_API_KEY=YOUR_HF_API_KEY_HERE

```

3. Replace `YOUR_TELEGRAM_BOT_TOKEN_HERE` and `YOUR_HF_API_KEY_HERE` with your own values.

4. Install the required dependencies by running `pip install python-telegram-bot requests python-dotenv`.

5. Run the script using `python script_name.py`.

After completing these steps and running the script, your Telegram bot should be able to read its token and your Hugging Face API key from a `.env` file.

"""
