import bcrypt

# # Função para criar uma senha criptografada
def criar_senha_criptografada(senha_plana):
    # Crie uma senha criptografada automaticamente com um salt
    senha_criptografada = bcrypt.hashpw(senha_plana.encode('utf-8'), bcrypt.gensalt())
    return senha_criptografada

# Função para verificar uma senha em relação a uma senha criptografada
def verificar_senha(senha_plana, senha_criptografada):
    # Verifique se a senha criptografada corresponde à senha plana
    return bcrypt.checkpw(senha_plana.encode('utf-8'), senha_criptografada)


# # Exemplo de uso
# senha_plana = "minha_senha"
# senha_criptografada = criar_senha_criptografada(senha_plana)

# # Agora você pode armazenar a senha criptografada no banco de dados, por exemplo.

# # Para verificar a senha posteriormente
# senha_inserida = "minha_senha"  # Esta é a senha que o usuário insere
# if verificar_senha(senha_inserida, senha_criptografada):
#     print("Senha correta!")
# else:
#     print("Senha incorreta!")

# # hashed = bcrypt.hashpw("123xyz", bcrypt.gensalt())
# # print(hashed)