from flask import Flask, abort
from datetime import datetime
import urllib.request
import json

app = Flask(__name__)

# variaveis globais
numero_operacao = 1

# constantes
DATA_SERVER_URL = "http://localhost:5000"
IP = "1"


def log(args = []):
    logfile = open("business_server.log", "a")
    now = datetime.now().strftime("%m/%d/%Y %T")
    global numero_operacao
    logfile.write(", ".join([now, str(numero_operacao), IP] + args) + "\n")
    numero_operacao += 1
    logfile.close()


def has_error(response):
    return "error_code" in response


def lock_account(account):
    query_string = urllib.parse.urlencode({"id_negoc": IP, "conta": account})
    response = urllib.request.urlopen(DATA_SERVER_URL + "/getLock" + "?" + query_string)
    return json.loads(response.read())


def unlock_account(account):
    query_string = urllib.parse.urlencode({"id_negoc": IP, "conta": account})
    urllib.request.urlopen(DATA_SERVER_URL + "/unLock" + "?" + query_string)


def get_saldo(account):
    query_string = urllib.parse.urlencode({"id_negoc": IP, "conta": account})
    response = urllib.request.urlopen(DATA_SERVER_URL + "/getSaldo" + "?" + query_string)
    data = json.loads(response.read())
    return int(data["saldo"])


def set_saldo(account, saldo):
    query_string = urllib.parse.urlencode({"id_negoc": IP, "conta": account, "valor": saldo})
    urllib.request.urlopen(DATA_SERVER_URL + "/setSaldo" + "?" + query_string)


@app.route("/status")
def status():
    return "business_server is up and running"


@app.route("/deposito/<int:acnt>/<int:amt>")
def deposito(acnt, amt):
    response = lock_account(acnt)
    if has_error(response):
        abort(403)
    saldo = get_saldo(acnt)
    set_saldo(acnt, saldo + amt)
    unlock_account(acnt)
    log(["deposito", str(acnt), str(amt)])
    return {}


@app.route("/saque/<int:acnt>/<int:amt>")
def saque(acnt, amt):
    response = lock_account(acnt)
    if has_error(response):
        abort(403)
    saldo = get_saldo(acnt)
    set_saldo(acnt, saldo - amt)
    unlock_account(acnt)
    log(["saque", str(acnt), str(amt)])
    return {}


@app.route("/saldo/<int:acnt>")
def saldo(acnt):
    response = lock_account(acnt)
    if has_error(response):
        abort(403)
    saldo = get_saldo(acnt)
    unlock_account(acnt)
    log(["saldo", str(acnt)])
    return {"saldo": saldo}


@app.route("/transferencia/<int:acnt_orig>/<int:acnt_dest>/<int:amt>")
def transferencia(acnt_orig, acnt_dest, amt):
    response = lock_account(acnt_orig)
    if has_error(response):
        abort(403)
    response = lock_account(acnt_dest)
    if has_error(response):
        unlock_account(acnt_orig)
        abort(403)
    saldo = get_saldo(acnt_orig)
    set_saldo(acnt_orig, saldo - amt)
    saldo = get_saldo(acnt_dest)
    set_saldo(acnt_dest, saldo + amt)
    unlock_account(acnt_orig)
    unlock_account(acnt_dest)
    log(["transferencia", str(acnt_orig), str(acnt_dest), str(amt)])
    return {}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
