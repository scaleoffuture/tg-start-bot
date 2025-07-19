from telegram import Update, ReplyKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,  MessageHandler, filters
from asyncio import sleep

user_names = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📛 Моё имя", "🆘 Помощь", "✨ Команды"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Я твой первый Telegram-бот 🤖",
    reply_markup=reply_markup)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я готов помочь с чем угодно! Только скажи 👩‍💻")


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я - первый Telegram-бот независимого создателя Scaleoffuture.\n"
        "Вместе мы создаем ценность для всего окружения.\n"
        "Те, кто выбирают нас, получают самый качественный продукт во всех рынках.\n"
        "Даже если таковых нет.\n"
        "Я не просто Telegram-бот, я - твой ассистент, который готов выдавать максимум из своей работы.\n"
        "Мы всегда будем стремиться к качеству, свободе и пользе для всего мира."
    )

    
async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Наши команды: /start, /help, /about, /myname, /timer и /commands")


async def save_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    name = update.message.text
    user_names[user_id] = name
    await update.message.reply_text(f"Приятно познакомиться, {name}! 😊")


#async def my_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #user_id = update.message.from_user.id
    #name = user_names.get(user_id)
    #if name:
        #await update.message.reply_text(f"Твоё имя — {name}!")
    #else:
        #await update.message.reply_text("Я ещё не знаю твоё имя. Напиши его!")


async def my_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        name = ' '.join(context.args)
        context.user_data['name'] = name
        await update.message.reply_text(f"Отлично, {name}, я запомнил твоё имя!")
    else:
        name = context.user_data.get('name')
        if name:
            await update.message.reply_text(f"Твоё имя — {name}.")
        else:
            await update.message.reply_text("Я пока не знаю твоё имя. Напиши его после команды, например: /myname Vlad")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📛 Моё имя":
        await my_name(update, context)
    elif text == "🆘 Помощь":
        await help(update, context)
    elif text == "✨ Команды":
        await commands(update,context)
    #else:
        #context.user_data["name"] = text
        #await update.message.reply_text(f"Приятно познакомиться, {text}! 😊")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отличное фото! 👌")


async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напомню через 18 секунд!")
    await sleep(18)
    await update.message.reply_text("⌛ Напоминаю!")


app = ApplicationBuilder().token("YOUR TOKEN").build()

# commands of the bot
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("about", about))
app.add_handler(CommandHandler("commands", commands))
app.add_handler(CommandHandler("myname", my_name))
app.add_handler(CommandHandler("timer", remind))

# 
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.run_polling()
print('Our bot is ready⚡')
