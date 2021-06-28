#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from threading import Thread, Timer
import argparse
import logging


class Unit:
    def __init__(self):
        # парсер берет роль юнита из аргументов
        self.parser = argparse.ArgumentParser(
            description='unit type - server or client')
        self.parser.add_argument(
            '--server', '-s', action='store_true', dest='server', help='unit become server')
        self.parser.add_argument(
            '--client', '-c', action='store_true', dest='client', help='unit become client')
        self.args = self.parser.parse_args()
        self.conn = None # cоединение
        self.addr = None # адрес юнита ip:port
        self.info = None # передаваемая информация
        self.listen = 1 # состояние юнита вкл/выкл
        self.server_socket = socket.socket()
        self.client_socket = socket.socket()
        self.name = f"unoctl-{socket.gethostname()}"
        if self.args.server:
            logging.info(f"{self.name} now is server")
            self.name = f"{self.name}-server"
        if self.args.client:
            self.name = f"{self.name}-client"
            logging.info(f"{self.name} now is client")
        logging.basicConfig(filename=f"{self.name}.log", level=logging.INFO)
        self.threads = []

    def server(self):
        logging.info("start server work")
        host = socket.gethostname()
        port = 5000
        data = ''
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        self.conn, self.addr = self.server_socket.accept()
        print('connected:', self.addr)
        # передача инициируется после получения сообщения start
        error_message = int.from_bytes(self.conn.recv(1024), 'little')

        while error_message:
            error_message = int.from_bytes(self.conn.recv(1024), 'little')

        # пока не придет сигнал о закрытии соединения со стороны клиента или сервера
        while data != 'close' and not error_message:
            # отправь данные и проверь, дошли ли они
            data = input("Server -> ")
            self.conn.sendall(data.encode())
            error_message = int.from_bytes(self.conn.recv(1024), 'little')
            if error_message:
                #  if not data:
                #     break
                logging.error(f"error on client side")
                print('error on client side')
                data = 'close'

    def client(self):
        logging.info("start client work")
        host = socket.gethostname()
        port = 5000
        try:
            self.client_socket.connect((host, port))
            error_message = 0
        except ConnectionRefusedError:
            error_message = 1
            logging.error(f"Can't connect to server")
        self.client_socket.send(error_message.to_bytes(1, 'little'))
        while not error_message:
            try:
                data = self.client_socket.recv(1024).decode()
                print('Received from server: ' + data)
                if data:
                    error_message = 0
                    self.client_socket.send(error_message.to_bytes(1, 'little'))
                else:
                    error_message = 1
            except KeyboardInterrupt:
                logging.error("input error")
                error_message = True
        self.stop()

    def listening(self):
        for thr in self.threads:
            thr.join()
            self.threads.remove(thr)
        if self.args.server:
            self.threads.append(Timer(interval=0, function=self.server))
            self.threads[-1].start()
        if self.args.client:
            self.threads.append(Timer(interval=0, function=self.client))
            self.threads[-1].start()

    def stop(self):
        for thr in self.threads:
            thr.cancel()
        self.conn.close()
        self.server_socket.close()
        self.client_socket.close()
        logging.warning("close connection")


unit = Unit()
unit.listening()
