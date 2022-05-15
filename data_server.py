from http.client import NOT_FOUND
from flask import Flask, request, jsonify, abort
from datetime import datetime

app = Flask(__name__)

# variaveis globais
numero_operacao = 1
contas = {
    "1": {"saldo": 1000, "locked": False, "locked_by": None},
    "2": {"saldo": 1000, "locked": False, "locked_by": None},
    "3": {"saldo": 1000, "locked": False, "locked_by": None},
    "4": {"saldo": 1000, "locked": False, "locked_by": None},
    "5": {"saldo": 1000, "locked": False, "locked_by": None},
    "6": {"saldo": 1000, "locked": False, "locked_by": None},
    "7": {"saldo": 1000, "locked": False, "locked_by": None},
    "8": {"saldo": 1000, "locked": False, "locked_by": None},
    "9": {"saldo": 1000, "locked": False, "locked_by": None},
    "10": {"saldo": 1000, "locked": False, "locked_by": None}
}

# constantes
LOCKED_ACCOUNT = -1
INVALID_ACCOUNT = -2
INVALID_VALUE = -3
NOT_FOUND = -4
TOKENS = ["ba0f", "4c0e", "a5fc", "b317", "4723",
          "a061", "1aac", "4396", "8ace", "8d69"]


def log(args):
    logfile = open("data_server.log", "+a")
    now = datetime.now().strftime("%m/%d/%Y %T")
    global numero_operacao
    for i in range(len(args)):
        args[i] = str(args[i])
    logfile.write(", ".join([now, str(numero_operacao)] + args) + "\n")
    numero_operacao += 1
    logfile.close()


def check_token(request):
    return 'token' in request.headers and request.headers['token'] in TOKENS


def validate_transaction(conta, id_negoc):
    if conta == INVALID_ACCOUNT:
        return INVALID_ACCOUNT
    if not conta in contas:
        return NOT_FOUND
    if contas[conta]["locked"] and contas[conta]["locked_by"] != id_negoc:
        return LOCKED_ACCOUNT
    return 0


def get_id_negoc(request):
    return request.args.get("id_negoc", request.remote_addr)


def get_conta(request):
    return request.args.get("conta", INVALID_ACCOUNT)


def get_valor(request):
    return request.args.get("valor", None)


@app.route("/status")
def status():
    return "data_server is up and running"


@app.route("/inspect")
def inspect():
    conta = get_conta(request)
    return jsonify(contas[conta])


@app.route("/autentica")
def autentica():
    id_negoc = get_id_negoc(request)
    if check_token(request):
        log([id_negoc, "autentica", True])
        return {}
    else:
        log([id_negoc, "autentica", False])
        abort(401)


@app.route("/getSaldo")
def getSaldo():
    if not check_token(request):
        abort(401)
    id_negoc = get_id_negoc(request)
    conta = get_conta(request)
    invalid_transaction = validate_transaction(conta, id_negoc)
    # todo: consultar saldo de conta bloqueada
    if invalid_transaction:
        return {"error_code": invalid_transaction}
    saldo = contas[conta]["saldo"]
    log([id_negoc, "getSaldo", conta, saldo])
    return {"saldo": saldo}


@app.route("/setSaldo")
def setSaldo():
    if not check_token(request):
        abort(401)
    id_negoc = get_id_negoc(request)
    conta = get_conta(request)
    invalid_transaction = validate_transaction(conta, id_negoc)
    if invalid_transaction:
        return {"error_code": invalid_transaction}
    valor = get_valor(request)
    if valor == None:
        return {"error_code": INVALID_VALUE}
    contas[conta]["saldo"] = int(valor)
    log([id_negoc, "setSaldo", conta, valor])
    return {}


@app.route("/getLock")
def getLock():
    if not check_token(request):
        abort(401)
    id_negoc = get_id_negoc(request)
    conta = get_conta(request)
    invalid_transaction = validate_transaction(conta, id_negoc)
    if invalid_transaction:
        return {"error_code": invalid_transaction}
    contas[conta]["locked"] = True
    contas[conta]["locked_by"] = id_negoc
    log([id_negoc, "getLock", conta])
    return {}


@app.route("/unLock")
def unLock():
    if not check_token(request):
        abort(401)
    id_negoc = get_id_negoc(request)
    conta = get_conta(request)
    invalid_transaction = validate_transaction(conta, id_negoc)
    if invalid_transaction:
        return {"error_code": invalid_transaction}
    contas[conta]["locked"] = False
    contas[conta]["locked_by"] = None
    log([id_negoc, "unLock", conta])
    return {}


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
