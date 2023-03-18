import os
import telegram
import telegram.ext
import asyncio
import aiohttp
from telegram import Update
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# Set the Hugging Face API endpoint and model ID
HF_API_ENDPOINT = 'https://api-inference.huggingface.co/models/gpt2-xl'

# Get your Telegram bot token and Hugging Face API key from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
HF_API_KEY = os.getenv('HF_API_KEY')

async def start(update: Update, context: telegram.ext.CallbackContext) -> None:
    await update.message.reply_text('Hello! I am a bot that uses the Hugging Face Inference API to generate text. Send me a message to get started.')

async def generate_text(update: Update, context: telegram.ext.CallbackContext) -> None:
    # Get the user's message
    user_message = update.message.text

    # Use the Hugging Face Inference API to generate text based on the user's message
    headers = {'Authorization': f'Bearer {HF_API_KEY}'}
    data = {'inputs': user_message}

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(HF_API_ENDPOINT, json=data) as response:
                if response.status == 200:
                    response_data = await response.json()
                    generated_text = response_data[0]['generated_text']

                    # Send the generated text back to the user
                    await update.message.reply_text(generated_text)
                else:
                    error_message = f'An error occurred while generating text: {response.text}'
                    await update.message.reply_text(error_message)
    except Exception as e:
        error_message = f'An error occurred while generating text: {e}'
        await update.message.reply_text(error_message)

async def main() -> None:
    # Create a Telegram bot object
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

    # Create an Updater object
    updater = telegram.ext.Updater(bot.token, use_context=True)

    # Register handlers for different commands and messages
    updater.dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
    updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command, generate_text))

    # Start polling for updates from Telegram
    await updater.start_polling()
    await updater.idle()

if __name__ == '__main__':
    # Start the main function
    asyncio.run(main())
