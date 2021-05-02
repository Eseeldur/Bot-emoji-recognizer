"""
Можно вводить смайлики в windows через "win+."
Если ввести "end", программа завершит свою работу и выведет то, что есть в таблицах в БД
Бот реализован без учета времени простоя в 1 мин (я знаю что в Unix можно это реализовать через
signal, SIGALRM, но он не работает в windows), к сожалению я не рассчитал время реализации
Но задание мне понравилось и делал я его с интересом
"""
import sqlite3
import datetime


db_file = 'DBemojiBot.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
# Создание таблицы
cursor.execute("""CREATE TABLE IF NOT EXISTS Messages
                  (message_id INTEGER PRIMARY KEY, time_of message TEXT NOT NULL, session_id INTEGER NOT NULL,
                   message_text TEXT NOT NULL, client_id INTEGER NOT NULL)
               """)
cursor.execute("""CREATE TABLE IF NOT EXISTS Sessions
                  (session_id INTEGER PRIMARY KEY, start_time TEXT NOT NULL, end_time TEXT NOT NULL)
               """)
with sqlite3.connect(db_file) as conn:
    cursor = conn.cursor()
    session_id = 0  # id сессии для записи в БД
    client_id = 0  # id клиента для записи в БД
    message_id = 0  # id сообщения для записи в БД


    def emoj_analis(session_id, client_id, message_id):
        happyemoji = ['\U0001F600', '\U0001F603', '\U0001F604',
                      '\U0001F601', '\U0001F606', '\U0001F602',
                      '\U0001F60A', '\U0001F929', '\U0001F973']  # список возможных смайлов
        sademoji = ['\U0001F612', '\U0001F61E', '\U0001F614',
                    '\U0001F61F', '\U0001F615', '\U0001F641',
                    '\U0001F629', '\U0001F62B', '\U0001F613']
        angryemoji = ['\U0001F47F', '\U0001F62C', '\U0001F624',
                      '\U0001F621', '\U0001F47A', '\U0001F480',
                      '\U0001F620', '\U0001F92F', '\U0001F928']
        start_time = datetime.datetime.now()  # время начала сессии для записи в БД
        end_time = ''  # время конца сессии для записи в БД
        message_text = ''  # текст сообщения для записи в БД

        # Индикация предыдущего сообщения юзера
        # 0 - не было сообщений
        # 1 - пред сообщение радостное
        # 2 - пред сообщение грустное
        # 3 - пред сообщение злое
        prev_answ = 0
        answer = ''
        session_flag = True  # Флаг сессии бота: True - сессия идет, False - беседа обнулилась

        while 1:
            answer = input()
            message_time = datetime.datetime.now()
            if answer == 'end':
                cursor.execute('INSERT INTO Sessions VALUES (?, ?, ?)', (session_id, start_time, end_time))
                print('Таблица Messages\nmessage_id, message_time, session_id, message_text, client_id')
                mes = cursor.execute('Select * From Messages')
                for row in mes:
                    print(*row, sep='\t')
                print('\nТаблица Sessions\nsession_id, start_time, end_time')
                ses = cursor.execute('Select * From Sessions')
                for row in ses:
                    print(*row, sep='\t')
                print('Бот выключается')
                raise SystemExit
            else:
                message_text = answer
                cursor.execute("INSERT INTO Messages VALUES (?, ?, ?, ?, ?)",
                               (message_id, message_time, session_id, message_text, client_id))
                message_id += 1
                if answer in happyemoji and prev_answ == 0:
                    print('Привет, о, ты улыбаешься, это хорошо!')
                    prev_answ = 1
                elif answer in sademoji and prev_answ == 0:
                    print('Привет, не грусти, все хорошо!')
                    prev_answ = 2
                elif answer in angryemoji and prev_answ == 0:
                    print('Привет, успокойся, не нужно злиться')
                    prev_answ = 3
                elif answer in happyemoji and prev_answ == 1:
                    print('Ты продолжаешь радоваться,это замечательно!')
                    prev_answ = 1
                elif answer in happyemoji and prev_answ == 2:
                    print('Хорошо, что ты перестал грустить и теперь радуешься!')
                    prev_answ = 1
                elif answer in happyemoji and prev_answ == 3:
                    print('Вот и правильно, не надо злиться, а радоваться!')
                    prev_answ = 1
                elif answer in sademoji and prev_answ == 1:
                    print('Ты был весел, а теперь грустишь, надеюсь ничего серьезного?')
                    prev_answ = 2
                elif answer in sademoji and prev_answ == 2:
                    print('Ты продолжаешь грустить, ну воот(')
                    prev_answ = 2
                elif answer in sademoji and prev_answ == 3:
                    print('Ты злился, а теперь грустишь, ну что это такое? посмотри хороший фильм, отдохни')
                    prev_answ = 2
                elif answer in angryemoji and prev_answ == 1:
                    print('Ты же радовался, а теперь злишься, раздражен, успокойся, все хорошо')
                    prev_answ = 3
                elif answer in angryemoji and prev_answ == 2:
                    print('Кажется, тебе стало хуже')
                    prev_answ = 3
                elif answer in angryemoji and prev_answ == 3:
                    print('Ты продолжаешь злиться, не навреди никому в таком состоянии')
                    prev_answ = 3
                else:
                    print('Беседа обнуляется')
                    session_flag = False
                    prev_answ = 0
                    end_time = datetime.datetime.now()
                    cursor.execute("INSERT INTO Sessions VALUES (?, ?, ?)", (session_id, start_time, end_time))
                    session_id += 1
                    client_id += 1
                    emoj_analis(session_id, client_id, message_id)

if __name__ == '__main__':
    print('Этот бот распознает смайлики и отвечает только на них\nВведи, пожалуйста, один смайлик:')
    emoj_analis(0, 0, 0)
