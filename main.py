import sqlite3

import requests
import telebot
import PySimpleGUI as sg
import random
from utils.db_api.schemas.user import User

bot = telebot.TeleBot("token_place")

conn = sqlite3.connect('db/registration.db', check_same_thread=False)
cursor = conn.cursor()


def make_win1():
    layout = [[sg.Text("Выберите способ авторизации")],
              [sg.Button("Registration", size=(25, 3), )],
              [sg.Button("Login", size=(25, 3))], ]
    window1 = sg.Window("Авторизируйтесь!", layout)
    while True:
        event, values = window1.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == "Login":
            layout = [[sg.Text('Login:', size=(30, 1), justification='right'),
                       sg.InputText(key='-lg-', do_not_clear=False)],
                      [sg.Text('Password:', size=(30, 1), justification='right'),
                       sg.InputText(key='-pw-', do_not_clear=False)],
                      [sg.Submit('Войти'), sg.Cancel('Отмена')]]

            window = sg.Window('Форма ввода').Layout(layout)
            while True:
                event, values = window.Read()
                if event is None:
                    break
                if event == 'Войти':

                    logid = cursor.execute(
                        "select user_id from User_list where login = ? AND password = ?", (
                            values['-lg-'], values['-pw-']))
                    logid2 = logid.fetchone()[0]

                    logpw = cursor.execute(
                        "select login, password, user_id from User_list where login = ? AND password = ? AND user_id", (
                            values['-lg-'], values['-pw-']))

                    if str(len(list(logpw))) > str(0):
                        sg.Popup('Шестизначный код подтверждения отправлен вам в Telegram!')
                        rnd_code = generate_code(6)

                        send_message(logid2, rnd_code)
                        layout = [[sg.Text('Введите шестизначный код:'),
                                   sg.InputText(key='-code-')],
                                  [sg.Submit('Ввод')]]
                        window = sg.Window('Введите код').Layout(layout)
                        while True:
                            event, values = window.Read()
                            if event is None:
                                break
                            if event == sg.WIN_CLOSED:
                                break
                            if event == 'Ввод' and str(rnd_code) == (values['-code-']):
                                sg.Popup('Успешный вход!')
                                window.close()
                                break
                            if event == 'Ввод' and str(rnd_code) != (values['-code-']):
                                sg.Popup('Неверный шестизначный код!')
                            continue

                    elif str(len(list(logpw))) == str(0):
                        sg.Popup('Неверный логин или пароль!')
                        break

        if event == "Registration":
            layout = [[sg.Text('TelegramID:', size=(30, 1), justification='right'),
                       sg.InputText(key='-tid-', do_not_clear=False)],
                      [sg.Text('Login:', size=(30, 1), justification='right'),
                       sg.InputText(key='-rlg-', do_not_clear=False)],
                      [sg.Text('Password:', size=(30, 1), justification='right'),
                       sg.InputText(key='-rpw-', do_not_clear=False)],
                      [sg.Submit('Регистрация'), sg.Cancel('Отмена')]]

            window = sg.Window('Форма ввода').Layout(layout)

            while True:
                event, values = window.Read()
                if event is None:
                    break
                if event == 'Регистрация':

                    requests.post('https://httpbin.org/post', data={(values['-tid-']): (values['-rlg-'])})

                    window.close()

        window1.close()


def db_table_val(user_id: int, login: str, password: str):
    cursor.execute('INSERT INTO User_list (user_id, login, password) VALUES (?, ?, ?)',
                   (user_id, login, password))
    conn.commit()


def send_message(user_id, rnd_code):
    bot.send_message(user_id, rnd_code)


def generate_code(code_len):
    all_char = '0123456789qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJIKOLP'
    code = ''
    for _ in range(code_len):
        num = random.randint(0, len(all_char) - 1)
        code += all_char[num]
        print(code)
    return code


async def registration(tg_id: str, login_: str, password: str, ver_code=random.randint(1000, 9999)):
    requests.post('https://httpbin.org/post', data={'key': 'value'})
        return "ex_tg_id"
    if await User.query.where(User.login == login_).gino.first():
        return "ex_login"

if __name__ == "__main__":
    make_win1()
