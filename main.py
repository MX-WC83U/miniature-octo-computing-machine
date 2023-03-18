


import os
import logging
from dotenv import find_dotenv, load_dotenv
import telegram 
import telegram.ext
#from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

load_dotenv(find_dotenv())

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')
MODEL_NAME_OR_PATH = "EleutherAI/gpt-neo-1.3B"
MODEL_NAME_OR_OATH = "t5-small"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME_OR_PATH)
    generator = pipeline("text-generation", model=MODEL_NAME_OR_PATH, tokenizer=MODEL_NAME_OR_PATH, device="cpu", api_key=HUGGINGFACE_API_KEY)
except Exception as e:
    logging.error(f"Failed to load Hugging Face model: {e}")
    exit(1)

def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm a chatbot powered by Hugging Face. How can I assist you?")

def echo(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    response = generator(text, max_length=100)[0]['generated_text']
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def main() -> None:
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


