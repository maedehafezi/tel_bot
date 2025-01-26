from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

API_TOKEN = 'API_TOKEN'

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! I am your AI Assistant.")

async def echo(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    await update.message.reply_text(f"You said: {user_message}")

def main():
    app = Application.builder().token(API_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling()

if __name__ == "__main__":
    main()
