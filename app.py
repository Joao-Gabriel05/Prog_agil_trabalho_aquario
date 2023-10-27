from flask import Flask, request, jsonify
from Mongo import Mongo
from pass_functions import *
import bson

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
                return {"sucesso":"usuario autenticado"}, 200
        else:
            return {"erro":"email ou senha incorretos"}, 400
    except Exception as e:
        return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500
    
@app.route('/usuarios', methods=['POST'])
def cadastrar_user():
    data = request.json

    if all(key not in data for key in ['nome','email','senha']) or all(not value.strip() or type(value) != str  for value in data.values()):
        return {"erro": "informaçoes faltando"}
    
    if usuarios.existe({"email":data["email"]}):
        return {"erro":"email ja cadastrado"}

    try:
        data["senha"] = criar_senha_criptografada(data["senha"])
        usuarios.create_document(data)
        return {"sucesso": "usuario criado com sucesso"}, 201
    except Exception as e:
        return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500
    
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

@app.route('/usuarios/<usuario_id>', methods=['PUT'])
def update_usuario(usuario_id):
    if usuarios.existe({"_id":bson.ObjectId(usuario_id)}):
        data = request.json

        if all(not value.strip() or type(value) != str  for value in data.values()):
            return {"error": "Dado para atualização não fornecido!"}, 400
        
        try:
            if "senha" in data:
                data["senha"] = criar_senha_criptografada(data["senha"])
            usuarios.update_document({"_id": bson.ObjectId(usuario_id)}, {"$set": data})
            return {"sucesso": f"Usuario {usuario_id} atualizado com sucesso!"}, 200
        except Exception as e:
             return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500
    
    return {"erro": "id não encontrado"}, 404

if __name__ == '__main__':
    app.run(debug=True)