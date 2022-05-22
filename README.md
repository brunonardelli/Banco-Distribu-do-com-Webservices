# Requisitos

O projeto foi desenvolvido utilizando Python `3.8` com Flask `2.1`.

---

# Execução

## Servidor de Dados
O comando abaixo inicializa o servidor de dados. Por padrão, ele é executada na porta 5000.

```sh
python3.8 data_server.py
```
Todo o log das operações executadas pelo servidor de dados são salvas no arquivo `data_server.log` no formato a seguir:
```
TIMESTAMP, NUMERO OPERACAO, ID_NEGOC, OPERACAO, *PARAMETROS DA OPERAÇÃO
```
Rotas
| endpoint     | método | headers | query string           | descrição                                                     |
|--------------|:------:|---------|------------------------| --------------------------------------------------------------|
| `/status`    | `GET`  |         |                        | verifica status do servidor                                   |
| `/autentica` | `GET`  | token   | id_negoc               | autentica o token informado                                   |
| `/getSaldo`  | `GET`  | token   | id_negoc, conta        | retorna o saldo da conta informada                            |
| `/setSaldo`  | `GET`  | token   | id_negoc, conta, valor | atualiza o saldo com o valor informado                        |
| `/getLock`   | `GET`  | token   | id_negoc, conta        | bloqueia a conta para escrita de outros servidores de negócio |
| `/setLock`   | `GET`  | token   | id_negoc, conta        | libera a conta para escrita de outros servidores de negócio   |


---

## Servidor de Negócio
O código abaixo inicializa um servidor de negócios, com o servidor de dados executando na url `http://localhost:5000`, na porta `5001`. A porta é opcional, o valor padrão é `5000`.

```sh
python3.8 business_server.py http://localhost:5000 5001
```
Todo o log das operações executadas pelo servidor de negócio são salvas no arquivo `business_server.log` no formato a seguir:
```
TIMESTAMP, NUMERO OPERACAO, ID_NEGOC, OPERACAO, *PARAMETROS DA OPERAÇÃO
```

Rotas
| endpoint                                           | método | headers | descrição                                                                              |
|----------------------------------------------------|:------:|---------|----------------------------------------------------------------------------------------|
| `/status`                                          | `GET`  |         | verifica status do servidor                                                            |
| `/deposito/<conta>/<valor>`                        | `GET`  | token   | faz um deposito de `<valor>` na conta `<conta>`                                        |
| `/saque/<conta>/<valor>`                           | `GET`  | token   | faz um saque de `<valor>` na conta `<conta>`                                           |
| `/saldo/<conta>`                                   | `GET`  | token   | consulta o saldo da `<conta>`                                                          |
| `/transferencia/<conta_orig>/<conta_dest>/<valor>` | `GET`  | token   | faz uma transferência de `<valor>` da conta `<conta_orig>` para a conta `<conta_dest>` |

---

## Cliente
O código abaixo inicializa um cliente utilizando o servidor de negócios na url `http://localhost:5001` e se autenticando pela url `http://localhost:5000/autentica`.

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

# Demonstração
O código abaixo é usado para executar um script que inicializa um Cliente, realiza algumas operações e exibe o retorno delas na tela.

```sh
python3.8 executa-cliente.py
```

---

# Considerações

## Servidor de Dados
- Os parâmetros são enviados ao servidor de dados pela _query string_ da requisição. Exemplo `/getSaldo?id_negoc=1&conta=2`
- A falha na verificação do token aborta a requisição com status `401` (Não autorizado).
- Os parâmetros de cada requisição são validados e existe um código de erro para cada falha conforme a tabela abaixo:

| constante         | valor | descrição                                                    |
|-------------------|:-----:|--------------------------------------------------------------|
| `LOCKED_ACCOUNT`  | -1    | Conta bloqueada para escrita                                 |
| `INVALID_ACCOUNT` | -2    | Nenhuma conta foi passada na requisição                      |
| `INVALID_VALUE`   | -3    | Nenhum valor ou um valor inválido foi passado na requisição  |
| `NOT_FOUND`       | -4    | A conta passada na requisição não existe no banco de dados   |


---


## Servidor de Negócio
- Os parâmetros são enviados ao servidor pela url da requisição, conforme enunciado.
- O valor `id_negoc` passado ao servidor de dados tem o formato a seguir: `IP`:`PORTA`.
- Caso haja algum erro na requisição, a operação é abortada com um código HTTP conforme a tabela abaixo:

| código | descrição      | motivo                                                  |
|:------:|----------------|---------------------------------------------------------|
| `401`  | Não autorizado | O token não é válido ou não foi informado               |
| `403`  | Proibido       | A conta de origem/destino estão bloqueadas para escrita |
| `404`  | Não encontrado | A conta não foi encontrada ou o valor é inválido        |


---


## Cliente
- O cliente pode ser inicializado com um token e utiliza um token padrão caso nenhum seja passado.
- O cliente é um objeto com quatro métodos públicos: `deposito`, `saque`, `saldo` e `transferencia`.
- Foi criado uma classe `ClientErr` para tratamento de erros
- O cliente tem tratamento de erros e todas as operações retornam uma _string_ no formato abaixo:
```
body: <CORPO RESPOSTA>, status: <STATUS RESPOSTA>
```

---


## Script de testes
- O script de testes inicializa um cliente utilizando tokens válidos e inválidos e tenta fazer operações diversas em contas existentes e não existentes.
- Todo o resultado é tratado e exibido em tela.
