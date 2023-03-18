import os
from dotenv import load_dotenv
import requests 
import telegram 
import telegram.ext
from telegram import Update

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
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    updater = telegram.ext.Updater(bot.token)
    # Register handlers for different commands and messages
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, generate_text))
    # Start polling for updates from Telegram
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
