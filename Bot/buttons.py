from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def languages():
    markup = InlineKeyboardMarkup()

    btn = InlineKeyboardButton("🇺🇿 Uzbekistan", callback_data="uz")
    markup.add(btn)

    markup.row_width = 2
    markup.add(InlineKeyboardButton("🇬🇧 English", callback_data="en"),
               InlineKeyboardButton("🇷🇺 Russian", callback_data="ru"),
               InlineKeyboardButton("🇫🇷 French", callback_data="fr"),
               InlineKeyboardButton("🇩🇪 German", callback_data="de"),
               InlineKeyboardButton("🇸🇦 Arabic", callback_data="ar"),
               InlineKeyboardButton("🇮🇳 Hindi", callback_data="hi"))

    return markup


def settings():
    markup = InlineKeyboardMarkup()

    btn2 = InlineKeyboardButton("⚙️ Change language", callback_data='settings')
    markup.add(btn2)

    return markup


def result():
    markup = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton("🎧 Pronunciation", callback_data='pronunciation')
    btn2 = InlineKeyboardButton("⚙️ Settings", callback_data='settings')
    btn = InlineKeyboardButton(" ❌ ", callback_data='delete')
    markup.add(btn1, btn2)
    markup.add(btn)

    return markup


def delete():
    markup = InlineKeyboardMarkup()

    btn = InlineKeyboardButton(" ❌ ", callback_data='delete')
    markup.add(btn)

    return markup


def repo():
    markup = InlineKeyboardMarkup()

    btn = InlineKeyboardButton("Github Repo", url='https://github.com/coder2077/iTranslator-bot')
    btn1 = InlineKeyboardButton(" ❌ ", callback_data='delete')
    markup.add(btn)
    markup.add(btn1)

    return markup


# Handling /start command
@bot.message_handler(commands=['start'])
def start_command(message):
    firstname = message.from_user.first_name
    username = message.from_user.username
    chat_id = message.chat.id

    answer = f'🔥 *Welcome {firstname} !*\n\n⚙️ _Select language and send me text_\n\n🆘 *Available commands: /help*'
    lang = bot.send_message(chat_id, answer, reply_markup=languages())

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (chat_id,))
    data = cursor.fetchone()
    if data is None:
        cursor.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?);", (firstname, username, chat_id, 'None', 'None'))
    else:
        pass

    conn.commit()
    conn.close()


# Handling /statistics command
@bot.message_handler(commands=['statistics'])
def stat_command(message):
    first_name = message.from_user.first_name
    chat_id = message.chat.id

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    num = cur.execute("SELECT COUNT(*) FROM users")
    for n in num:
        for i in n:
            msg_text = f'<b><i>Number of users</i> - {i}</b>'

    conn.close()

    bot.send_message(chat_id, msg_text, parse_mode='html', reply_markup=delete())
