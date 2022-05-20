from client import *

VALID_TOKENS = ["ba0f", "4c0e", "a5fc", "b317", "6t2q",
                "a061", "1aac", "8w9k", "8ace", "8d69"]

tokens = VALID_TOKENS + ["__INVALID__"]

args = ["http://localhost:5001", "http://localhost:5000/autentica", tokens[4]]
cliente = Client(*args)
print("client  ->  " + str(cliente))
print("    deposito(2, 5000)  ->  " + cliente.deposito(2, 5000))
print("    transferencia(2, 1, 2000)  ->  " + cliente.transferencia(2, 1, 2000))
print("    saldo(20)  ->  " + cliente.saldo(20))
print("    saque(1, 1000)  ->  " + cliente.saque(1, 1000))
print("    saldo(1)  ->  " + cliente.saldo(1))
print("    saldo(2)  ->  " + cliente.saldo(2))
print("")

args = ["http://localhost:5001", "http://localhost:5000/autentica", tokens[5]]
cliente = Client(*args)
print("client  ->  " + str(cliente))
print("    deposito(2, 5000)  ->  " + cliente.deposito(2, 5000))
print("    transferencia(2, 1, 2000)  ->  " + cliente.transferencia(2, 1, 2000))
print("    saldo(20)  ->  " + cliente.saldo(20))
print("    saque(1, 1000)  ->  " + cliente.saque(1, 1000))
print("    saldo(1)  ->  " + cliente.saldo(1))
print("    saldo(2)  ->  " + cliente.saldo(2))
print("")

args = ["http://localhost:5001", "http://localhost:5000/autentica", tokens[10]]
cliente = Client(*args)
print("client  ->  " + str(cliente))
print("    deposito(2, 5000)  ->  " + cliente.deposito(2, 5000))
print("    transferencia(2, 1, 2000)  ->  " + cliente.transferencia(2, 1, 2000))
print("    saldo(20)  ->  " + cliente.saldo(20))
print("    saque(1, 1000)  ->  " + cliente.saque(1, 1000))
print("    saldo(1)  ->  " + cliente.saldo(1))
print("    saldo(2)  ->  " + cliente.saldo(2))
print("")

args = ["http://localhost:5001", "http://localhost:5000/autentica"]
cliente = Client(*args)
print("client  ->  " + str(cliente))
print("    deposito(2, 5000)  ->  " + cliente.deposito(2, 5000))
print("    transferencia(2, 1, 2000)  ->  " + cliente.transferencia(2, 1, 2000))
print("    saldo(20)  ->  " + cliente.saldo(20))
print("    saque(1, 1000)  ->  " + cliente.saque(1, 1000))
print("    saldo(1)  ->  " + cliente.saldo(1))
print("    saldo(2)  ->  " + cliente.saldo(2))
print("")
