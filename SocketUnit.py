#!venv/bin/python3
# -*- coding: utf-8 -*-
import socket
import argparse
from threading import Timer, Thread


class SocketUnit:
    def __init__(self, block: int = 1024, port: int = 9090, period=0):
        self.parser = argparse.ArgumentParser(
            description='unit type - server or client')
        self.parser.add_argument(
            '--server', '-s', action='store_true', dest='server', help='unit become server')
        self.parser.add_argument(
            '--client', '-c', action='store_true', dest='client', help='unit become client')
        self.sock = socket.socket()
        self.port = port
        self.addr = ''
        self.period = period
        self.timer = Timer(interval=period, function=self.start)
        self.block = block
        self.work_mode = True
        self.args = self.parser.parse_args()
        self.post_thread = Thread(target=self.send())

    def start(self):
        if self.args.server:
            print('connected:', self.addr)
            self.sock.bind(('', self.port))
            self.sock.listen(1)
            conn, self.addr = self.sock.accept()
            while self.work_mode:
                data = conn.recv(self.block)
                if not data:
                    break
                conn.send(data.upper())
            conn.close()
        elif self.args.client:
            try:
                pass
            except ConnectionRefusedError:
                print('Cannot connect to server')
        else:
            print("No unit type, close")

    def stop(self):
        self.timer.cancel()
        self.timer.join()
        self.work_mode = False

    def send(self):
        sock = socket.socket()
        data = input()
        data.encode()
        sock.connect(('localhost', self.port))
        sock.send(data)
        data = sock.recv(self.block)
        sock.close()


if __name__ == '__main__':
    unit = SocketUnit()
    unit.start()
