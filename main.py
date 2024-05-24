import api_token
import logging
from random import randint
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="!автор - профиль автора\n!рандом 0 100 - случайное число в выбранном диапазоне\n/start - вывод этого сообщения"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "!автор":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="@youalwayswereakiddersteve")
    elif update.message.text.split(' ')[0] == "!рандом":
        await context.bot.send_message(chat_id=update.effective_chat.id, text=randint(int(update.message.text.split(' ')[1]), int(update.message.text.split(' ')[2])))

    
if __name__ == '__main__':
    application = ApplicationBuilder().token(api_token.apitoken).build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)
    
    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()