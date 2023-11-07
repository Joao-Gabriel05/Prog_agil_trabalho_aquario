from flask import Flask, request, jsonify
from Mongo import Mongo
from pass_functions import *
import bson
from datetime import datetime

app = Flask(__name__)

usuarios = Mongo('mongodb+srv://admin:admin@cluster0.zpeilug.mongodb.net/','prog_eficaz','usuarios')
aquarios = Mongo('mongodb+srv://admin:admin@cluster0.zpeilug.mongodb.net/','prog_eficaz','aquarios')

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    try:
        if usuarios.existe({"email":data['email']}):
            user = usuarios.read_document_one({"email":data['email']})
            if verificar_senha(data["senha"], user["senha"]):
                return {"sucesso":user['_id']}, 200
        else:
            return {"erro":"email ou senha incorretos"}, 400
    except Exception as e:
        return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500
    
@app.route('/usuarios/<usuario_id>', methods=['GET'])
def ler_usuario_id(usuario_id):
    if usuarios.existe({"_id": bson.ObjectId(usuario_id)}):
        try:
            user = usuarios.read_document_one({"_id":bson.ObjectId(usuario_id)})
            user['senha'] = str(user['senha'])
            return {"usuario": user}, 200
        except Exception as e:
            return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500
        
    return {"erro": "id não encontrado"}, 404

@app.route('/usuarios', methods=['POST'])
def cadastrar_user():
    data = request.json

    if all(key not in data for key in ['nome','email','senha']) or all(not value.strip() or type(value) != str  for value in data.values()):
        return {"erro": "informaçoes faltando"}
    
    if usuarios.existe({"email":data["email"]}):
        return {"erro":"email ja cadastrado"}

    try:
        data["senha"] = criar_senha_criptografada(data["senha"])
        user = usuarios.create_document(data)
        return {"sucesso": user['_id']}, 201
    except Exception as e:
        return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500

@app.route('/usuarios/<usuario_id>', methods=['PUT'])
def update_user(usuario_id):
    if usuarios.existe({"_id":bson.ObjectId(usuario_id)}):
        data = request.json

        if all(not value.strip() or type(value) != str  for value in data.values()):
            return {"erro": "Dado para atualização não fornecido!"}, 400
        
        try:
            if "senha" in data:
                data["senha"] = criar_senha_criptografada(data["senha"])
            usuarios.update_document({"_id": bson.ObjectId(usuario_id)}, data)
            return {"sucesso": f"Usuario {usuario_id} atualizado com sucesso!"}, 200
        except Exception as e:
            return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500
    
    return {"erro": "id não encontrado"}, 404


@app.route('/usuarios/<usuario_id>', methods=['DELETE'])
def delete_user(usuario_id,agendar):
    if usuarios.existe({"_id":bson.ObjectId(usuario_id)}):
        try:
            usuarios.delete_document({"_id":bson.ObjectId(usuario_id)})
            return {"sucesso": f"Usuario deletado com sucesso"}, 200
        except Exception as e:
            return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500
    
    return {"erro": "id não encontrado"}, 404

#AQUARIOS

@app.route('/aquarios', methods=['GET'])
def ler_aquarios():

    try:
        return {"aquarios": aquarios.read_document_all()}, 200
    except Exception as e:
        return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500
    
@app.route('/aquarios/<aquario_id>', methods=['GET'])
def ler_aquario_id(aquario_id):
    if aquarios.existe({"_id": bson.ObjectId(aquario_id)}):
        try:
            return {"aquario": aquarios.read_document_one({"_id":bson.ObjectId(aquario_id)})}, 200
        except Exception as e:
            return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500
        
    return {"erro": "id não encontrado"}, 404
    
@app.route('/aquarios', methods=['POST'])
def cadastrar_aquario():
    data = request.json

    if all(key not in data for key in ['nome','local']) or all(not value.strip() or type(value) != str  for value in data.values()):
        return {"erro": "informaçoes faltando"}
    
    if aquarios.existe({"nome":data["nome"]}):
        return {"erro":"aquario ja cadastrado"}

    try:
        aquarios.create_document(data)
        return {"sucesso": "aquario criado com sucesso"}, 201
    except Exception as e:
        return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500
    
@app.route('/aquarios/<aquario_id>', methods=['PUT'])
def update_aquario(aquario_id):
    if aquarios.existe({"_id":bson.ObjectId(aquario_id)}):
        data = request.json

        if all(not value.strip() or type(value) != str  for value in data.values()):
            return {"erro": "Dado para atualização não fornecido!"}, 400
        
        try:
            aquarios.update_document({"_id": bson.ObjectId(aquario_id)}, data)
            return {"sucesso": f"aquario {aquario_id} atualizado com sucesso!"}, 200
        except Exception as e:
            return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500
    
    return {"erro": "id não encontrado"}, 404

@app.route('/aquarios/<aquario_id>', methods=['DELETE'])
def delete_aquario(aquario_id):
    if aquarios.existe({"_id":bson.ObjectId(aquario_id)}):
        try:
            aquarios.delete_document({"_id":bson.ObjectId(aquario_id)})
            return {"sucesso": f"aquario deletado com sucesso"}, 200
        except Exception as e:
            return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500
    
    return {"erro": "id não encontrado"}, 404

#AGENDAMENTOS
def verifica_horario(entrada_horario):
        
    data, hora = entrada_horario.split('-')
    data_desejada = datetime.strptime(data, "%d/%m/%Y").date()
    data_atual = datetime.now().date()
    if data_desejada < data_atual:
        return True
        
    elif data_desejada == data_atual:
        hora_desejada = datetime.strptime(hora, "%H_%M").time()
        hora_atual = datetime.now().time()
        if hora_desejada <= hora_atual:
            return True
    return False

@app.route('/verifica_agendamentos', methods=['GET'])
def verifica_agendamento_expirou():
    try:
        users = usuarios.read_document_all()
        for user in users:
            if 'agendamentos' in user:
                for agendamento in user['agendamentos']:
                    if verifica_horario(agendamento['agendamento']):
                        deletar_agendamento(user['_id'],agendamento['aquario']['_id'],agendamento)
        return {"sucesso":"chekou todos os agendamnetos"},200
    except Exception as e:
            return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500

def verifica_agendamento_valido(tentativa_agendamento):
    users = usuarios.read_document_all()
    for user in users:
        if 'agendamentos' in user:
            for agendamento in user['agendamentos']:
                if agendamento['agendamento'] == tentativa_agendamento:
                    return False
    return True

@app.route('/agendamentos/usuario/<usuario_id>/aquario/<aquario_id>', methods=['POST'])
def cadastrar_agendamento(usuario_id,aquario_id):
    '''
    espera um documento json seguindo o exemplo a seguir:
    {
    "agendamento": "21/11/2023-20_21"
    }
    '''
    if aquarios.existe({"_id":bson.ObjectId(aquario_id)}) and usuarios.existe({"_id":bson.ObjectId(usuario_id)}):
        data_aquario = request.json[:]
        data_user = request.json[:]

        if all(not value.strip() or type(value) != str  for value in data_aquario.values()) and all(not value.strip() or type(value) != str  for value in data_user.values()):
            return {"erro": "Dado para atualização não fornecido!"}, 400
        
        if not verifica_agendamento_valido(data_user):
            return {"erro": "Horario indisponivel"}, 400
        
        if verifica_horario(data_user['agendamento']):
            return {"erro": "Horario indisponivel"}, 400

        try:
            aquario = aquarios.read_document_one({"_id": bson.ObjectId(aquario_id)})
            user = usuarios.read_document_one({"_id":bson.ObjectId(usuario_id)})

            if 'agendamentos' not in aquario:
                aquario["agendamentos"] = []
            if 'agendamentos' not in user:
                user["agendamentos"] = []

            aquario["agendamentos"].append(data_aquario)
            data_user["aquario"] = {"_id":aquario["_id"],"nome": aquario["nome"],"local": aquario["local"]}
            user["agendamentos"].append(data_user)

            del user["_id"]
            del aquario["_id"]
            
            aquarios.update_document({"_id": bson.ObjectId(aquario_id)}, aquario)
            usuarios.update_document({"_id": bson.ObjectId(usuario_id)}, user)

            return {"sucesso": "agendamento realizado"}, 200
        except Exception as e:
            return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500
    
    return {"erro": "id não encontrado"}, 404

@app.route('/agendamentos/usuario/<usuario_id>/aquario/<aquario_id>', methods=['DELETE'])
def deletar_agendamento(usuario_id, aquario_id):
    try:
        aquario = aquarios.read_document_one({"_id": bson.ObjectId(aquario_id)})
        user = usuarios.read_document_one({"_id":bson.ObjectId(usuario_id)})

        for agendamento in user['agendamentos']:
            if verifica_horario(agendamento['agendamento']):
                user['agendamentos'].remove(agendamento)
                del agendamento['aquario']
                aquario['agendamentos'].remove(agendamento)

                del user['_id']
                del aquario['_id']

                usuarios.update_document({"_id":bson.ObjectId(usuario_id)}, user)
                aquarios.update_document({"_id": bson.ObjectId(aquario_id)}, aquario)

        return {'sucesso': 'agendamento deletado'}, 200
    except Exception as e:
            return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500

# if __name__ == '__main__':
#     app.run(debug=True)