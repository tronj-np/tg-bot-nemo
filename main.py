import api_token
import logging
from random import randint
from random import seed
import datetime
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import json_db

seed(api_token.seed)
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
    db.add_user(user_id=str(update.effective_user.id), points=100, user_type='user', daily_bonus=False, daily_bonus_time_penalty=datetime.datetime.now().hour+2)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower() == "!автор":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="@youalwayswereakiddersteve")
    elif update.message.text.split(' ')[0].lower() == "!рандом":
        try:
            randNumber = randint(int(update.message.text.split(' ')[1]), int(update.message.text.split(' ')[2]))
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите корректный диапазон чисел")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=randNumber)
        
    elif update.message.text.lower() == "!профиль":
        user_points = db.get_user_points(str(update.effective_user.id))
        user_type = db.get_user_type(str(update.effective_user.id))
        daily_bonus = db.get_user_profile(str(update.effective_user.id))["daily_bonus"]
        profile = f"Профиль:\nОчки:{user_points}\nВаш статус:{user_type}\nБонус:{daily_bonus}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=profile)

    elif update.message.text.lower() == "!бонус":
        bonus_penalty = int(db.get_bonus_penalty(str(update.effective_user.id)))
        daily_bonus = db.get_user_profile(str(update.effective_user.id))["daily_bonus"]
        bonus_amount = randint(100, 1000)
        if (abs((datetime.datetime.now().hour - bonus_penalty)) < 2):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Вы уже получали бонус")
        elif (abs((datetime.datetime.now().hour - bonus_penalty)) >= 2):
            db.set_bonus_penalty(str(update.effective_user.id), datetime.datetime.now().hour)
            db.set_bonus_status(str(update.effective_user.id), True)
            db.add_points(str(update.effective_user.id), bonus_amount)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Бонус получен в размере {bonus_amount}!")
    elif update.message.text.split(' ')[0].lower() == "!трансфер":
        try:
            receiver_point_id = str(update.message.reply_to_message.from_user.id)
            point_amount = int(update.message.text.split(' ')[1])
            try:
                user_points = db.get_user_points(str(update.effective_user.id))
            except:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Данного пользователя не существует в базе данных!\nНапишите /start для создания профиля!") 
            if (user_points < point_amount):
                await context.bot.send_message(chat_id=update.effective_chat.id, text="У вас недостаточно очков!")
            elif (point_amount < 1):
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите корректную сумму")
            else:
                db.add_points(receiver_point_id, point_amount)
                db.remove_points(str(update.effective_user.id), -point_amount)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Переведено {point_amount} очков, пользователю @{update.message.reply_to_message.from_user.username}!")
                await context.bot.send_message(chat_id=receiver_point_id, text=f"Получено {point_amount} очков, от пользователя @{update.effective_user.username}!")
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Ответьте на сообщение человека, которому вы хотите перевести очки.")
    elif update.message.text.split(' ')[0].lower() == "!кости":
        try:
            user_points = db.get_user_points(str(update.effective_user.id))
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
                mid_arm = (dice_sum + user_sum) / 2
                print(f"Dice log: Dice sum - Mid arm = {dice_sum - mid_arm}")
                if (dice_sum - mid_arm) > 0.5:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Вы проиграли!\nВыпало:{dice1}+{dice2}={dice_sum}\nВаша сумма:{user_sum}")
                    db.remove_points(str(update.effective_user.id), user_bid)
                elif (dice_sum - mid_arm) < 0:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Вы ПРОЕБАЛИ!\nВыпало:{dice1}+{dice2}={dice_sum}\nВаша сумма:{user_sum}")
                    db.remove_points(str(update.effective_user.id), user_bid*10)
                elif dice_sum == mid_arm:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"ДЖЕКПОТ!\nВыпало:{dice1}+{dice2}={dice_sum}\nВаша сумма:{user_sum}")
                    db.add_points(str(update.effective_user.id), user_bid*10)
                elif (dice_sum - mid_arm) <= 0.5:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Вы выиграли!\nВыпало:{dice1}+{dice2}={dice_sum}\nВаша сумма:{user_sum}")
                    db.add_points(str(update.effective_user.id), user_bid*2)
               
        except:
            pass

    elif update.message.text.split(' ')[0].lower() == "!setadmin":
        user_type = db.get_user_type(user_id=str(update.effective_user.id))
        try:
            replied_user_id = str(update.message.reply_to_message.from_user.id)
        except:
            replied_user_id = str(update.message.text.split(' ')[1])
        if user_type == "owner-user":
            db.set_user_type(user_id=replied_user_id, user_type="admin-user")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="CODE 0 OK")
        elif user_type != "owner-user":
            await context.bot.send_message(chat_id=update.effective_chat.id, text="CODE 1 ERROR\nUSER DOESN'T HAVE ENOUGH RIGHTS")
        elif update.message.text.split(' ')[1] == "":
            await context.bot.send_message(chat_id=update.effective_chat.id, text="CODE 1 ERROR\nEMPTY USER ID")

    elif update.message.text.split(' ')[0].lower() == "!getprofile":
        user_type = db.get_user_type(user_id=str(update.effective_user.id))
        try:
            replied_user_id = str(update.message.reply_to_message.from_user.id)
        except:
            replied_user_id = str(update.message.text.split(' ')[1])
        if user_type == "owner-user":
            user_points = db.get_user_points(replied_user_id)
            user_type = db.get_user_type(replied_user_id)
            daily_bonus = db.get_user_profile(replied_user_id)["daily_bonus"]
            profile = f"Профиль пользователя [@{update.message.reply_to_message.from_user.username}]:\nОчки:{user_points}\nВаш статус:{user_type}\nБонус:{daily_bonus}"
            await context.bot.send_message(chat_id=update.effective_chat.id, text="CODE 0 OK")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=profile)
        elif user_type != "owner-user":
            await context.bot.send_message(chat_id=update.effective_chat.id, text="CODE 1 ERROR\nUSER DOESN'T HAVE ENOUGH RIGHTS")
        elif replied_user_id == None or "":
            await context.bot.send_message(chat_id=update.effective_chat.id, text="CODE 1 ERROR\nEMPTY USER ID")

    elif update.message.text.split(' ')[0].lower() == "!setuser":
        user_type = db.get_user_type(user_id=str(update.effective_user.id))
        try:
            replied_user_id = str(update.message.reply_to_message.from_user.id)
        except:
            replied_user_id = str(update.message.text.split(' ')[1])
        if user_type == "owner-user":
            db.set_user_type(user_id=replied_user_id, user_type="user")
            await context.bot.send_message(chat_id=update.effective_chat.id, text="CODE 0 OK")
        elif user_type != "owner-user":
            await context.bot.send_message(chat_id=update.effective_chat.id, text="CODE 1 ERROR\nUSER DOESN'T HAVE ENOUGH RIGHTS")
        elif update.message.text.split(' ')[1] == "":
            await context.bot.send_message(chat_id=update.effective_chat.id, text="CODE 1 ERROR\nEMPTY USER ID")

    elif update.message.text.split(' ')[0].lower() == "!setseed":
        user_type = db.get_user_type(user_id=str(update.effective_user.id))
        if len(update.message.text) == 8:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="CODE 1 ERROR\nEMPTY SEED")
        elif len(update.message.text.split(' ')[1]) < 10:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="CODE 1 ERROR\nSEED TOO SHORT")
        elif user_type != "owner-user":
            await context.bot.send_message(chat_id=update.effective_chat.id, text="CODE 1 ERROR\nUSER DOESN'T HAVE ENOUGH RIGHTS")
        else:
            seed(str(update.message.text.split(' ')[1]))
            await context.bot.send_message(chat_id=update.effective_chat.id, text="CODE 0 OK")
    
if __name__ == '__main__':
    application = ApplicationBuilder().token(api_token.apitoken).build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)
    
    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()