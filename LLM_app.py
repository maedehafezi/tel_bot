import torch
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
API_TOKEN = 'API_TOKEN'
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! I am your AI Assistant.")
async def chat(update: Update, context: CallbackContext) -> None:
    try:
        user_message = update.message.text
        prompt = f"You are a knowledgeable assistant. Answer the user's question in detail.\nUser: {user_message}\nAssistant: "
        inputs = tokenizer.encode(prompt, return_tensors="pt").to(device)
        outputs = model.generate(
            inputs,
            max_length=100,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response.replace(prompt, "").strip()
        limited_response = " ".join(response.split()[:60])
        if not limited_response.endswith(('.', '!', '?')):
            limited_response = limited_response.rsplit('.', 1)[0] + "."
        await update.message.reply_text(limited_response)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Oops! Something went wrong.")
def main():
    app = Application.builder().token(API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()
if __name__ == "__main__":
    main()
