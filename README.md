# API para Gerenciador de Eventos

### Virtualenv
Estou usando um virtual environment. Para criar um, basta inserir o comando `python -m venv env` e ele será criado.
Ai basta ativar. No meu sistema o comando `cd .\env\Scripts\; .\activate; cd ..; cd ..` no Windows Terminal, já o ativa. Mas dependendo do sistema operacional ou terminal, outro comando deve ser usado para ativar.

### Requerimentos necessários
Para instalar os requerimentos necessários, nas versões corretas. Inserir comando `pip install -r requirements.txt`

O script inserir.py, serve para popular o banco de dados, para realizar testes. Executando-o, ele insere 4 linhas em cada tabela.

### Informações
- Eu utilizei o PDF que pode ser encontrado [aqui](Descri%C3%A7%C3%A3o_requests.pdf), para facilitar no design dos endpoints e requests. Nele estão todos os requests possíveis e uma breve descrição de cada.
- Para mandar requests, deve estar autenticado, o login é `admin` e a senha é `senha1234`.

### Especificações do Projeto/API
- Python 3.9.6
- Só foi testado no Windows 10.
- Utilizei o framework Flask
- Bibliotecas utilizadas:
    - Flask 2.2.3
    - Flask-HTTPAuth 4.7.0
    - Flask-RESTful 0.3.9
    - SQLAlchemy 2.0.4
    - SQLite 3.35.5 (padrão)
