import telebot
import base64
import hashlib
import urllib.parse

token = ''
bot = telebot.TeleBot(token)

HELP = """
help - напечатать справку
codeit - зашифровать текст
base64 - расшифровать base64
urlencode - зашифровать в url
urldecode - расшифровать url"""

# Приветствие при старте
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Привет ✌️, я помогу тебе зашивровать или расшифровать популярные виды хэшей!")

# Вывод справки
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, HELP)

# Обрезка до аргумента
def extract_arg(arg):
    return arg.split()[1:]

# Зашифровать текст
@bot.message_handler(commands=['codeit'])
def codeit_message(message):
    extract = extract_arg(message.text)
    if len(extract) == 0:
        bot.send_message(message.chat.id, "Некорректная команда: /codeit text")
    else:
        # Список ответа
        output = []
        # Текст для шифрования
        message_bytes = extract[0].encode('utf-8')
        # Шифрование через hashlib
        output.append("MD5: " + hashlib.md5(message_bytes).hexdigest().upper())
        output.append("SHA-1: " + hashlib.sha1(message_bytes).hexdigest().upper())
        output.append("SHA-256: " + hashlib.sha256(message_bytes).hexdigest().upper())
        output.append("SHA-512: " + hashlib.sha512(message_bytes).hexdigest().upper())
        # Шифрование в base64
        base64_bytes = base64.b64encode(message_bytes)
        output.append("Base64: " + base64_bytes.decode('utf-8'))
        # Ответ бота
        bot.send_message(message.chat.id, str('\n'.join(output)))


# Расшифровка Base64
@bot.message_handler(commands=['base64'])
def base64_message(message):
    extract = extract_arg(message.text)
    if len(extract) == 0:
        bot.send_message(message.chat.id, "Некорректная команда: /base64 hash")
    else:
        decoded = base64.b64decode(extract[0].encode('utf-8'))
        decoded_ascii = decoded.decode('utf-8')
        bot.send_message(message.chat.id, decoded_ascii)

# Зашифровать в URL
@bot.message_handler(commands=['urlencode'])
def urlencode_message(message):
    extract = extract_arg(message.text)
    if len(extract) == 0:
        bot.send_message(message.chat.id, "Некорректная команда: /urlencode text")
    else:
        message_bytes = extract[0].encode('utf-8')
        bot.send_message(message.chat.id, urllib.parse.quote(message_bytes))

# Расшифровать URL
@bot.message_handler(commands=['urldecode'])
def urldecode_message(message):
    extract = extract_arg(message.text)
    if len(extract) == 0:
        bot.send_message(message.chat.id, "Некорректная команда: /urldecode url")
    else:
        message_bytes = extract[0].encode('utf-8')
        bot.send_message(message.chat.id, urllib.parse.unquote(message_bytes))

# Ответ на рандомные сообщения | должен быть после команд
@bot.message_handler(content_types=["text"])
def text_message(message):
    print(message.text)
    bot.send_message(message.chat.id, "Неизвестная команда")
    bot.send_message(message.chat.id, HELP)

bot.polling(none_stop=True)
