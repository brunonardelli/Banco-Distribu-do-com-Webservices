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
    # o 11o. elemento eh um token invalido
    tokens = ["ba0f", "4c0e", "a5fc", "b317", "4723",
              "a061", "1aac", "4396", "8ace", "8d69",
              "__INVALID__"]

    def __init__(self, server_address, authentication_server, token=0):
        self.server_address = server_address
        self.authentication_server = authentication_server
        self.token = token if token < len(self.tokens) else len(self.tokens) - 1

    def __str__(self):
        return (f"server_address: {self.server_address} "
                f" authentication_server: {self.authentication_server} "
                f" token: {self.tokens[self.token]}")

    def __do_request(self, url):
        request = urllib.request.Request(url)
        request.add_header("token", self.tokens[self.token])
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
        return str(json.loads(response.read())) + ", status: " + str(response.status)

    def deposito(self, acnt, amt):
        return self.__auth() and self.__execute(["deposito", acnt, amt])

    def saque(self, acnt, amt):
        return self.__auth() and self.__execute(["saque", acnt, amt])

    def saldo(self, acnt):
        return self.__auth() and self.__execute(["saldo", acnt])

    def transferencia(self, acnt_orig, acnt_dest, amt):
        return self.__auth() and self.__execute(["transferencia", acnt_orig, acnt_dest, amt])


args = ["http://localhost:5001", "http://localhost:5000/autentica", 4]
cliente = Client(*args)
print("client  ->  " + str(cliente))
print("    deposito(2, 5000)  ->  " + cliente.deposito(2, 5000))
print("    transferencia(2, 1, 2000)  ->  " + cliente.transferencia(2, 1, 2000))
print("    saldo(20)  ->  " + cliente.saldo(20))
print("    saldo(1)  ->  " + cliente.saldo(1))
print("    saldo(2)  ->  " + cliente.saldo(2))
print("")

args = ["http://localhost:5001", "http://localhost:5000/autentica", 5]
cliente = Client(*args)
print("client  ->  " + str(cliente))
print("    deposito(2, 5000)  ->  " + cliente.deposito(2, 5000))
print("    transferencia(2, 1, 2000)  ->  " + cliente.transferencia(2, 1, 2000))
print("    saldo(20)  ->  " + cliente.saldo(20))
print("    saldo(1)  ->  " + cliente.saldo(1))
print("    saldo(2)  ->  " + cliente.saldo(2))
print("")

args = ["http://localhost:5001", "http://localhost:5000/autentica", 10]
cliente = Client(*args)
print("client  ->  " + str(cliente))
print("    deposito(2, 5000)  ->  " + cliente.deposito(2, 5000))
print("    transferencia(2, 1, 2000)  ->  " + cliente.transferencia(2, 1, 2000))
print("    saldo(20)  ->  " + cliente.saldo(20))
print("    saldo(1)  ->  " + cliente.saldo(1))
print("    saldo(2)  ->  " + cliente.saldo(2))
print("")

args = ["http://localhost:5001", "http://localhost:5000/autentica"]
cliente = Client(*args)
print("client  ->  " + str(cliente))
print("    deposito(2, 5000)  ->  " + cliente.deposito(2, 5000))
print("    transferencia(2, 1, 2000)  ->  " + cliente.transferencia(2, 1, 2000))
print("    saldo(20)  ->  " + cliente.saldo(20))
print("    saldo(1)  ->  " + cliente.saldo(1))
print("    saldo(2)  ->  " + cliente.saldo(2))
print("")
