
import logging
import csv
import telebot
from telebot import types
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



bot = telebot.TeleBot('your API')

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Да', 'Нет')

keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('Регистрация', 'Нет')


keyboard3 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard3.row('/start')

keyboard4 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard4.row('Да правильно', 'Неправильно')

keyboard5 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=False) 
keyboard5.row('Влажный кашель')
keyboard5.row('Сухой кашель') 
keyboard5.row("Лихорадка, головная боль")
keyboard5.row("Насморк") 
keyboard5.row("Боль в горле")

keyboard6 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard6.row("Продолжить","Выйти")


User_name = {}
email = ''
res = ''


def send_email(User_name):

    
    global res
    user_email = str(User_name['email'])
    
    fromaddr = "botdoctor23@gmail.com"
    toaddr = user_email
    mypass = "123456Doctor"
    
    body = f"Здравствуйте {str(User_name['first_name'])}\n\n{str(res)}\n\nС уважением команда Коди-Руй"
    
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Это сообщение было отправлено Вам от телеграм Доктор-бот"
    
    
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, mypass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

# функция для записа 
def write_csv(User_name):
    with open('doctor-bot.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((User_name['first_name'],
                        User_name['surname'],
                        User_name['age'],
                        User_name['email']
                        ))



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Вас приветсвует персональный ассистент по диагностированию болезней Доктор Бот', reply_markup=keyboard1)  
    bot.send_message(message.chat.id, 'Вы готовы?')



@bot.message_handler(content_types=['text'])

def start(message):
    
    global User_name
    
    if message.text == 'Нет':
        bot.send_message(message.chat.id, 'Всего Доброго! Будьте здоровы!')
        bot.send_message(message.chat.id, "Чтобы начать сначала, напишите '/start'", reply_markup=keyboard3)
        bot.register_next_step_handler(message, start_message)
    
    elif message.text == 'Да':
        bot.send_message(message.chat.id, 'Для выявления заболевания, нам необходимо провести регистрацию и диагностику', reply_markup=keyboard2)
        
    if message.text == 'Регистрация':
     
        bot.send_message(message.from_user.id, "Как Ваше Имя:?")
        User_name[message.from_user.id] = {'first_name': '', 'surname': '', 'age': '', 'email': ''}
        print(User_name)
        bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name


def get_name(message):
    global User_name
    User_name[message.from_user.id]['first_name'] = message.text
    bot.send_message(message.from_user.id, 'Сообщите Вашу фамилию?')
    bot.register_next_step_handler(message, get_surname)
    
    print(User_name)
 
def get_surname(message): #получаем фамилию
    global User_name
    User_name[message.from_user.id]['surname'] = message.text
    bot.send_message(message.from_user.id, 'Введите Ваш возраст:')
    bot.register_next_step_handler(message, get_age)
    
    print(User_name)

def get_age(message): #получаем возраст
    global User_name
    User_name[message.from_user.id]['age'] = message.text
    bot.send_message(message.from_user.id, 'Введите Ваш электронный адрес:')
    bot.register_next_step_handler(message, get_email)
    
    print(User_name)

def get_email(message): #получаем email
    global User_name
    email = message.text
    User_name[message.from_user.id]['email'] = message.text
    print(User_name)
    write_csv(User_name[message.from_user.id])

    bot.send_message(message.from_user.id, "Был ли у Вас контакт с больным ОРВИ, и было ли у Вас переохлаждение организма?", reply_markup=keyboard1)                                  
    bot.register_next_step_handler(message, get_diagnoz_1)
  
def get_diagnoz_1(message):
    global res

    if message.text == 'Нет':
        res = "Вам рекомендуется:\
            \nВам нужно срочно обратиться к врачу. Не тяните с этим"
        
        bot.send_message(message.chat.id, 'Для уточнения диагноза и назначения лечения, запишитесь на прием к лечащему врачу.\
            \nМожете перейти по ссылке https://zdorovie-lab.kg/')
        bot.send_message(message.chat.id, "Чтобы начать сначала, напишите '/start'")
        send_email(User_name[message.from_user.id])
        bot.register_next_step_handler(message, start_message)  

    if message.text == 'Да':
        bot.send_message(message.chat.id,"Наблюдается ли у Вас данные симптомы в совокупности:\
            \n1.Высокая температура(выше 39*С)\
            \n2.Кашель\
            \n3.Ввыделение мокроты\
            \n4.Боль в горле", reply_markup=keyboard1)
        bot.register_next_step_handler(message, get_diagnoz_2)

def get_diagnoz_2(message):
    global res
    if message.text == 'Да':
        res = "Вам рекомендуется:\
            \nВам нужно срочно обратиться к врачу. Не тяните с этим"
        send_email(User_name[message.from_user.id])
        bot.send_message(message.chat.id, 'Вам нужно срочно обратиться к лечащему врачу.\
            \nМожете перейти по ссылке https://zdorovie-lab.kg/')
        bot.send_message(message.chat.id, "Чтобы начать сначала, напишите '/start'")
        bot.register_next_step_handler(message, start_message)  
    if message.text == 'Нет':
        bot.send_message(message.chat.id,"Наблюдается ли у Вас ухудшение состояния?", reply_markup=keyboard1)
        bot.register_next_step_handler(message, get_diagnoz_3)


def get_diagnoz_3(message):
    global email
    global User_name
    global res
    if message.text == 'Да':
        res = "Вам рекомендуется:\
            \nВам нужно срочно обратиться к врачу. Не тяните с этим"
        send_email(User_name[message.from_user.id])
        bot.send_message(message.chat.id, 'Вам нужно срочно обратиться к лечащему врачу.\
            \nМожете перейти по ссылке https://zdorovie-lab.kg/')
        bot.send_message(message.chat.id, "Чтобы начать сначала, напишите '/start'")
        bot.register_next_step_handler(message, start_message)  
    if message.text == 'Нет':
        bot.send_message(message.chat.id,"Следует принимать препараты для лечения симптомов, Выберите симптом:", reply_markup=keyboard5)
        bot.register_next_step_handler(message, get_diagnoz_3)

    if  message.text == 'Влажный кашель':
        res = "Вам рекомендуется:\
            \nОтхаркивающие средства на основе растительных компонентов (АЦЦ, Бромгексин), ингаляция, растирание грудной клетки"
        bot.send_message(message.chat.id,"Вам рекомендуется:\
            \nОтхаркивающие средства на основе растительных компонентов (АЦЦ, Бромгексин), ингаляция, растирание грудной клетки")
        bot.send_message(message.chat.id, "Выберете следующее действие:", reply_markup=keyboard6)
        bot.register_next_step_handler(message, get_diagnoz_3)

    if  message.text == 'Сухой кашель':
        res = "Вам рекомендуется:\
            \nПротивокашлевые и секретолитики:  на растительной основе, комбинированные, и центрального действия (Амбробене сироп)"
        bot.send_message(message.chat.id,"Вам рекомендуется:\
            \nПротивокашлевые и секретолитики:  на растительной основе, комбинированные, и центрального действия (Амбробене сироп)")
        bot.send_message(message.chat.id, "Выберете следующее действие:", reply_markup=keyboard6)
        bot.register_next_step_handler(message, get_diagnoz_3)

    if  message.text == 'Лихорадка, головная боль':
        res = "Вам рекомендуется:\
            \nКомбинированный препарат для лечения простуды (Цитрамон, Ибупрофен)"
        bot.send_message(message.chat.id,"Вам рекомендуется:\
            \nКомбинированный препарат для лечения простуды (Цитрамон, Ибупрофен)")
        bot.send_message(message.chat.id, "Выберете следующее действие:", reply_markup=keyboard6)
        bot.register_next_step_handler(message, get_diagnoz_3)

    if  message.text == 'Насморк':
        res = "Вам рекомендуется:\
            \nПрепарат для лечения насморка (Нафтизин, Аквафор); проделывание ингалляции с эфирными маслами"
        bot.send_message(message.chat.id,"Вам рекомендуется:\
            \nПрепарат для лечения насморка (Нафтизин, Аквафор); проделывание ингалляции с эфирными маслами")
        bot.send_message(message.chat.id, "Выберете следующее действие:", reply_markup=keyboard6)
        bot.register_next_step_handler(message, get_diagnoz_3)

    if  message.text == 'Боль в горле':
        res = "Вам рекомендуется:\
            \nПрепараты для лечения боли в горле: пастилки, таблетки, аэрозоли (Стрепсилс, Грамидин)"
        bot.send_message(message.chat.id,"Вам рекомендуется:\
            \nПрепараты для лечения боли в горле: пастилки, таблетки, аэрозоли (Стрепсилс, Грамидин)")
        bot.send_message(message.chat.id, "Выберете следующее действие:", reply_markup=keyboard6)
        bot.register_next_step_handler(message, get_diagnoz_3)

    if message.text == 'Продолжить':
        bot.send_message(message.chat.id,"Выберите другой симптом:", reply_markup=keyboard5)
        bot.register_next_step_handler(message, get_diagnoz_3)
        
    if message.text == 'Выйти':
        bot.send_message(message.chat.id, 'Всего Доброго! Будьте здоровы!')
        bot.send_message(message.chat.id, "Чтобы начать сначала, напишите '/start'", reply_markup=keyboard3)
        bot.register_next_step_handler(message, start_message)
        
        send_email(User_name[message.from_user.id])

print(User_name)
bot.polling(none_stop=True, interval=0)
