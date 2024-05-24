import api_token
import logging
from random import randint
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import json_db

db = json_db.DatabaseInteraction()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="!автор - профиль автора\n!рандом [от] [до] - случайное число в выбранном диапазоне\n/start - вывод этого сообщения\n!профиль - профиль пользователя\n!кости [ставка] [сумма 2 выпавших костей]"
    )
    db.add_user(user_id=str(update.effective_chat.id), points=0, user_type='user')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "!автор":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="@youalwayswereakiddersteve")
    elif update.message.text.split(' ')[0] == "!рандом":
        try:
            randNumber = randint(int(update.message.text.split(' ')[1]), int(update.message.text.split(' ')[2]))
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите корректный диапазон чисел")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=randNumber)
    elif update.message.text == "!профиль":
        user_points = db.get_user_points(str(update.effective_chat.id))
        user_type = db.get_user_type(str(update.effective_chat.id))
        profile = f"Профиль:\nОчки:{user_points}\nВаш статус:{user_type}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=profile)
    elif update.message.text.split(' ')[0] == "!кости":
        try:
            user_points = db.get_user_points(str(update.effective_chat.id))
            user_type = db.get_user_type(str(update.effective_chat.id))
            user_bid = int(update.message.text.split(' ')[1])
            user_sum = int(update.message.text.split(' ')[2])
            if ((user_sum > 12) or (user_sum == 1)):
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите корректную сумму")
            elif (user_bid > user_points):
                await context.bot.send_message(chat_id=update.effective_chat.id, text="У вас недостаточно очков")
            elif (user_bid < 1):
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите корректную ставку")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ваша ставка:{user_bid}\nВаша сумма:{user_sum}")
                dice1 = randint(1, 6)
                dice2 = randint(1, 6)
                dice_sum = dice1 + dice2
                if user_sum > dice_sum:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Вы проиграли!\nВыпало:\n{dice1}\n{dice2}\nСумма:{dice_sum}")
                    db.remove_points(str(update.effective_chat.id), user_bid*3)
                elif user_sum < dice_sum:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Вы выиграли!\nВыпало:\n{dice1}\n{dice2}\nСумма:{dice_sum}")
                    db.add_points(str(update.effective_chat.id), user_bid*2)
                elif user_sum == dice_sum:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"ДЖЕКПОТ!\nВыпало:\n{dice1}\n{dice2}\nСумма:{dice_sum}")
                    db.add_points(str(update.effective_chat.id), user_bid*10)
        except:
            pass

    
if __name__ == '__main__':
    application = ApplicationBuilder().token(api_token.apitoken).build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)
    
    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()