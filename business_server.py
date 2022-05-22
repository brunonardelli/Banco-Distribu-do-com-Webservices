"""
DESENVOLVIDO POR:
NOME: Breno F Pinho        - TIA: 41932110
NOME: Bruno N Santiago     - TIA: 41933613
NOME: Guilherme B Pereira  - TIA: 32060785

DISCIPLINA: Computação distribuída
TURMA: 6N
"""

from flask import Flask, abort, request
from datetime import datetime
import urllib.request
import json
import sys
import socket

app = Flask(__name__)

# variaveis globais
numero_operacao = 1

# constantes
LOCKED_ACCOUNT = -1
INVALID_ACCOUNT = -2
INVALID_VALUE = -3
NOT_FOUND = -4
TOKENS = ["ba0f", "4c0e", "a5fc", "b317", "6t2q",
          "a061", "1aac", "8w9k", "8ace", "8d69"]


def log(args):
    logfile = open("business_server.log", "+a")
    now = datetime.now().strftime("%m/%d/%Y %T")
    global numero_operacao
    for i in range(len(args)):
        args[i] = str(args[i])
    logfile.write(", ".join([now, str(numero_operacao)] + args) + "\n")
    numero_operacao += 1
    logfile.close()


def check_token(request):
    if 'token' in request.headers and request.headers['token'] in TOKENS:
        response = do_request(request.headers['token'], "/autentica", {"id_negoc": ip()})
        if not response.status == 200:
            abort(401)
    else:
        abort(401)


def ip():
    global port
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return str(local_ip) + ":" + str(port)


def get_token(request):
    return request.headers['token']


def has_error(response):
    return "error_code" in response


def check_errors(response):
    if has_error(response):
        if response["error_code"] == NOT_FOUND:
            abort(404)
        else:
            abort(403)


def do_request(token, endpoint, query = {}):
    global data_server_url
    # concatena a url do servidor de dados com o endpoint e a query
    url = data_server_url + endpoint + "?" + urllib.parse.urlencode(query)
    # adiciona o token no header de todas as requisicoes
    req = urllib.request.Request(url)
    req.add_header("token", token)
    return urllib.request.urlopen(req)


def lock_account(token, account):
    response = do_request(token, "/getLock", {"id_negoc": ip(), "conta": account})
    return json.loads(response.read())


def unlock_account(token, account):
    do_request(token, "/unLock", {"id_negoc": ip(), "conta": account})


def get_saldo(token, account):
    response = do_request(token, "/getSaldo", {"id_negoc": ip(), "conta": account})
    data = json.loads(response.read())
    return int(data["saldo"])


def set_saldo(token, account, saldo):
    do_request(token, "/setSaldo", {"id_negoc": ip(), "conta": account, "valor": saldo})


@app.route("/status")
def status():
    '''for DEBUG: check server health'''
    return "business_server is up and running"


@app.route("/deposito/<int:acnt>/<int:amt>")
def deposito(acnt, amt):
    check_token(request)
    token = get_token(request)
    response = lock_account(token, acnt)
    check_errors(response)
    saldo = get_saldo(token, acnt)
    set_saldo(token, acnt, saldo + amt)
    unlock_account(token, acnt)

    log([request.remote_addr, "deposito", acnt, amt])
    return {}


@app.route("/saque/<int:acnt>/<int:amt>")
def saque(acnt, amt):
    check_token(request)
    token = get_token(request)
    response = lock_account(token, acnt)
    check_errors(response)
    saldo = get_saldo(token, acnt)
    set_saldo(token, acnt, saldo - amt)
    unlock_account(token, acnt)

    log([request.remote_addr, "saque", acnt, amt])
    return {}


@app.route("/saldo/<int:acnt>")
def saldo(acnt):
    check_token(request)
    token = get_token(request)
    response = lock_account(token, acnt)
    check_errors(response)
    saldo = get_saldo(token, acnt)
    unlock_account(token, acnt)

    log([request.remote_addr, "saldo", acnt])
    return {"saldo": saldo}


@app.route("/transferencia/<int:acnt_orig>/<int:acnt_dest>/<int:amt>")
def transferencia(acnt_orig, acnt_dest, amt):
    check_token(request)
    token = get_token(request)
    response = lock_account(token, acnt_orig)
    check_errors(response)
    response = lock_account(token, acnt_dest)

    # aborta caso a conta de destino esteja bloqueada
    if has_error(response):
        unlock_account(token, acnt_orig)
        abort(403)

    saldo = get_saldo(token, acnt_orig)
    set_saldo(token, acnt_orig, saldo - amt)
    saldo = get_saldo(token, acnt_dest)
    set_saldo(token, acnt_dest, saldo + amt)
    unlock_account(token, acnt_orig)
    unlock_account(token, acnt_dest)

    log([request.remote_addr, "transferencia", acnt_orig, acnt_dest, amt])
    return {}


if __name__ == "__main__":
    global data_server_url, port
    data_server_url = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else 5000
    app.run(host="0.0.0.0", port=port, debug=True)
