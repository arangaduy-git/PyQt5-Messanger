from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
import UI_login
import UI_chat
import UI_registration
import UI_settings
import UI_change_password
import sqlite3
import hashlib
import socket
import threading
from datetime import date

conn = sqlite3.connect('users.sqlite')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   mail TEXT PRIMARY KEY,
   user_name TEXT,
   password TEXT,
   registration TEXT,
   birthday TEXT);
""")

conn.commit()
conn.close()


# класс смены пароля
class Change_Password(QtWidgets.QMainWindow, UI_change_password.Ui_MainWindow):
    def __init__(self, mail):
        super(Change_Password, self).__init__()
        self.setupUi(self)
        self.mail = mail
        print(self.mail)

        # Отключаем стандартные границы окна программы
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.center()

        self.close_app.clicked.connect(lambda: self.close())
        self.btn_change_password.clicked.connect(lambda: self.change_password())

    # Перетаскивание безрамочного окна
    # ==================================================================
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            pass

    # Обработчик события на выход из клиента
    def closeEvent(self, value: QtGui.QCloseEvent) -> None:
        try:
            self.close()
        except Exception as err:
            print(err)

    def change_password(self):
        first_password = hashlib.md5(self.line_edit_first_password.text().encode()).hexdigest()
        second_password = hashlib.md5(self.line_edit_second_password.text().encode()).hexdigest()
        print(first_password, second_password)

        con = sqlite3.connect('users.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM users
                            WHERE mail = '{self.mail}'""").fetchone()
        if result[2] == first_password:
            cur.execute(f"""UPDATE users
                        SET password = '{second_password}'
                        WHERE mail = '{self.mail}'""")
            con.commit()
            con.close()
            self.close()
        else:
            self.text_name.setStyleSheet('color: #EA2F4E;')
            self.line_edit_first_password.setStyleSheet("QLineEdit{\n"
                                              "    border-radius: 7px;\n"
                                              "    color: #EA2F4E;\n"
                                              "    padding: 2px;\n"
                                              "}")


    # ==================================================================


# класс настроек
class Settings(QtWidgets.QMainWindow, UI_settings.Ui_MainWindow):
    def __init__(self, mail):
        super(Settings, self).__init__()
        self.change_password = None
        self.mail = mail
        self.setupUi(self)

        # Отключаем стандартные границы окна программы
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.center()

        f = open('config.txt')
        read = f.read()
        ip = read.split('\n')[0]
        port = read.split('\n')[1]
        self.line_edit_ip.setText(ip)
        self.line_edit_port.setText(port)
        f.close()

        self.close_app.clicked.connect(lambda: self.close())
        self.turn_app.clicked.connect(lambda: self.showMinimized())
        self.btn_save_settings.clicked.connect(lambda: self.close_settings())
        self.btn_change_password.clicked.connect(lambda: self.open_change_password())

    # Перетаскивание безрамочного окна
    # ==================================================================
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            pass

    # ==================================================================

    # Обработчик события на выход из клиента
    def closeEvent(self, value: QtGui.QCloseEvent) -> None:
        try:
            self.close()
        except Exception as err:
            print(err)

    def close_settings(self):
        f = open('config.txt', 'w')
        ip = self.line_edit_ip.displayText()
        port = self.line_edit_port.displayText()
        print(ip + "\n" + port)
        f.write(ip + "\n" + port)
        f.close()
        self.close()

    def open_change_password(self):
        self.change_password = Change_Password(self.mail)
        self.change_password.show()
        self.close()


# класс входа
class Login(QtWidgets.QMainWindow, UI_login.Ui_MainWindow):
    def __init__(self):
        super(Login, self).__init__()
        self.chat = None
        self.registration = None
        self.setupUi(self)

        # Отключаем стандартные границы окна программы
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.center()

        self.close_app.clicked.connect(lambda: self.close())
        self.turn_app.clicked.connect(lambda: self.showMinimized())
        self.btn_registration.clicked.connect(lambda: self.open_registration())
        self.btn_login.clicked.connect(lambda: self.open_chat())

    # Перетаскивание безрамочного окна
    # ==================================================================
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            pass

    # ==================================================================

    # Обработчик события на выход из клиента
    def closeEvent(self, value: QtGui.QCloseEvent) -> None:
        try:
            self.close()
        except Exception as err:
            print(err)

    def open_registration(self):
        self.registration = Registration()
        self.registration.show()
        self.close()

    def open_chat(self):
        mail = self.line_edit_mail.text()
        password = hashlib.md5(self.line_edit_password.text().encode()).hexdigest()

        con = sqlite3.connect('users.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM users
                    WHERE mail = '{mail}'""").fetchone()
        con.close()
        if result is None:
            self.text_mail.setStyleSheet('color: #EA2F4E;')
            self.line_edit_mail.setStyleSheet("QLineEdit{\n"
                                              "    border-radius: 7px;\n"
                                              "    color: #EA2F4E;\n"
                                              "    padding: 2px;\n"
                                              "}")
            self.text_password.setStyleSheet('color: #FFFFFF;')
            self.line_edit_password.setStyleSheet("QLineEdit{\n"
                                                  "    border-radius: 7px;\n"
                                                  "    color: #000000;\n"
                                                  "    padding: 2px;\n"
                                                  "}")
        elif result[2] != password:
            self.text_password.setStyleSheet('color: #EA2F4E;')
            self.line_edit_password.setStyleSheet("QLineEdit{\n"
                                              "    border-radius: 7px;\n"
                                              "    color: #EA2F4E;\n"
                                              "    padding: 2px;\n"
                                              "}")
            self.text_mail.setStyleSheet('color: #FFFFFF;')
            self.line_edit_mail.setStyleSheet("QLineEdit{\n"
                                              "    border-radius: 7px;\n"
                                              "    color: #000000;\n"
                                              "    padding: 2px;\n"
                                              "}")
        else:
            self.chat = Chat(mail)
            self.chat.show()
            self.close()


# класс регистрации
class Registration(QtWidgets.QMainWindow, UI_registration.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Registration, self).__init__()
        self.chat = None
        self.login = None
        self.setupUi(self)

        # Отключаем стандартные границы окна программы
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.center()

        self.close_app.clicked.connect(lambda: self.close())
        self.turn_app.clicked.connect(lambda: self.showMinimized())
        self.btn_login.clicked.connect(lambda: self.open_login())
        self.btn_registration.clicked.connect(lambda: self.open_chat())

    # Перетаскивание безрамочного окна
    # ==================================================================
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            pass
    # ==================================================================

    # Обработчик события на выход из клиента
    def closeEvent(self, value: QtGui.QCloseEvent) -> None:
        try:
            self.close()
        except Exception as err:
            print(err)

    def open_login(self):
        self.login = Login()
        self.login.show()
        self.close()

    def open_chat(self):
        user_name = self.line_edit_name.text()
        mail = self.line_edit_mail.text()
        password = hashlib.md5(self.line_edit_password.text().encode()).hexdigest()
        date_of_birth = self.line_edit_date_of_bitrh.text()
        today = date.today()
        registration = str(today.day) + '.' + str(today.month) + '.' + str(today.year)

        if '.' in mail and '@' in mail:

            try:
                con = sqlite3.connect('users.sqlite')
                cur = con.cursor()
                user = (mail, user_name, password, registration, date_of_birth)
                cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?)", user)
                con.commit()
                con.close()
                self.chat = Chat(mail)
                self.chat.show()
                self.close()
            except:
                self.line_edit_mail.setStyleSheet("QLineEdit{\n"
                                                  "    border-radius: 7px;\n"
                                                  "    color: #EA2F4E;\n"
                                                  "    padding: 2px;\n"
                                                  "}")
                self.text_mail.setStyleSheet('color: #EA2F4E;')
        else:
            self.line_edit_mail.setStyleSheet("QLineEdit{\n"
                                              "    border-radius: 7px;\n"
                                              "    color: #EA2F4E;\n"
                                              "    padding: 2px;\n"
                                              "}")
            self.text_mail.setStyleSheet('color: #EA2F4E;')


# класс самого чата
class Chat(QtWidgets.QMainWindow, UI_chat.Ui_MainWindow):

    def __init__(self, mail):
        super(Chat, self).__init__()
        self.client = None
        self.settings = None
        self.setupUi(self)
        self.mail = mail

        con = sqlite3.connect('users.sqlite')
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM users
                            WHERE mail = '{mail}'""").fetchone()
        self.user_name = result[1]
        self.registration = result[3]
        self.birthday = result[4]
        con.close()

        self.text_date_of_birth_2.setText(self.birthday)
        self.text_mail_2.setText(self.mail)
        self.text_date_of_registration_2.setText(self.registration)
        self.name_account.setText(str(self.user_name).replace(' ', '\n'))
        self.name_account.setStyleSheet('color: #FFFFFF;')

        # Отключаем стандартные границы окна программы
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.center()

        self.close_app.clicked.connect(lambda: self.close())
        self.turn_app.clicked.connect(lambda: self.showMinimized())
        self.btn_settings.clicked.connect(lambda: self.open_settings())
        self.btn_connect.clicked.connect(lambda: self.connect())
        self.btn_send_message.clicked.connect(lambda: self.send_message())

    # Перетаскивание безрамочного окна
    # ==================================================================
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            pass

    # ==================================================================

    # Обработчик события на выход из клиента
    def closeEvent(self, value: QtGui.QCloseEvent) -> None:
        try:
            self.close()
        except Exception as err:
            print(err)

    def open_settings(self):
        self.settings = Settings(self.mail)
        self.settings.show()

    def listen_for_client(self, cli):
        while True:
            message = cli.recv(1024).decode()
            print(message)
            name = message.split(':')[0]
            msg = ' '.join(message.split(':')[1:])

            item = QtWidgets.QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignLeft)
            font = QtGui.QFont()
            font.setFamily("Montserrat Medium")
            font.setPointSize(10)
            item.setFont(font)

            item.setText(f"{name}:\n{msg}")
            self.chat.addItem(item)

    def connect(self):
        if self.client is None:
            f = open('config.txt')
            read = f.read()
            ip = read.split('\n')[0]
            port = int(read.split('\n')[1])
            print(ip, port)
            f.close()
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.client.connect((ip, port))
                self.client.send(' '.join(self.name_account.text().split('\n')).encode())
                self.line_edit_send_message.setText('')
                a1 = threading.Thread(target=self.listen_for_client, args=(self.client,))
                a1.start()
            except:
                self.line_edit_send_message.setText('Неверный IP адрес или порт')

    def send_message(self):
        self.client.send(self.line_edit_send_message.text().encode())


# запуск
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # myapp = Chat('1')
    myapp = Registration()
    myapp.show()
    sys.exit(app.exec_())