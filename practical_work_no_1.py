import logging, os, re, paramiko
from dotenv import load_dotenv
from pathlib import Path
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

dotenv_path = Path('D:\PycharmProjects\pt_start_2024_spring\.env')
load_dotenv(dotenv_path=dotenv_path)
TOKEN = os.getenv('BOT_TOKEN')
host = os.getenv('HOST')
port = os.getenv('PORT')
username = os.getenv('USER')
password = os.getenv('PASSWORD')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Подключаем логирование
logging.basicConfig(
    filename='logfile.txt', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')

def helpCommand(update: Update, context):
    update.message.reply_text('Help!')

# 1. Поиск информации в тексте и вывод ее
def findEmailAdressesCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска email-адресов: ')

    return 'findEmailAdresses'

def findEmailAdresses(update: Update, context):
    user_input = update.message.text  # Получаем текст, содержащий(или нет) email-адреса
    emailAddrRegex = re.compile(r'''[A-z0-9!#$%&'*+-/=?^_`{|}~]+@[A-z0-9.-]+''')

    emailAdressesList = emailAddrRegex.findall(user_input)  # Ищем email-адреса

    if not emailAdressesList:  # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Email-адреса не найдены')
        return ConversationHandler.END  # Завершаем выполнение функции

    emailAdresses = ''  # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(emailAdressesList)):
        emailAdresses += f'{i + 1}. {emailAdressesList[i]}\n'  # Записываем очередной адрес
    update.message.reply_text(emailAdresses)  # Отправляем сообщение пользователю
    return ConversationHandler.END  # Завершаем работу обработчика диалога

def findPhoneNumbersCommand(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'findPhoneNumbers'

def findPhoneNumbers(update: Update, context):
    user_input = update.message.text  # Получаем текст, содержащий(или нет) номера телефонов
    phoneNumRegex = re.compile(r"((((8 \()|(\+7 \())|((8|\+7)[ (-]?))\d{3}((\) ?)|-| )?\d{3}([ -]?\d{2}){2})")  # формат 8 (000) 000-00-00

    phoneNumberList = phoneNumRegex.findall(user_input)  # Ищем номера телефонов
    if not phoneNumberList:  # Обрабатываем случай, когда номеров телефонов нет
        update.message.reply_text('Телефонные номера не найдены')
        return ConversationHandler.END  # Завершаем выполнение функции

    phoneNumbers = ''  # Создаем строку, в которую будем записывать номера телефонов
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i + 1}. {phoneNumberList[i][0]}\n'  # Записываем очередной номер
    update.message.reply_text(phoneNumbers)  # Отправляем сообщение пользователю
    return ConversationHandler.END  # Завершаем работу обработчика диалога

# 2. Проверка сложности пароля регулярным выражением.
def verifyPasswordCommand(update: Update, context):
    update.message.reply_text('Введите пароль, который нужно проверить: ')

    return 'verifyPassword'

def verifyPassword(update: Update, context):
    user_input = update.message.text  # Получаем текст
    verifyPasswordRegex = re.compile(r"(?=.*[0-9])(?=.*[!@#$%^&*()])(?=.*[a-z])(?=.*[A-Z])[0-9A-z!@#$%^&*()]{8,}")  # формат 8 (000) 000-00-00

    verifyPasswordRes = verifyPasswordRegex.search(user_input)  # Ищем номера телефонов
    if not verifyPasswordRes:  # Обрабатываем случай, когда пароль не подходит
        update.message.reply_text('Пароль простой')
        return ConversationHandler.END  # Завершаем выполнение функции
    else:
        update.message.reply_text('Пароль сложный')
        return ConversationHandler.END  # Завершаем работу обработчика диалога


# 3. Мониторинг Linux-системы
def replaceDataSymbols(data):
    return str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
def getReleaseCommand(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('cat /etc/os-release')
    data = stdout.read() + stderr.read()
    client.close()
    update.message.reply_text(replaceDataSymbols(data))

def getUname(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uname -a')
    data = stdout.read() + stderr.read()
    client.close()
    update.message.reply_text(replaceDataSymbols(data))

def getUptime(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    client.close()
    update.message.reply_text(replaceDataSymbols(data))

def getDf(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('df')
    data = stdout.read() + stderr.read()
    client.close()
    update.message.reply_text(replaceDataSymbols(data))

def getFree(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('free -h')
    data = stdout.read() + stderr.read()
    client.close()
    update.message.reply_text(replaceDataSymbols(data))

def getMpstat(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('mpstat -A')
    data = stdout.read() + stderr.read()
    client.close()
    update.message.reply_text(replaceDataSymbols(data))

def getW(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('w')
    data = stdout.read() + stderr.read()
    client.close()
    update.message.reply_text(replaceDataSymbols(data))

def getAuths(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('last > last_10_logins.txt && tail -10 last_10_logins.txt')
    data = stdout.read() + stderr.read()
    client.close()
    update.message.reply_text(replaceDataSymbols(data))

def getCritical(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('journalctl -p crit')
    data = stdout.read() + stderr.read()
    client.close()
    update.message.reply_text(replaceDataSymbols(data))

def getPs(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ps -aux | head')
    data = stdout.read() + stderr.read()
    client.close()
    update.message.reply_text(replaceDataSymbols(data))

def getSs(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ss | head')
    data = stdout.read() + stderr.read()
    client.close()
    update.message.reply_text(replaceDataSymbols(data))

def getAptListCommand(update: Update, context):
    update.message.reply_text('Введите all для вывода всех пакетов или название пакета для поиска информации о нем')

    return 'getAptList'

def getAptList(update: Update, context):
    user_input = update.message.text  # Получаем текст
    client.connect(hostname=host, username=username, password=password, port=port)
    if user_input == "all":  # Обрабатываем случай, когда пароль не подходит
        stdin, stdout, stderr = client.exec_command('apt list --installed | head')
        data = stdout.read() + stderr.read()
    else:
        stdin, stdout, stderr = client.exec_command('apt show ' + user_input)
        data = stdout.read() + stderr.read()
    client.close()
    update.message.reply_text(replaceDataSymbols(data))
    return ConversationHandler.END

def getServices(update: Update, context):
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('service --status-all | head')
    data = stdout.read() + stderr.read()
    client.close()
    update.message.reply_text(replaceDataSymbols(data))

def echo(update: Update, context):
    update.message.reply_text(update.message.text)

def main():
    updater = Updater(TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    convHandlerFindEmailAdresses = ConversationHandler(
        entry_points=[CommandHandler('find_email', findEmailAdressesCommand)],
        states={
            'findEmailAdresses': [MessageHandler(Filters.text & ~Filters.command, findEmailAdresses)],
        },
        fallbacks=[]
    )
    # Обработчик диалога
    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', findPhoneNumbersCommand)],
        states={
            'findPhoneNumbers': [MessageHandler(Filters.text & ~Filters.command, findPhoneNumbers)],
        },
        fallbacks=[]
    )

    convHandlerVerifyPassword = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verifyPasswordCommand)],
        states={
            'verifyPassword': [MessageHandler(Filters.text & ~Filters.command, verifyPassword)],
        },
        fallbacks=[]
    )

    convHandlerGetAptList = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', getAptListCommand)],
        states={
            'getAptList': [MessageHandler(Filters.text & ~Filters.command, getAptList)],
        },
        fallbacks=[]
    )

    # Регистрируем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(convHandlerFindEmailAdresses)
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerVerifyPassword)
    dp.add_handler(CommandHandler("get_release", getReleaseCommand))
    dp.add_handler(CommandHandler("get_uname", getUname))
    dp.add_handler(CommandHandler("get_uptime", getUptime))
    dp.add_handler(CommandHandler("get_df", getDf))
    dp.add_handler(CommandHandler("get_free", getFree))
    dp.add_handler(CommandHandler("get_mpstat", getMpstat))
    dp.add_handler(CommandHandler("get_w", getW))
    dp.add_handler(CommandHandler("get_auths", getAuths))
    dp.add_handler(CommandHandler("get_critical", getCritical))
    dp.add_handler(CommandHandler("get_ps", getPs))
    dp.add_handler(CommandHandler("get_ss", getSs))
    dp.add_handler(convHandlerGetAptList)
    # Регистрируем обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dp.add_handler(CommandHandler("get_services", getServices))
    # Запускаем бота
    updater.start_polling()

    # Останавливаем бота при нажатии Ctrl+C
    updater.idle()


if __name__ == '__main__':
    main()
