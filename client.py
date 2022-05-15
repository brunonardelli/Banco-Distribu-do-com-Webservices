from telnetlib import AUTHENTICATION
import urllib.request
import json

AUTHENTICATION_SERVER_URL = "http://localhost:5000/autentica"
BUSINESS_SERVER_URL = "http://localhost:5001"
TOKENS = ["ba0f", "4c0e", "a5fc", "b317", "4723",
          "a061", "1aac", "4396", "8ace", "8d69"]


def request(segments):
    for i in range(len(segments)):
        segments[i] = str(segments[i])
    url = "/".join([BUSINESS_SERVER_URL] + segments)
    req = urllib.request.Request(url)
    req.add_header("token", TOKENS[0])
    response = urllib.request.urlopen(req)
    return json.loads(response.read())


def autentica():
    global authentication_server
    authentication_server = AUTHENTICATION_SERVER_URL
    req = urllib.request.Request(authentication_server)
    req.add_header("token", TOKENS[0])
    response = urllib.request.urlopen(req)
    return response.code == 200


def deposito(acnt, amt):
    if autentica():
        return request(["deposito", acnt, amt])
    else:
        print("falha de autenticacao")


def saque(acnt, amt):
    if autentica():
        return request(["saque", acnt, amt])
    else:
        print("falha de autenticacao")


def saldo(acnt):
    if autentica():
        return request(["saldo", acnt])
    else:
        print("falha de autenticacao")


def transferencia(acnt_orig, acnt_dest, amt):
    if autentica():
        return request(["transferencia", acnt_orig, acnt_dest, amt])
    else:
        print("falha de autenticacao")


print(deposito(2, 5000))
print(saldo(1))
print(saque(1, 500))
print(deposito(1, 4500))
print(saldo(1))
print(transferencia(1, 2, 1000))
print(saldo(1))
print(saldo(2))
print(deposito(2, 5000))
print(saldo(1))
print(saque(1, 500))
print(deposito(1, 4500))
print(saldo(1))
print(transferencia(1, 2, 1000))
print(saldo(1))
print(saldo(2))
print(deposito(2, 5000))
print(saldo(1))
print(saque(1, 500))
print(deposito(1, 4500))
print(saldo(1))
print(transferencia(1, 2, 1000))
print(saldo(1))
print(saldo(2))
print(deposito(2, 5000))
print(saldo(1))
print(saque(1, 500))
print(deposito(1, 4500))
print(saldo(1))
print(transferencia(1, 2, 1000))
print(saldo(1))
print(saldo(2))
print(deposito(2, 5000))
print(saldo(1))
print(saque(1, 500))
print(deposito(1, 4500))
print(saldo(1))
print(transferencia(1, 2, 1000))
print(saldo(1))
print(saldo(2))
print(deposito(2, 5000))
print(saldo(1))
print(saque(1, 500))
print(deposito(1, 4500))
print(saldo(1))
print(transferencia(1, 2, 1000))
print(saldo(1))
print(saldo(2))
print(deposito(2, 5000))
print(saldo(1))
print(saque(1, 500))
print(deposito(1, 4500))
print(saldo(1))
print(transferencia(1, 2, 1000))
print(saldo(1))
print(saldo(2))
print(deposito(2, 5000))
print(saldo(1))
print(saque(1, 500))
print(deposito(1, 4500))
print(saldo(1))
print(transferencia(1, 2, 1000))
print(saldo(1))
print(saldo(2))
print(deposito(2, 5000))
print(saldo(1))
print(saque(1, 500))
print(deposito(1, 4500))
print(saldo(1))
print(transferencia(1, 2, 1000))
print(saldo(1))
print(saldo(2))
print(deposito(2, 5000))
print(saldo(1))
print(saque(1, 500))
print(deposito(1, 4500))
print(saldo(1))
print(transferencia(1, 2, 1000))
print(saldo(1))
print(saldo(2))
print(deposito(2, 5000))
print(saldo(1))
print(saque(1, 500))
print(deposito(1, 4500))
print(saldo(1))
print(transferencia(1, 2, 1000))
print(saldo(1))
print(saldo(2))
print(deposito(2, 5000))
print(saldo(1))
print(saque(1, 500))
print(deposito(1, 4500))
print(saldo(1))
print(transferencia(1, 2, 1000))
print(saldo(1))
print(saldo(2))
print(deposito(2, 5000))
print(saldo(1))
print(saque(1, 500))
print(deposito(1, 4500))
print(saldo(1))
print(transferencia(1, 2, 1000))
print(saldo(1))
print(saldo(2))
print(deposito(2, 5000))
print(saldo(1))
print(saque(1, 500))
print(deposito(1, 4500))
print(saldo(1))
print(transferencia(1, 2, 1000))
print(saldo(1))
print(saldo(2))
print(deposito(2, 5000))
print(saldo(1))
print(saque(1, 500))
print(deposito(1, 4500))
print(saldo(1))
print(transferencia(1, 2, 1000))
print(saldo(1))
print(saldo(2))
print(deposito(2, 5000))
print(saldo(1))
print(saque(1, 500))
print(deposito(1, 4500))
print(saldo(1))
print(transferencia(1, 2, 1000))
print(saldo(1))
print(saldo(2))
