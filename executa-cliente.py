"""
DESENVOLVIDO POR:
NOME: Breno F Pinho        - TIA: 41932110
NOME: Bruno N Santiago     - TIA: 41933613
NOME: Guilherme B Pereira  - TIA: 32060785

DISCIPLINA: Computação distribuída
TURMA: 6N
"""

from client import Client
from random import seed, randint

# tokens validos
VALID_TOKENS = ["ba0f", "4c0e", "a5fc", "b317", "6t2q",
                "a061", "1aac", "8w9k", "8ace", "8d69"]

# quantidade de contas no servidor de dados
NUM_CONTAS = 10

# endereco dos servidores de negocio
BUSINESS_SERVERS = ["http://localhost:5001", "http://localhost:5002", "http://localhost:5003"]

# endereco de autenticacao
AUTHENTICATION_URL = "http://localhost:5000/autentica"

seed()

tokens = VALID_TOKENS + ["__INVALID__"]

for i in range(10):
  args = [
    # seleciona um servidor do array "BUSINESS_SERVERS" de forma aleatoria
    BUSINESS_SERVERS[randint(0, len(BUSINESS_SERVERS)-1)],
    AUTHENTICATION_URL,
    # seleciona um token do array "tokens" de forma aleatoria
    tokens[randint(0, len(tokens)-1)]
  ]

  # contas aleatorias para as operacoes
  contas = [
    randint(0, NUM_CONTAS),
    randint(0, NUM_CONTAS),
    randint(0, NUM_CONTAS),
    randint(0, NUM_CONTAS)]

  # inicializa o cliente com os argumentos aleatorios
  client = Client(*args)

  print(f"client  ->  {str(client)}")
  # realiza as operacoes e imprime o retorno
  print(f"    saque({str(contas[0])}, 500)  ->  {client.saque(contas[0], 500)}")
  print(f"    deposito({str(contas[2])}, 5000)  ->  {client.deposito(contas[2], 5000)}")
  print(f"    transferencia({str(contas[2])}, {str(contas[1])}, 2000)  ->  {client.transferencia(contas[2], contas[1], 2000)}")
  print(f"    saque({str(contas[3])}, 1000)  ->  {client.saque(contas[3], 1000)}")
  # consulta o saldo e imprime o retorno
  print(f"    saldo({str(contas[0])})  ->  {client.saldo(contas[0])}")
  print(f"    saldo({str(contas[1])})  ->  {client.saldo(contas[1])}")
  print(f"    saldo({str(contas[2])})  ->  {client.saldo(contas[2])}")
  print(f"    saldo({str(contas[3])})  ->  {client.saldo(contas[3])}")

  print("")
