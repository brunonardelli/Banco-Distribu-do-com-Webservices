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
TOKENS = ["ba0f", "4c0e", "a5fc", "b317", "6t2q",
          "a061", "1aac", "8w9k", "8ace", "8d69"]


def log(args):
    logfile = open("data_server.log", "+a")
    now = datetime.now().strftime("%m/%d/%Y %T")
    global numero_operacao
    for i in range(len(args)):
        args[i] = str(args[i])
    logfile.write(", ".join([now, str(numero_operacao)] + args) + "\n")
    numero_operacao += 1
    logfile.close()


def validate_token(request):
    return 'token' in request.headers and request.headers['token'] in TOKENS


def validate_account(conta):
    if conta == INVALID_ACCOUNT:
        return INVALID_ACCOUNT
    if not conta in contas:
        return NOT_FOUND
    return 0


def validate_write_mode(conta, id_negoc):
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
    '''for DEBUG: check server health'''
    return "data_server is up and running"


@app.route("/autentica")
def autentica():
    id_negoc = get_id_negoc(request)
    if validate_token(request):
        log([id_negoc, "autentica", True])
        return {}
    else:
        log([id_negoc, "autentica", False])
        abort(401)


@app.route("/getSaldo")
def getSaldo():
    # verifica se o token eh valido
    if not validate_token(request):
        abort(401)

    id_negoc = get_id_negoc(request)
    conta = get_conta(request)

    # verifica se a conta eh uma conta valida
    invalid_account = validate_account(conta)
    if invalid_account:
        return {"error_code": invalid_account}

    saldo = contas[conta]["saldo"]

    log([id_negoc, "getSaldo", conta, saldo])
    return {"saldo": saldo}


@app.route("/setSaldo")
def setSaldo():
    # verifica se o token eh valido
    if not validate_token(request):
        abort(401)

    id_negoc = get_id_negoc(request)
    conta = get_conta(request)

    # verifica se a conta eh uma conta valida
    invalid_account = validate_account(conta)
    if invalid_account:
        return {"error_code": invalid_account}

    # verifica se a conta esta liberada para escrita
    locked_account = validate_write_mode(conta, id_negoc)
    if locked_account:
        return {"error_code": locked_account}

    # verifica se o valor recebido eh valido
    valor = get_valor(request)
    if valor == None:
        return {"error_code": INVALID_VALUE}

    contas[conta]["saldo"] = int(valor)

    log([id_negoc, "setSaldo", conta, valor])
    return {}


@app.route("/getLock")
def getLock():
    # verifica se o token eh valido
    if not validate_token(request):
        abort(401)

    id_negoc = get_id_negoc(request)
    conta = get_conta(request)

    # verifica se a conta eh uma conta valida
    invalid_account = validate_account(conta)
    if invalid_account:
        return {"error_code": invalid_account}

    # verifica se a conta esta liberada para escrita
    locked_account = validate_write_mode(conta, id_negoc)
    if locked_account:
        return {"error_code": locked_account}

    contas[conta]["locked"] = True
    contas[conta]["locked_by"] = id_negoc

    log([id_negoc, "getLock", conta])
    return {}


@app.route("/unLock")
def unLock():
    # verifica se o token eh valido
    if not validate_token(request):
        abort(401)

    id_negoc = get_id_negoc(request)
    conta = get_conta(request)

    # verifica se a conta eh uma conta valida
    invalid_account = validate_account(conta)
    if invalid_account:
        return {"error_code": invalid_account}

    # verifica se a conta esta liberada para escrita
    locked_account = validate_write_mode(conta, id_negoc)
    if locked_account:
        return {"error_code": locked_account}

    contas[conta]["locked"] = False
    contas[conta]["locked_by"] = None

    log([id_negoc, "unLock", conta])
    return {}


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
