class Usuario:
    def __init__(self, nome, senha, tipo='comum'):
        self.nome = nome
        self.senha = senha
        self.tipo = tipo 

    def validar(self, nome_usuario, senha):
        return self.nome == nome_usuario and self.senha == senha
