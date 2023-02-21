from flask import Flask, make_response, jsonify, request
from flask_restful import Api, Resource
from flask_httpauth import HTTPBasicAuth

import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

import datetime
from datetime import datetime

engine = sqlalchemy.create_engine('sqlite:///db.db')
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

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False # para deixar em ordem alfabetica
auth = HTTPBasicAuth()

USER_DATA = {
    "admin": "senha1234"
}

@auth.verify_password
def verify(username, password):
    if not(username, password):
        return False
    return USER_DATA.get(username) == password


@app.route('/local', methods=['GET'])
@auth.login_required
def get_todos_locais():
    """ Devolve a lista com todos os Locais. """

    Session = sessionmaker(bind=engine)
    session = Session()

    locais = []
    for i in session.query(Local).order_by(Local.id):
        local = {
            "id": i.id, "nome": i.nome, 
            "endereço":i.endereço, "capacidade_maxima": i.capacidade_maxima
        }
        locais.append(local)
    
    return make_response(
        jsonify(
            message="Lista com todos os locais",
            data=locais
        )
    )

@app.route('/agendamento', methods=['GET'])
@auth.login_required
def get_todos_agendamentos():
    """ Devolve a lista com todos os Agendamentos. """

    Session = sessionmaker(bind=engine)
    session = Session()

    agendamentos = []
    for i in session.query(Agendamento).order_by(Agendamento.id):
        agendamento = {
            "id": i.id, "nome_responsável": i.nome_responsável, 
            "data_hora_inicio":i.data_hora_inicio, "data_hora_termino": i.data_hora_termino,
            "id_local": i.id_local
        }
        agendamentos.append(agendamento)
    
    return make_response(
        jsonify(
            message="Lista com todos os agendamentos",
            data=agendamentos
        )
    )

@app.route('/local', methods=['POST'])
@auth.login_required
def post_local():
    """ Insere um local """
    Session = sessionmaker(bind=engine)
    session = Session()

    local_json = request.json

    local_database = Local(
        id=local_json['id'], nome=local_json['nome'],
        endereço=local_json['endereço'], capacidade_maxima=local_json['capacidade_maxima'])

    session.add(local_database)
    session.commit()
    
    return make_response(
        jsonify(
            message="Local inserido com sucesso",
            data=local_json
        )
    )

@app.route('/agendamento', methods=['POST'])
@auth.login_required
def post_agendamento():
    """ Insere um agendamento """
    Session = sessionmaker(bind=engine)
    session = Session()

    agendamento_json = request.json
    
    # As horas ficam salvas em JSON como strings, mas o banco de dados...
    # as recebe somente como datetime, por isso tenho que converter:
    datetime_hora_inicio = datetime.strptime(
        agendamento_json['data_hora_inicio'], '%Y-%m-%d %H:%M:%S.%f'
    )
    datetime_hora_termino = datetime.strptime(
        agendamento_json['data_hora_termino'], '%Y-%m-%d %H:%M:%S.%f'
    )

    agendamento_database = Agendamento(
        id=agendamento_json['id'], nome_responsável=agendamento_json['nome_responsável'],
        data_hora_inicio=datetime_hora_inicio, data_hora_termino=datetime_hora_termino,
        id_local=agendamento_json['id_local'])

    session.add(agendamento_database)
    session.commit()

    return make_response(
        jsonify(
            message="Agendamento inserido com sucesso",
            data=agendamento_json
        )
    )

@app.route('/local', methods=['DELETE'])
@auth.login_required
def deletar_locais():
    """ Deleta todos os locais """
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Local).delete()

    session.commit()
    
    return make_response(
        jsonify(
            message="Todos os locais foram deletados",
            data={"resultado": "sucesso em deletar todos os locais"}
        )
    )

@app.route('/agendamento', methods=['DELETE'])
@auth.login_required
def deletar_agendamentos():
    """ Deleta todos os agendamentos """
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Agendamento).delete()

    session.commit()
    
    return make_response(
        jsonify(
            message="Todos os agendamentos foram deletados",
            data={"resultado": "sucesso em deletar todos os agendamentos"}
        )
    )


class Local_by_id(Resource):
    @auth.login_required
    def get(self, id):
        """ Pega um local por id """
        Session = sessionmaker(bind=engine)
        session = Session()
        
        local_by_id = session.query(Local).filter_by(id=id).first()
        
        local_json = {
            "id": local_by_id.id, "nome": local_by_id.nome, 
            "endereço":local_by_id.endereço, "capacidade_maxima": local_by_id.capacidade_maxima
        }

        return make_response(
            jsonify(
                message="Visualizando um local de acordo com o id",
                data=local_json
            )
        )
    @auth.login_required
    def delete(self, id):
        """ Deleta um local por id """
        Session = sessionmaker(bind=engine)
        session = Session()

        local = session.query(Local).filter_by(id=id).first()
        session.delete(local)

        session.commit()
        
        return make_response(
            jsonify(
                message="Deletou um local de acordo com o id",
                data={"resultado": "sucesso em deletar um local"}
            )
        )
    @auth.login_required
    def put(self, id):
        """ Modifica um local por id """
        Session = sessionmaker(bind=engine)
        session = Session()

        local_original = session.query(Local).filter_by(id=id).first()

        local_json = request.json

        local_original.nome = local_json['nome']
        local_original.endereço = local_json['endereço']
        local_original.capacidade_maxima=local_json['capacidade_maxima']

        session.commit()
        
        return make_response(
            jsonify(
                message="Modificou um local de acordo com o id",
                data={"resultado": "sucesso em modificar um local"}
            )
        )
api.add_resource(Local_by_id, "/local/<int:id>")

class Agendamento_by_id(Resource):
    @auth.login_required
    def get(self, id):
        """ Pega um agendamento por id """
        Session = sessionmaker(bind=engine)
        session = Session()
        
        agendamento_by_id = session.query(Agendamento).filter_by(id=id).first()
        
        agendamento_json = {
            "id": agendamento_by_id.id,
            "nome_responsável": agendamento_by_id.nome_responsável, 
            "data_hora_inicio":agendamento_by_id.data_hora_inicio,
            "data_hora_termino": agendamento_by_id.data_hora_termino,
            "id_local": agendamento_by_id.id_local
        }
        
        return make_response(
            jsonify(
                message="Visualizando um agendamento de acordo com o id",
                data=agendamento_json
            )
        )
    @auth.login_required
    def delete(self, id):
        """ Deleta um agendamento por id """
        Session = sessionmaker(bind=engine)
        session = Session()

        agendamento = session.query(Agendamento).filter_by(id=id).first()
        session.delete(agendamento)

        session.commit()
        
        return make_response(
            jsonify(
                message="Deletou um agendamento de acordo com o id",
                data={"resultado": "sucesso em deletar um agendamento"} 
            )
        )
    @auth.login_required
    def put(self, id):
        """ Modifica um agendamento por id """
        Session = sessionmaker(bind=engine)
        session = Session()

        agendamento_original = session.query(Agendamento).filter_by(id=id).first()

        agendamento_json = request.json

        datetime_hora_inicio = datetime.strptime(
            agendamento_json['data_hora_inicio'], '%Y-%m-%d %H:%M:%S.%f')
        
        datetime_hora_termino = datetime.strptime(
            agendamento_json['data_hora_termino'], '%Y-%m-%d %H:%M:%S.%f')
        
        agendamento_original.nome_responsável = agendamento_json['nome_responsável']
        agendamento_original.data_hora_inicio = datetime_hora_inicio
        agendamento_original.data_hora_termino = datetime_hora_termino
        agendamento_original.id_local = agendamento_json['id_local']

        session.commit()
        
        return make_response(
            jsonify(
                message="Modificou um agendamento de acordo com o id",
                data={"resultado": "sucesso em modificar um agendamento"}
            )
        )
api.add_resource(Agendamento_by_id, "/agendamento/<int:id>")

class Local_query(Resource):
    @auth.login_required
    def get(self):
        """ Busca um local por (id,nome,endereço ou capacidade máxima) """
        Session = sessionmaker(bind=engine)
        session = Session()

        args = request.args
        if "id" in args.keys():
            local_filter = session.query(Local).filter_by(id=args['id'])
        elif "nome" in args.keys():
            local_filter = session.query(Local).filter_by(nome=args['nome'])
        elif "endereço" in args.keys():
            local_filter = session.query(Local).filter_by(endereço=args['endereço'])
        elif "capacidade_maxima" in args.keys():
            local_filter = session.query(Local).filter_by(capacidade_maxima=args['capacidade_maxima'])

        # se agendamento_filter não existir, é class NoneType
        if local_filter != None:
            # if se for possivel iterar.
            if str(type(local_filter)) == "<class 'sqlalchemy.orm.query.Query'>":
                array_elementos_filtrados = []
                for i in local_filter:
                    local_filter_json = {
                        "id": i.id,
                        "nome": i.nome,
                        "endereço": i.endereço,
                        "capacidade_maxima": i.capacidade_maxima}
                    array_elementos_filtrados.append(local_filter_json)
                return make_response(
                    jsonify(
                    message="Sucesso, Varios elementos foram encontrados de acordo com a query",    
                    data=array_elementos_filtrados
                    )
                )

            # if se não for possivel iterar.
            if str(type(local_filter)) == "<class '__main__.Local'>":
                array_elementos_filtrados = []
                local_filter_json = {
                    "id": local_filter.id,
                    "nome": local_filter.nome,
                    "endereço": local_filter.endereço,
                    "capacidade_maxima": local_filter.capacidade_maxima}
                array_elementos_filtrados.append(local_filter_json)
                return make_response(
                    jsonify(
                    message="Sucesso, um elemento foi encontrado de acordo com a query",    
                    data=array_elementos_filtrados
                    )
                )
        elif local_filter == None:
            array_elementos_filtrados = {}
            return make_response(
                    jsonify(
                    message="Nenhum elemento foi encontrado de acordo com a query",    
                    data=array_elementos_filtrados
                    )
                )
api.add_resource(Local_query, "/local/")

class Agendamento_query(Resource):
    @auth.login_required
    def get(self):
        """ 
        Busca um agendamento por (id,nome do responsável,data e hora de
        inicio, data e hora de termino ou id do local).
        """
        Session = sessionmaker(bind=engine)
        session = Session()

        args = request.args
        if "id" in args.keys():
            agendamento_filter = session.query(Agendamento).filter_by(id=args['id'])
        elif "nome_responsável" in args.keys():
            agendamento_filter = session.query(Agendamento).filter_by(nome_responsável=args['nome_responsável'])
        elif "data_hora_inicio" in args.keys():
            agendamento_filter = session.query(Agendamento).filter_by(data_hora_inicio=args["data_hora_inicio"])
        elif "data_hora_termino" in args.keys():
            agendamento_filter = session.query(Agendamento).filter_by(data_hora_termino=args['data_hora_termino'])
        elif "id_local" in args.keys():
            agendamento_filter = session.query(Agendamento).filter_by(id_local=args['id_local'])

        # se agendamento_filter não existir, é class NoneType
        if agendamento_filter != None:
            # if se for possivel iterar.
            if str(type(agendamento_filter)) == "<class 'sqlalchemy.orm.query.Query'>":
                array_elementos_filtrados = []
                for i in agendamento_filter:
                    agendamento_filter_json = {
                        "id": i.id,
                        "nome_responsável": i.nome_responsável,
                        "data_hora_inicio": i.data_hora_inicio,
                        "data_hora_termino": i.data_hora_termino,
                        "id_local": i.id_local}
                    array_elementos_filtrados.append(agendamento_filter_json)
                return make_response(
                    jsonify(
                    message="Sucesso, Varios elementos foram encontrados de acordo com a query",    
                    data=array_elementos_filtrados
                    )
                )

            # if se não for possivel iterar.
            if str(type(agendamento_filter)) == "<class '__main__.Agendamento'>":
                array_elementos_filtrados = []
                agendamento_filter_json = {
                    "id": agendamento_filter.id,
                    "nome_responsável": agendamento_filter.nome_responsável,
                    "data_hora_inicio": agendamento_filter.data_hora_inicio,
                    "data_hora_termino": agendamento_filter.data_hora_termino,
                    "id_local": agendamento_filter.id_local}
                array_elementos_filtrados.append(agendamento_filter_json)
                return make_response(
                    jsonify(
                    message="Sucesso, um elemento foi encontrado de acordo com a query",    
                    data=array_elementos_filtrados
                    )
                )
        elif agendamento_filter == None:
            array_elementos_filtrados = {}
            return make_response(
                    jsonify(
                    message="Nenhum elemento foi encontrado de acordo com a query",    
                    data=array_elementos_filtrados
                    )
                )
api.add_resource(Agendamento_query, "/agendamento/")

if __name__ == "__main__":
    app.run()