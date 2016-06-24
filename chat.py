import asyncio
import requests
import os
from socket import *


class Utils:
    """
    Simple class to contain utility functions.
    """

    def curl_ip(self):
        curl = os.popen('curl ipinfo.io').read()
        return str.encode(curl)

    def parse(self, data):
        str_data = str(data)
        new_data = str_data.split('\'')[1].split('\\')
        return new_data


class Server:

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.utils = Utils()
        self.info = self.utils.curl_ip()
        self.clients = []
        self.path = 'nicks/'

    def run(self):
        self.loop.create_task(self.echo_server(('', 25000)))
        self.loop.run_forever()

    def is_cmd(self, client, data):
        data = self.utils.parse(data)
        data = data[0]
        if data[0] == '/':
            self.cmd_handle(client, data)
            return True
        else:
            return False

    def cmd_handle(self, client, data):
        cmd = data.split('/')[1]
        if 'register' in cmd:
            nick = cmd.split(' ')[1]
            self.register(client, nick)

    def broadcast(self, client, data):
        for c in self.clients:
            if c is not client:
                self.loop.sock_sendall(c, data)

    def register(self, client, nick):
        nick_path = '{}{}'.format(self.path, str(nick))
        nick_ls = os.popen('ls {}'.format(self.path)).read()
        taken_nicks = str(nick_ls).split('\n')
        nick_avail = 0

        for pos_nick in taken_nicks:
            if pos_nick == nick:
                nick_avail = 1
                print('Taken')

        if nick_avail == 0:
            with open(nick_path, 'w') as reg_file:
                reg_file.write('Taken by:{}'.format(client))
                print('You now own that nick.')

    async def echo_server(self, address):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind(address)
        sock.listen(5)
        sock.setblocking(False)
        while True:
            client, addr = await self.loop.sock_accept(sock)
            self.clients.append(client)
            print('Connection from {}'.format(str(addr)))
            self.loop.create_task(self.echo_handler(client))

    async def echo_handler(self, client):
        with client:
            while True:
                data = await self.loop.sock_recv(client, 10000)
                if not data:
                    break
                print(data)

                if self.is_cmd(client, data):
                    print(data)
                else:
                    self.broadcast(client, data)
                    print(data)
            print('Connection closed.')

chat = Server()
chat.run()
