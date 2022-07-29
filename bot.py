'''
Программа создания бота
'''
import os
import telebot # импортируем бота из PyTelegramBotApy (синхронная библиотека)
from dotenv import load_dotenv
import pprint
from parser import parse_news

load_dotenv()               #token для ТГ-бота храним в виртуальном окружении
token = os.getenv('TOKEN')
print(f'Token: {token}')

bot = telebot.TeleBot(token)

# С помощью декоратора регистриуем функцию 'send_welcome' в качестве обработчика ('handler')
# commands=['help', 'start'] - показывает на что будет реагировать данный обработчик:
# (декоратор определяет фильтры для сообщений:
# сообщение обрабатывается ПЕРВЫМ обработчиком через фильтр которого прошло)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):                          # message - сообщение, которое передает нам ТГ-бот
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")

@bot.message_handler(commands=['pars'])
def start_parser(message):
    bot.reply_to(message, 'Парсер Новостей с сайта https://www.све.рф')
    bot.send_message(message.chat.id, "Let's begin..." )
    last_news = parse_news()
    print(f'Количество новостей: {len(last_news)}')
    for item_news in last_news:
        s1 = item_news['Number']
        s2 = item_news['Data']
        s3 = item_news['Heading']
        s4 = item_news['Text']
        s5 = item_news['Link']
        bot_news = f'{s1}. \n {s2}\n {s3}\n {s4}\n {s5}'
        bot.send_message(message.chat.id, bot_news)
        #print(item_news)
        #print(item_news['Number'], item_news['Heading'], item_news['Text'], item_news['Link'])


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda m: True)
def echo_message(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()

