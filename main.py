import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, TextGenerationPipeline

# Load environment variables from .env file
load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')


# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Load the Hugging Face model and tokenizer
model_name_or_path = "EleutherAI/gpt-neo-1.3B"
model = AutoModelForCausalLM.from_pretrained(model_name_or_path)
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)

# Initialize the Hugging Face Inference API
api_key = os.environ["HUGGINGFACE_API_KEY"]
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=-1,
    api_key=api_key
)

# Define the start command
def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm a chatbot powered by Hugging Face. How can I assist you?")

# Define the echo command
def echo(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    response = generator(text, max_length=100)[0]['generated_text']
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# Define the main function
def main() -> None:
    # Create the Telegram Updater and dispatcher
    updater = Updater(token=os.environ["TELEGRAM_BOT_TOKEN"], use_context=True)
    dispatcher = updater.dispatcher

    # Add the handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the bot
    updater.start_polling()

    # Run the bot until Ctrl-C is pressed
    updater.idle()

if __name__ == '__main__':
    main()
