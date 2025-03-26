import os
import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Load environment variables
TELEGRAM_TOKEN = os.getenv("8062159434:AAFVrcYQDUSEOOq4Yn8e_t2v2PvhNjOpiaY")
HUGGINGFACE_API_KEY = os.getenv("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")

# Allowed models
ALLOWED_MODELS = {
    "gpt2": "gpt2",
    "mistral": "mistralai/Mistral-7B-Instruct",
    "bigcode": "bigcode/starcoder"
}

# Default model
current_model = ALLOWED_MODELS["mistral"]

# Function to call Hugging Face API
def get_ai_response(user_input):
    global current_model
    url = f"https://api-inference.huggingface.co/models/{current_model}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": user_input}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]['generated_text']
    else:
        return f"⚠️ Error: Unable to process request for model `{current_model}`."

# Start Command
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🤖 **AI Chatbot Powered by Hugging Face**\n"
        "I support these models:\n"
        "🟢 `gpt2` - Small OpenAI model\n"
        "🟢 `mistral` - Large conversational AI\n"
        "🟢 `bigcode` - AI for coding\n\n"
        "Use `/model <name>` to switch models.\n"
        "Example: `/model gpt2`"
    )

# Change Model Command
def change_model(update: Update, context: CallbackContext):
    global current_model
    if len(context.args) == 0:
        update.message.reply_text("⚠️ Usage: `/model <name>`\nExample: `/model mistral`")
        return

    new_model = context.args[0].lower()
    if new_model in ALLOWED_MODELS:
        current_model = ALLOWED_MODELS[new_model]
        update.message.reply_text(f"✅ AI model changed to `{new_model}`")
    else:
        update.message.reply_text("⚠️ Invalid model. Use `/model gpt2`, `/model mistral`, or `/model bigcode`.")

# Message Handler
def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text
    bot_reply = get_ai_response(user_text)
    update.message.reply_text(bot_reply)

# Main Function
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("model", change_model))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
