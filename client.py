"""
DESENVOLVIDO POR:
NOME: Breno F Pinho        - TIA: 41932110
NOME: Bruno N Santiago     - TIA: 41933613
NOME: Guilherme B Pereira  - TIA: 32060785

DISCIPLINA: Computação distribuída
TURMA: 6N
"""

import urllib.request
import json


class ClientErr:
    def __init__(self, status):
        self.status = status

    def status(self):
        return self.status

    def read(self):
        return "{}"


class Client:
    def __init__(self, server_address, authentication_server, token="ba0f"):
        self.server_address = server_address
        self.authentication_server = authentication_server
        self.token = token

    def __str__(self):
        return (f"server_address: {self.server_address} "
                f" authentication_server: {self.authentication_server} "
                f" token: {self.token}")

    def __do_request(self, url):
        request = urllib.request.Request(url)
        request.add_header("token", self.token)
        try:
            return urllib.request.urlopen(request)
        except urllib.error.HTTPError as err:
            return ClientErr(err.status)

    def __auth(self):
        return self.__do_request(self.authentication_server)

    def __url_for(self, url_segments):
        for i in range(len(url_segments)):
            url_segments[i] = str(url_segments[i])
        return "/".join([self.server_address] + url_segments)

    def __execute(self, url_segments):
        url = self.__url_for(url_segments)
        response = self.__do_request(url)
        return "body: " + str(json.loads(response.read())) + ", status: " + str(response.status)

    def deposito(self, acnt, amt):
        return self.__auth() and self.__execute(["deposito", acnt, amt])

    def saque(self, acnt, amt):
        return self.__auth() and self.__execute(["saque", acnt, amt])

    def saldo(self, acnt):
        return self.__auth() and self.__execute(["saldo", acnt])

    def transferencia(self, acnt_orig, acnt_dest, amt):
        return self.__auth() and self.__execute(["transferencia", acnt_orig, acnt_dest, amt])
