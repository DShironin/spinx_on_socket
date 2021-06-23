#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
from threading import Thread
import argparse


class Unit:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='unit type - server or client')
        self.parser.add_argument(
            '--server', '-s', action='store_true', dest='server', help='unit become server')
        self.parser.add_argument(
            '--client', '-c', action='store_true', dest='client', help='unit become client')
        self.args = self.parser.parse_args()
        self.conn = None
        self.addr = None
        self.info = None
        self.listen = 1
        self.server_socket = socket.socket()
        self.client_socket = socket.socket()

    def server(self):
        host = socket.gethostname()
        port = 5000
        data = ''
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        self.conn, self.addr = self.server_socket.accept()
        print('connected:', self.addr)
        while data.lower().strip() != 'close':
            message = self.conn.recv(1024).decode()
            if message == 'OK':
                #  if not data:
                #     break
                data = input("Server -> ")
                self.conn.sendall(data.encode())

    def client(self):
        host = socket.gethostname()
        port = 5000
        self.client_socket.connect((host, port))
        message = input("Client -> ")
        while message.lower().strip() != 'close':
            try:
                self.client_socket.send(message.encode())
                data = self.client_socket.recv(1024).decode()
                print('Received from server: ' + data)
                if data == 'OK':
                    message = " Client -> OK"
            except KeyboardInterrupt:
                print('input error')
        self.client_socket.close()

    def listening(self):
        if self.args.server:
            Thread(target=self.server).start()
        if self.args.client:
            Thread(target=self.client()).start()

    def stop(self):
        self.conn.close()
        self.server_socket.close()
        self.client_socket.close()
        print('close connection')


unit = Unit()
unit.listening()
