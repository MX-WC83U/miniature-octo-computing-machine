import os
import logging
from dotenv import load_dotenv
import requests 
import telegram 
import telegram.ext
from telegram import Update

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Set the Hugging Face API endpoint and model ID
HF_API_ENDPOINT = 'https://api-inference.huggingface.co/models/gpt2-xl'

# Get your Telegram bot token and Hugging Face API key from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
HF_API_KEY = os.getenv('HF_API_KEY')

def start(update: Update, context: telegram.ext.CallbackContext) -> None:
    """Handler for /start command"""
    update.message.reply_text('Hello! I am a bot that uses the Hugging Face Inference API to generate text. Send me a message to get started.')

def generate_text(update: Update, context: telegram.ext.CallbackContext) -> None:
    """Handler for generating text based on user input"""
    # Get the user's message
    user_message = update.message.text

    # Validate user input
    if not user_message:
        update.message.reply_text('Please provide a message.')
        return
    if len(user_message) > 1024:
        update.message.reply_text('Your message is too long. Please provide a shorter message.')
        return

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
        logger.error(error_message)

def main() -> None:
    """Main function to start the bot"""
    # Create an Updater object with your bot's token
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    updater = telegram.ext.Updater(bot.token, use_context=True)

    # Register handlers for different commands and messages
    updater.dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
    updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command, generate_text))

    # Start polling for updates from Telegram
    updater.start_polling()
    logger.info('Bot started. Press Ctrl-C to stop.')
    updater.idle()

if __name__ == '__main__':
    main()
