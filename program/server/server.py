import threading
import socket


# класс сервера
class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.all_client = []

        # Запускаем прослушивание соединений
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip, self.port))
        self.server.listen(0)
        threading.Thread(target=self.connect_handler).start()
        print('Сервер запущен!')

    # Обрабатываем входящие соединения
    def connect_handler(self):
        while True:
            client, address = self.server.accept()
            if client not in self.all_client:
                self.all_client.append(client)
                name = client.recv(1024).decode()

                print(f'{address}, {name} - Успешное подключение к чату!')
                a1 = threading.Thread(target=self.listen_for_client, args=(client, name ))
                a1.start()

    def listen_for_client(self, client, name):
        while True:
            message = client.recv(1024).decode()
            print(message)
            for cl in self.all_client:
                cl.send(f'{name}:{message}'.encode())


if __name__ == "__main__":
    myserver = Server('localhost', 5555)
