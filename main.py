"""

Bot for channel.

That bot helps to moderate server.

There are some charachers that will look a little bit different in messanger.=)

"""
# -*- coding: utf-8 -*-
print("[*]Started!")

while True:
    try:
        import sys
        import time
        import telebot
        import threading
        from functools import wraps
        from collections import Counter
        from datetime import datetime
        # from config import TOKEN
        
        TOKEN = "780145984:AAFnKJ6kg4elDMDfz4DmT-nsh4OiHjBFOiE"
        
        # main thread locker
        lock = threading.Lock()
        # max depth setting(need for while True cycle)
        sys.setrecursionlimit(100000000)
        # enviroment variables
        TOKEN = telebot.TeleBot(TOKEN)
        # help strings
        STR_help = """
        <i>Привет!</i>
        <b> На нашем сервере </b> (http://t.me/TexnoD0m) <b> не много правил, в-общем вот они:
        1) Умеренная отправка сообщений, старайтесь не спамить;
        2) Не спамить командами бота;
        3) Не используйте маты слишком часто, уважайте друг-друга;
        4) Без личностных оскорблений, будьте адекватными;
        5) Никакой рекламы, раскрутки и тд.
        Вот и всё, спасибо за использование нашего канал и чата! </b>

        <i> Используйте другие функции бота для более полной информации о чате:) </i>
        """
        STR_info = """
        <i>Привет!</i>
        <b> Тебя приветствует бот нашего техно-канала </b> (http://t.me/TexnoD0m) <b> 
        Вы можете найти проверенную информацию из зарубежных и русских источников,
        красиво оформленную для вашего же удобства.
        Смотрите новости об сматрфонах, гаджетах и IT в целом только у нас! </b>

        <i> Используйте другие функции бота для более полной информации о чате:) </i>
        """
        # action variables
        SPAMMER_list = []
        SPAM_text = []
        ID_list = []
        # bool variables
        GET_mes = False
        GET_source = False
        GET_ans = False
        # text variables
        URL = ""
        TEXT = ""
        # markup
        group_markup = None


        def log(id, sent):
            """

            Bot logging.

            Func logger.

            """
            print("\n\n\n[*]Log-chat: ", id, "\n[*]Log-datetime: ",
                  datetime.now, "\n[*]Log-sent: ", sent)


        def locker(func):
            """

            Bot locking.

            Locking function for not trivial result printing.

            """
            @wraps(func)
            def wrapper(message=None, text=None):
                lock.acquire()
                try:
                    print("\n\n\n[*]Trying...")
                    if text is not None:
                        func(message, text)
                    else:
                        func(message)
                finally:
                    print("\n[*]Tried...")
                    lock.release()

            return wrapper


        def admin_menu(message, sent):
            """

            Button list.

            This function show buttons to admin.

            """
            message_id = message.chat.id
            user_markup = telebot.types.ReplyKeyboardMarkup()

            user_markup.row("Да", "Нет")
            user_markup.row("🤨Подумаю🤨")

            TOKEN.send_message(message_id, str(sent), reply_markup=user_markup,
                               parse_mode="HTML")


        def button_list(message, sent):
            """

            Button list.

            This function show buttons to user.

            """
            message_id = message.chat.id
            user_markup = telebot.types.ReplyKeyboardMarkup()

            user_markup.row("/ТехноНачало")
            user_markup.row("/ТехноПравила", "/ТехноИнфа")

            TOKEN.send_message(message_id, str(sent), reply_markup=user_markup)


        @locker
        def add_list(message):
            """

            Add list.

            Adding variables to spam lists.

            """
            global SPAMMER_list, ID_list, SPAM_text
            user_id = message.from_user.id

            SPAMMER_list.append(user_id)
            ID_list.append(message)
            SPAM_text.append(message.text)

            anti_spam(message)


        def anti_spam(message):
            """

            Spam list.

            Function for checking for spam.

            """
            global SPAMMER_list, ID_list, SPAM_text
            flag = True
            message_id = message.chat.id

            if len(SPAMMER_list) >= 15:
                TOKEN.send_chat_action(message_id, "typing")
                count = Counter(SPAMMER_list)
                try:
                    for i in SPAMMER_list:
                        spam_counter = count[i]

                        for j in SPAM_text:
                            spam_text_counter = count[j]

                            if spam_counter >= 10 or spam_text_counter >= 5:
                                print("\n\n\n[*]Anti-spamming function in!\n")

                                for el in ID_list:
                                    if el.from_user.id == i:
                                        if flag is True:
                                            first_name = el.from_user.first_name
                                            last_name = el.from_user.last_name
                                            username = ""

                                            if first_name != "None" and first_name is not None:
                                                username += first_name
                                            if last_name != "None" and last_name is not None:
                                                username += " " + last_name

                                            TOKEN.send_message(
                                                message_id,
                                                "{0}<b>, не спамьте в чате!</b>👿".
                                                format(username),
                                                parse_mode="HTML")

                                            flag = False

                                        TOKEN.delete_message(message_id, el.message_id)
                except Exception as e:
                    print(e)
                    print("[!]Could not delete message!\n")
                finally:
                    SPAMMER_list = []
                    ID_list = []
                    SPAM_text = []
                    flag = True


        def lists_func(message, string):
            """

            Info list.

            Decorator for function.

            """
            message_id = message.chat.id
            log(message_id, string)

            TOKEN.delete_message(message_id, message.message_id)
            TOKEN.send_chat_action(message_id, "typing")

            mes = TOKEN.send_message(message_id, string, parse_mode="HTML")

            time.sleep(30)

            TOKEN.delete_message(mes.chat.id, mes.message_id)


        @TOKEN.message_handler(commands=["ТехноНачало", "start"])
        def start_bot(message):
            """

            Bot started.

            Function that says decription about bot.

            """
            add_list(message)
            button_list(message, "(͡๏̯͡๏)")
            lists_func(message,
                       "<b>Мега-крутой-иновационный бот сделанный для канала Техно Дом - Новости It!</b> (http://t.me/TexnoD0m)")


        @TOKEN.message_handler(commands=["ТехноПравила"])
        def rules_list(message):
            """

            Rules list.

            Shows rules in server.

            """
            add_list(message)
            lists_func(message, STR_help)


        @TOKEN.message_handler(commands=["ТехноИнфа"])
        def info_list(message):
            """

            Info list.

            Shows info about the server.

            """
            add_list(message)
            lists_func(message, STR_info)


        @TOKEN.message_handler(commands=["password123"])
        def url_list(message):
            """

            Url list.

            Sending url button.

            """
            global GET_mes, GET_source, GET_ans
            admin_menu(message, "<i>Админское меню включено</i>")
            TOKEN.send_message(message.chat.id, "<b>Введите ссылку на телеграф</b>",
                               parse_mode="HTML")

            GET_mes = True
            GET_source = False
            GET_ans = False


        def result_text(message_id):
            """

            Resulting text.

            Sending result text.

            """
            global GET_ans, group_markup
            user_markup = telebot.types.InlineKeyboardMarkup()

            btn_switch = telebot.types.InlineKeyboardButton(
                text="📩Поделиться📩",
                url="https://t.me/share/url?url=https%3A//t.me/joinchat/AAAAAFUR0t" +
                "J6cfCYKuWFPw&text=%D0%A1%D0%BC%D0%BE%D1%82%D1%80%D0%B8%2C%20%D0%BD" +
                "%D0%B0%D1%88%D1%91%D0%BB%20%D0%BA%D0%B0%D0%BD%D0%B0%D0" +
                "%BB%20%D1%81%20%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%8F%D" +
                "0%BC%D0%B8%20%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%" +
                "B3%D0%B8%D0%B9.%20%D0%9D%D0%B5%D0%B2%D0%B5%D1%80%D0%BE%D"
                "1%8F%D1%82%D0%" +
                "BD%D0%BE%20%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D0%B5%D1%81%D0%BD%D0%BE")
            btn_chat = telebot.types.InlineKeyboardButton(text="📝Чат📝",
                                                          url="https://t.me/joinchat/INP6PFeFE4Vz7BVGqjwQBA")
            btn_chat_1 = telebot.types.InlineKeyboardButton(text="Лайк",
                                                            url="https://t.me/joinchat/INP6PFeFE4Vz7BVGqjwQBA")
            btn_chat_2 = telebot.types.InlineKeyboardButton(text="Дизлайк",
                                                            url="https://t.me/joinchat/INP6PFeFE4Vz7BVGqjwQBA")

            user_markup.row(btn_chat_1, btn_chat_2)
            user_markup.add(btn_switch, btn_chat)

            TOKEN.send_message(message_id,
                               """<a href="{1}">Телеграф</a>\n
<a href="{0}">Источник</a>\n
""".format(URL, TEXT) + TEXT, reply_markup=user_markup, parse_mode="HTML")
            TOKEN.send_message(message_id, "<i>Прислать в группу?</i>",
                               parse_mode="HTML")

            group_markup = user_markup
            GET_ans = True


        @TOKEN.message_handler(content_types=["text"])
        def handle_text(message):
            """

            Text list.

            Checks for text spam.

            """
            global GET_mes, GET_source, GET_ans, group_markup, URL, TEXT
            print(message)

            message_id = message.chat.id
            text = message.text

            log(message_id, "Text got!")

            if GET_ans is True:
                if text.lower() == "да":
                    TOKEN.send_message(message_id,
                                       "<i>Сообщение было отправлено</i>",
                                       parse_mode="HTML")
                    TOKEN.send_message(
                        "@TexnoD0m",
                        """<a href="{1}">Телеграф</a>\n
<a href="{0}">Источник</a>\n
""".format(URL, TEXT) + TEXT, reply_markup=group_markup, parse_mode="HTML")

                    GET_ans = False
                elif text.lower() == "нет":
                    TOKEN.send_message(message_id,
                                       "<i>Сообщение не было отправлено</i>",
                                       parse_mode="HTML")

                    GET_ans = False
                else:
                    TOKEN.send_message(message_id,
                                       "<i>Введите ответ да или нет</i>",
                                       parse_mode="HTML")
            elif GET_source is True:
                URL = text

                result_text(message_id)

                GET_source = False
            elif GET_mes is True:
                TEXT = text

                TOKEN.send_message(message_id,
                                   "<b>Введите ссылку на исходник</b>",
                                   parse_mode="HTML")

                GET_mes = False
                GET_source = True
            else:
                add_list(message)


        @TOKEN.message_handler(content_types=["photo"])
        def get_photo(message):
            """

            Photo list.

            Checks for photo spam.

            """
            add_list(message)


        @TOKEN.message_handler(content_types=["document", "gif"])
        def get_gif(message):
            """

            Gif list.

            Checks for gif spam.

            """
            add_list(message)


        try:
            while True:
                # trying to get access to telegram servers
                try:
                    TOKEN.polling(none_stop=True)
                except Exception:
                    # urlib or request error while trying to get access to telegram api
                    print("\n\n\n[!]Internet error!\n")
                    time.sleep(3600)
        except Exception:
            print("\n\n\n[!]Emm!\n")
            time.sleep(1337)
            time.sleep(228)

        """

        Короче, не знаю как так получилось, но в общем всё достаточно прикольно.

        Я сейчас пытаюсь печатать на новой-старой клавиатуре которая беспроводная и она
        вроде бы успевает за моей скоростью, но хотя задержки видны + атом-багатом.

        Одни проблемы, как так.

        Ну лан, в общем, привет Тарас в будущем!

        """
    except Exception:
        print("\n\n\n[!]Emm!\n")
        time.sleep(1337)
        time.sleep(228)


print("[*]Stopped!")
        
