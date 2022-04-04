import telebot
from settings import TOKEN
import re

bot = telebot.TeleBot(TOKEN)

def get_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/fortune','/btc','/plus')
    return keyboard

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, Я - бот по созданию сигналов, на кнопках указаны каналы с которых я могу переводить сигналы. Перед тем как скинуть сигнал незабудь выбрать канал', reply_markup=get_keyboard())

@bot.message_handler(commands=['fortune']) # ОБРАБОТКА СИГНАЛА С КАНАЛА FORTUNE CRYPTO
def fortune_message(message):
    signal = bot.send_message(message.chat.id, 'Отлично, теперь скиньте сигнал с канала FORTUNE CRYPTO 🧿')
    bot.register_next_step_handler(signal, output)

def output(message):
    input = message.text
    try:
        # РЕГУЛЯРКА ПО СИГНАЛАМ ФОРТУНЫ
        # получения названия монеты
        pattern = r'\w+'
        res = re.search(pattern, input)
        coin = res[0]

        # получения в какое направление открывать сделку
        pattern = r'\(\w+\)' 
        res = re.search(pattern, input)
        order = res[0][1:-1]

        # цена входа в сделку
        pattern1 = r'Entry+.+' #пока что панацея, если получится сравнивать по айди канала или названию канала будет круто
        res = re.search(pattern1, input)
        entry = res[0][0:-2].replace('Entry', '').replace(':', '').replace(' ', '')

        # получения целей
        pattern = r'Targets+.+\n.+' 
        res = re.search(pattern, input)
        targets = res[0][10:]

        # получения стоп лосса
        pattern = r'Stoploss+.+' 
        res = re.search(pattern, input)
        sp = res[0][10:-2]

        # получение плеча
        pattern = r'Leverage+.+\n.+' 
        res = re.search(pattern, input)
        leverage = res[0][16:-20]
        output = f'''
#{coin}
Вход в сделку {order}:{coin}USDT
Цена входа: {entry}
Цели: {targets}
Стоп лосс: {sp}

Плечо: {leverage}
'''
        bot.send_message(message.chat.id, output)
    except:
        bot.send_message(message.chat.id, "Вы сделали что-то не то, попробуйте еще раз /start")

@bot.message_handler(commands=['btc']) # ОБРАБОТКА СИГНАЛА С КАНАЛА SIGNALS BTC AND ALTS
def btc_message(message):
    signal = bot.send_message(message.chat.id, "Отлично, теперь пришлите сигнал с канала SIGNALS BTC AND ALTS")
    bot.register_next_step_handler(signal, outputbtc)

def outputbtc(message):
    input = message.text
    try:
        # РЕГУЛЯРКА ПО БТС АЛТС
        # получения названия монеты
        pattern = r'\w+'
        res = re.search(pattern, input)
        coin = res[0].upper()

        # получения в какое направление открывать сделку
        pattern = r'.+' 
        res = re.search(pattern, input)
        order = res[0].split()[1].upper()

        # цена входа
        entry = 'по рынку'

        # получения целей
        pattern = r'Targets+.+' 
        res = re.search(pattern, input)
        targets = res[0].replace('Targets', '').replace(' ', '')

        # получения стоп лосса
        pattern = r'Stop+.+' 
        res = re.search(pattern, input)
        sp = res[0].replace('Stop', '').replace(' ', '')

        # плечо
        leverage = "10x"

        output = f'''
#{coin}
Вход в сделку {order}:{coin}USDT
Цена входа: {entry}
Цели: {targets}
Стоп лосс: {sp}

Плечо: {leverage}
'''
        bot.send_message(message.chat.id, output)
    except:
        bot.send_message(message.chat.id, "Вы сделали что-то не то, попробуйте еще раз")

@bot.message_handler(commands=['plus']) # ОБРАБОТКА СИГНАЛА С КАНАЛА Trading Plus
def btc_message(message):
    signal = bot.send_message(message.chat.id, "Отлично, теперь пришлите сигнал с канала Trading Plus")
    bot.register_next_step_handler(signal, outputplus)

def outputplus(message):
    input = message.text
    try:
        # РЕГУЛЯРКА ПО ТРЭЙДИНГ ПЛЮС
        # получения названия монеты
        pattern = r'Торговая пара+.+'
        res = re.search(pattern, input)
        coin = res[0].replace("Торговая пара: ", '').replace("/USDT", '')

        # получения в какое направление открывать сделку
        pattern = r'\n\n\w+'
        res = re.search(pattern, input)
        order = res[0].replace("\n", "")

        # цена входа в сделку
        pattern1 = r'Вход+.+'
        res = re.search(pattern1, input)
        entry = res[0].replace('Вход', '').replace(':', '').replace(' ', '')

        # получения целей
        pattern1 = r'\d-я цель+.+\n.+' 
        pattern2 = r'Тейк-профит+.+\n.+' 
        res1 = re.search(pattern1, input)
        res2 = re.search(pattern2, input)
        res2 = res2[0].replace("Тейк-профит: ", "").replace("Стоп-лосс: по усмотрению", "").replace("\n", "")
        order2 = res2
        order1 = res1[0].replace("1-я", "").replace("2-я", "").replace(" цель - ", "").replace("\n", " - ")
        targets = str(order1) + ' - ' + str(order2)


        # получения стоп лосса
        pattern = r'Стоп-лосс+.+' 
        res = re.search(pattern, input)
        sp = res[0].replace("Стоп-лосс: ", "")

        # плечо
        leverage = "10x"

        output = f'''
#{coin}
Вход в сделку {order}:{coin}USDT
Цена входа: {entry}
Цели: {targets}
Стоп лосс: {sp}

Плечо: {leverage}
'''
        bot.send_message(message.chat.id, output)
    except:
        bot.send_message(message.chat.id, "Вы сделали что-то не то, попробуйте еще раз")

bot.polling(none_stop=True, interval=0)















































'''
@bot.message_handler(func=lambda message: message.text == 'Фортуна')
def signals(message):
    input = message.text
    try:
        # РЕГУЛЯРКА ПО СИГНАЛАМ ФОРТУНЫ
        # получения названия монеты
        pattern = r'\w+'
        res = re.search(pattern, input)
        coin = res[0]

        # получения в какое направление открывать сделку
        pattern = r'\(\w+\)' 
        res = re.search(pattern, input)
        order = res[0][1:-1]

        # цена входа в сделку
        pattern1 = r'Entry+.+' #пока что панацея, если получится сравнивать по айди канала или названию канала будет круто
        res = re.search(pattern1, input)
        entry = res[0][0:-2].replace('Entry', '').replace(':', '').replace(' ', '')

        # получения целей
        pattern = r'Targets+.+\n.+' 
        res = re.search(pattern, input)
        targets = res[0][10:]

        # получения стоп лосса
        pattern = r'Stoploss+.+' 
        res = re.search(pattern, input)
        sp = res[0][10:-2]

        # получение плеча
        pattern = r'Leverage+.+\n.+' 
        res = re.search(pattern, input)
        leverage = res[0][16:-20]

        output = f''''''
#{coin}
Вход в сделку {order}:{coin}USDT
Цена входа: {entry}
Цели: {targets}
Стоп лосс: {sp}

Плечо: {leverage}
        ''''''

        bot.send_message(message.chat.id, output)
    except:
        bot.send_message(message.chat.id, "Попробуйте еще раз вы сделали что-не то")

@bot.message_handler(func=lambda message: message.text == 'Бтс альтс')
def signals(message):
    input = message.text
    try:
        # получения названия монеты
        pattern = r'\w+'
        res = re.search(pattern, input)
        coin = res[0]

        # получения в какое направление открывать сделку
        pattern = r'.+' 
        res = re.search(pattern, input)
        order = res[0].split()[1].upper()

        # цена входа
        entry = 'по рынку'

        # получения целей
        pattern = r'Targets+.+' 
        res = re.search(pattern, input)
        targets = res[0].replace('Targets', '').replace(' ', '')

        # получения стоп лосса
        pattern = r'Stop+.+' 
        res = re.search(pattern, input)
        sp = res[0].replace('Stop', '').replace(' ', '')

        # плечо
        leverage = "10x"


        output = f''''''
#{coin}
Вход в сделку {order}:{coin}USDT
Цена входа: {entry}
Цели: {targets}
Стоп лосс: {sp}

Плечо: {leverage}
        ''''''

        bot.send_message(message.chat.id, output)
    except:
        bot.send_message(message.chat.id, "Попробуйте еще раз вы сделали что-не то")

@bot.message_handler(func=lambda message: message.text == 'Трейдинг плюс')
def signals(message):
    input = message.text
    try:
        # получения названия монеты
        pattern = r'Торговая пара+.+'
        res = re.search(pattern, input)
        coin = res[0].replace("Торговая пара: ", '').replace("/USDT", '')

        # получения в какое направление открывать сделку
        pattern = r'\n\n\w+'
        res = re.search(pattern, input)
        order = res[0].replace("\n", "")

        # цена входа в сделку
        pattern1 = r'Вход+.+'
        res = re.search(pattern1, input)
        entry = res[0].replace('Вход', '').replace(':', '').replace(' ', '')

        # получения целей
        pattern1 = r'\d-я цель+.+\n.+' 
        pattern2 = r'Тейк-профит+.+\n.+' 
        res2 = re.search(pattern2, input)
        res1 = re.search(pattern1, input)
        res2 = res2[0].replace("Тейк-профит: ", "")
        order2 = res2[:3]
        order1 = res1[0].replace("1-я", "").replace("2-я", "").replace(" цель - ", "").replace("\n", " - ")
        targets = str(order1) + ' - ' + str(order2)


        # получения стоп лосса
        pattern = r'Стоп-лосс+.+' 
        res = re.search(pattern, input)
        sp = res[0].replace("Стоп-лосс: ", "")

        # плечо
        leverage = "10x"


        output = f''''''
#{coin}
Вход в сделку {order}:{coin}USDT
Цена входа: {entry}
Цели: {targets}
Стоп лосс: {sp}

Плечо: {leverage}
        ''''''

        bot.send_message(message.chat.id, output)
    except:
        bot.send_message(message.chat.id, "Попробуйте еще раз вы сделали что-не то")


'''