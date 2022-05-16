from client import *

args = ["http://localhost:5001", "http://localhost:5000/autentica", 4]
cliente = Client(*args)
print("client  ->  " + str(cliente))
print("    deposito(2, 5000)  ->  " + cliente.deposito(2, 5000))
print("    transferencia(2, 1, 2000)  ->  " + cliente.transferencia(2, 1, 2000))
print("    saldo(20)  ->  " + cliente.saldo(20))
print("    saque(1, 1000)  ->  " + cliente.saque(1, 1000))
print("    saldo(1)  ->  " + cliente.saldo(1))
print("    saldo(2)  ->  " + cliente.saldo(2))
print("")

args = ["http://localhost:5001", "http://localhost:5000/autentica", 5]
cliente = Client(*args)
print("client  ->  " + str(cliente))
print("    deposito(2, 5000)  ->  " + cliente.deposito(2, 5000))
print("    transferencia(2, 1, 2000)  ->  " + cliente.transferencia(2, 1, 2000))
print("    saldo(20)  ->  " + cliente.saldo(20))
print("    saque(1, 1000)  ->  " + cliente.saque(1, 1000))
print("    saldo(1)  ->  " + cliente.saldo(1))
print("    saldo(2)  ->  " + cliente.saldo(2))
print("")

args = ["http://localhost:5001", "http://localhost:5000/autentica", 10]
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
