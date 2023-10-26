from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from Mongo import Mongo

app = Flask(__name__)

usuarios = Mongo('mongodb+srv://admin:admin@cluster0.zpeilug.mongodb.net/','prog_eficaz','usuarios')
aquarios = Mongo('mongodb+srv://admin:admin@cluster0.zpeilug.mongodb.net/','prog_eficaz','aquarios')

@app.route('/login', methods=['POST'])
def login():
    data = request.json

    try:
        if usuarios.existe(data):
            return {"sucesso":"usuario autenticado"}, 200
        else:
            return {"erro":"email ou senha incorretos"}, 400
    except Exception as e:
        return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500
    
@app.route('/usuarios', methods=['POST'])
def cadastrar():
    data = request.json

    if all(key not in data for key in ['nome','email','senha']) or all(not value.strip() or type(value) != str  for value in data.values()):
        return {"erro": "informaçoes faltando"}
    
    if usuarios.existe({"email":data["email"]}):
        return {"erro":"email ja cadastrado"}

    try:
        if usuarios.existe(data):
            return {"sucesso":"usuario autenticado"}, 200
        else:
            return {"erro":"email ou senha incorretos"}, 400
    except Exception as e:
        return {"erro":"Desculpe tivemos um problema interno, tente novamente mais tarde. Detalhes: {}".format(str(e))}, 500

@app.route('/usuarios/<usuario_id>', methods=['PUT'])
def update_usuario(usuario_id):
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Dado para atualização não fornecido!"}), 400
        usuarios.db.usuarios.update_one({"_id": ObjectId(usuario_id)}, {"$set": data})
        return jsonify({"message": f"Usuario {usuario_id} atualizado com sucesso!"}), 200
    except Exception as e:
        return {"erro":str(e)}, 500

@app.route('/usuarios/<usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
    try:
        usuario = usuarios.db.usuarios.find_one({"_id": ObjectId(usuario_id)})
        if usuario:
            usuario["_id"] = str(usuario["_id"])
            return usuario, 200
        return jsonify({"erro": "Usuario não encontrado!"}), 404
    except Exception as e:
        return {"erro":str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)