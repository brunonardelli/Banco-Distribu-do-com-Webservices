# Execução

## Servidor de dados
O comando abaixo inicializa o servidor de dados.

```sh
python3.8 data_server.py
```
Todo o log das operações executadas pelo servidor de dados são salvas no arquivo `data_server.log`.

---

## Servidor de negócio
O código abaixo inicializa um servidor de negócios na porta `5001`, com o servidor de dados executando na url `http://localhost:5000`.

```sh
python3.8 business_server.py http://localhost:5000 5001
```
Todo o log das operações executadas pelo servidor de negócio são salvas no arquivo `business_server.log`.

---

## Cliente
O código abaixo inicializa um cliente utilizando o servidor de negócios `http://localhost:5001` e se autenticando pela url `http://localhost:5000/autentica`.

```python
from client import *

client = Client("http://localhost:5001", "http://localhost:5000/autentica")

# Depósito de 5000 para a conta 2
client.deposito(2, 5000)

# Transferência de 2000, da conta 2 para a conta 1
client.transferencia(2, 1, 2000)

# Saque de 1000 da conta 1
client.saque(1, 1000)

# Saldo da conta 2
client.saldo(2)
```
---

## Demonstração
O código abaixo é usado para executar um script que inicializa um Cliente, realiza algumas operações e exibe o retorno delas na tela.

```sh
python3.8 executa-cliente.py
```
