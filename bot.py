import telebot
import sqlite3

from config import token
from football import gen_player

# new bot instance
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(m):
    try:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
        user_markup.row('⚽ Soccer', 'ℹ️ Help')

        db = sqlite3.connect("footballDB.sqlite")
        cursor = db.cursor()

        # Print SQLite version
        print("You are connected to - SQLite v", sqlite3.version, "\n")

        # Create Users Table
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id SERIAL, userId VARCHAR NOT NULL);')
        db.commit()
        print("Table created successfully in SQLite! ")

        from_user = [m.from_user.id]
        cursor.execute('SELECT EXISTS(SELECT userId FROM users WHERE userId = ?)', from_user)
        check = cursor.fetchone()

        if not check[0]:
            cursor.execute('INSERT INTO users (userId) VALUES (?)', from_user)
            db.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into users table")
        else:
            count = cursor.rowcount
            print(count, "Record already exists")

        start_msg = 'Hey *{}* 👋, I\'m *FootGuessr Bot* 🤖!\n\n' \
                    'With my help you can play the game to guess 🤔 the player\'s name from their statistics.\n\n' \
                    'Also you can see:\n\t\t\t- results of football events ⚽' \
                    '\n\t\t\t- statistics of different leagues 📈' \
                    '\n\t\t\t- statistics of players 🏃🏽‍♀️\n\n' \
                    'Player data is taken from [Wiki](https://en.wikipedia.org/wiki/Main_Page).\n' \
                    'Football stats from [Livescores](livescores.com).\n\n' \
                    'Press any button below to interact with me 😀\n\n' \
                    'Made with ❤️ by *@jackshen* & *@rudek0*'

        bot.send_message(m.chat.id, start_msg.format(m.from_user.first_name), reply_markup=user_markup,
                         parse_mode="Markdown", disable_web_page_preview="True")

    except Exception as error:
        print("Error occurred", error)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == '+':
        bot.send_message(message.chat.id, 'Try to guess the player, according to his career')
        text = "```" + str(gen_player()) + "```"
        bot.send_message(message.chat.id, text, parse_mode="MarkdownV2")


bot.polling()