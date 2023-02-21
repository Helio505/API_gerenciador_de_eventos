import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

# /////////////// PARTE PARA: CRIAÇÃO DO BANCO DE DADOS ///////////////////
engine = sqlalchemy.create_engine('sqlite:///db.db', echo=False)
Base = declarative_base()

class Local(Base):
    __tablename__ = 'local'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    endereço = Column(String(200))
    capacidade_maxima = Column(Integer())

class Agendamento(Base):
    __tablename__ = 'agendamento'

    id = Column(Integer, primary_key=True)
    nome_responsável = Column(String(100))
    data_hora_inicio = Column(DateTime())
    data_hora_termino = Column(DateTime())
    id_local = Column(Integer())

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
# /////////////// PARTE PARA: CRIAÇÃO DO BANCO DE DADOS ///////////////////

# //////////////////////// PARTE PARA INSERIR ////////////////////////
data_inicio_1 = datetime.datetime(
    year=2023, month=2, day=23, hour=23, minute=59, second=59)
data_inicio_2 = datetime.datetime(
    year=2024, month=3, day=23, hour=23, minute=59, second=59)
data_inicio_3 = datetime.datetime(
    year=2025, month=4, day=23, hour=23, minute=59, second=59)
data_inicio_4 = datetime.datetime(
    year=2026, month=5, day=23, hour=23, minute=59, second=59)

data_termino_1 = datetime.datetime(
    year=2024, month=2, day=23, hour=23, minute=59, second=59)
data_termino_2 = datetime.datetime(
    year=2025, month=4, day=23, hour=23, minute=59, second=59)
data_termino_3 = datetime.datetime(
    year=2026, month=5, day=23, hour=23, minute=59, second=59)
data_termino_4 = datetime.datetime(
    year=2027, month=6, day=23, hour=23, minute=59, second=59)

session.add_all([
    Local(nome="Club do AAAAAAA", endereço="Avenida Tom Carvalho, QD 25, LT 21, Rua da Amizade", capacidade_maxima=100),
    Local(nome="Club a fjd", endereço="Avenida americana, rua das flores, QD 33, LT 19", capacidade_maxima=10),
    Local(nome="Eventos da Dona Maria", endereço="Bairro flor do jardim, rua 21, QD 11, LT 88", capacidade_maxima=1000),
    Local(nome="Seu Zé Forró para idosos", endereço="Avenida Silva, bairro DDDDD, Rua 2, QD 93, LT 87", capacidade_maxima=200),
    Agendamento(nome_responsável="Paulo Ferreira da Silva", data_hora_inicio=data_inicio_1, data_hora_termino=data_termino_1, id_local=1),
    Agendamento(nome_responsável="José Martins", data_hora_inicio=data_inicio_2, data_hora_termino=data_termino_2, id_local=2),
    Agendamento(nome_responsável="Roberto Carlos", data_hora_inicio=data_inicio_3, data_hora_termino=data_termino_3, id_local=3),
    Agendamento(nome_responsável="Marcio José Arruda Filho", data_hora_inicio=data_inicio_4, data_hora_termino=data_inicio_4, id_local=4),
])
session.commit()
# //////////////////////// PARTE PARA INSERIR ////////////////////////