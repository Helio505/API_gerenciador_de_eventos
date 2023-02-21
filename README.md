# API para Gerenciador de Eventos

## Passos para execução
- Instalar os requerimentos necessários.
- Executar o arquivo [api.py](api.py)
- Escolher um request de um dos [possíveis requests](Descri%C3%A7%C3%A3o_requests.pdf).
- Enviar request. Se tiver body seguir os data types dos exemplos no final do README.

## Virtualenv
Estou usando um virtual environment. Para criar um, basta inserir o comando `python -m venv env` e ele será criado.
Ai basta ativar. No meu sistema o comando `cd .\env\Scripts\; .\activate; cd ..; cd ..` no Windows Terminal, já o ativa. Mas dependendo do sistema operacional ou terminal, outro comando deve ser usado para ativar.

## Requerimentos necessários
Para instalar os requerimentos necessários, nas versões corretas. Inserir comando `pip install -r requirements.txt`

O script inserir.py, serve para popular o banco de dados, para realizar testes. Executando-o, ele insere 4 linhas em cada tabela.

## Informações
- Eu utilizei o PDF que pode ser encontrado [aqui](Descri%C3%A7%C3%A3o_requests.pdf), para facilitar no design dos endpoints e requests. Nele estão todos os requests possíveis e uma breve descrição de cada.
- Para mandar requests, deve estar autenticado, o login é `admin` e a senha é `senha1234`.

## Especificações do Projeto/API
- Python 3.9.6
- Só foi testado no Windows 10.
- Utilizei o framework Flask
- A API está rodando em http://127.0.0.1:5000
- Utilizei o Postman no meu design
- Bibliotecas utilizadas:
    - Flask 2.2.3
    - Flask-HTTPAuth 4.7.0
    - Flask-RESTful 0.3.9
    - SQLAlchemy 2.0.4
    - SQLite 3.35.5 (padrão)


## Exemplos para requests que necessitam de dados (assumo que o banco de dados foi populado com `inserir.py`):

### POST /local
body:
```json
{
    "id": 5,
    "nome": "DDDDDDDDDD",
    "endereço": "EEEEEEEEEEEEEEEEE",
    "capacidade_maxima": 999
}
```

### POST /agendamento
body:
```json
{
    "id": 5,
    "nome_responsável": "Maria",
    "data_hora_inicio": "2023-02-19 19:12:39.363020",
    "data_hora_termino": "2026-05-23 23:59:59.000000",
    "id_local": 4
}
```

### PUT /local/{id}
```json
{
    "id": 4,
    "nome": "DDDDDDDDDD",
    "endereço": "EEEEEEEEEEEEEEEEE",
    "capacidade_maxima": 999
}
```

### PUT /agendamento/{id}
body:
```json
{
    "id": 3,
    "nome_responsável": "Marlene",
    "data_hora_inicio": "2023-02-19 19:12:39.363020",
    "data_hora_termino": "2024-02-19 19:12:39.363020",
    "id_local": 4
}
```

### GET /local/?id=4

obs. para queries, a data não usa aspas.

exemplo de uma possível response:
```json
{
    "message": "Sucesso, Varios elementos foram encontrados.",
    "data": [
        {
            "id": 5,
            "nome": "Clrrrub do sei ssssaalaoooouiiui fjdsçaljkfs",
            "endereço": "Avenida Naauuuullljh33333uuuuuu, QD 25oo09765Rua da Amizade",
            "capacidade_maxima": 123
        }
    ]
}
```

### GET /agendamento/?id_local=4

exemplo de uma possível response:
```json
{
    "message": "Sucesso, Varios elementos foram encontrados.",
    "data": [
        {
            "id": 3,
            "nome_responsável": "Marlon",
            "data_hora_inicio": "Sun, 19 Feb 2023 19:12:39 GMT",
            "data_hora_termino": "Mon, 19 Feb 2024 19:12:39 GMT",
            "id_local": 4
        },
        {
            "id": 4,
            "nome_responsável": "Rodrigo",
            "data_hora_inicio": "Sat, 23 May 2026 23:59:59 GMT",
            "data_hora_termino": "Sat, 23 May 2026 23:59:59 GMT",
            "id_local": 4
        },
    ]
}
```