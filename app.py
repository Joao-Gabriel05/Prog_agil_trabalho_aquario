from flask import Flask, request
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

if __name__ == '__main__':
    app.run(debug=True)