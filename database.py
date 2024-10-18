import psycopg2
from datetime import datetime

class Database:
    def __init__(self):
        self.conexao = self.conectar_db()
        self.criar_tabelas()  # Certifique-se de que as tabelas são criadas ao iniciar

    def conectar_db(self):
        try:
            conexao = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="boot",
                host="localhost",
                port="5432"
            )
            print("Conexão ao banco de dados estabelecida com sucesso.")
            return conexao
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def criar_tabelas(self):
        with self.conexao.cursor() as cursor:
            cursor.execute("SET search_path TO clinica;")
            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS medico (
                    id_medico SERIAL PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    crm VARCHAR(20) NOT NULL UNIQUE,
                    id_especialidade INT REFERENCES especialidade(id_especialidade),
                    id_clinica INT REFERENCES clinica(id_clinica)
                );
            """)
            cursor.execute(""" 
                CREATE TABLE IF NOT EXISTS agendamento (
                    id_agendamento SERIAL PRIMARY KEY,
                    data_horario TIMESTAMP NOT NULL,
                    tipo_consulta VARCHAR(50),
                    status VARCHAR(20),
                    id_medico INT REFERENCES medico(id_medico),
                    id_paciente INT REFERENCES paciente(id_paciente)
                );
            """)
            self.conexao.commit()
            print("Tabelas criadas com sucesso.")

    def adicionar_medico(self, nome, crm, id_especialidade, id_clinica):
        if not nome or not crm or not id_especialidade or not id_clinica:
            print("Todos os campos são obrigatórios.")
            return

        with self.conexao.cursor() as cursor:
            try:
                cursor.execute("SET search_path TO clinica;")
                cursor.execute(""" 
                    INSERT INTO medico (nome, crm, id_especialidade, id_clinica) 
                    VALUES (%s, %s, %s, %s);
                """, (nome, crm, id_especialidade, id_clinica))

                self.conexao.commit()
                print("Médico cadastrado com sucesso!")
            except psycopg2.IntegrityError as e:
                self.conexao.rollback()  
                print(f"Erro de integridade: {e} - O CRM deve ser único.")
            except psycopg2.Error as e:
                self.conexao.rollback()  
                print(f"Erro ao adicionar médico: {e}")

    def fechar_conexao(self):
        if self.conexao:
            self.conexao.close()
            print("Conexão com o banco de dados fechada.")

    def listar_medicos(self):
        with self.conexao.cursor() as cursor:
            cursor.execute("SET search_path TO clinica;")
            cursor.execute("SELECT * FROM medico;")
            return cursor.fetchall()

    def excluir_medico(self, crm):
        with self.conexao.cursor() as cursor:
            cursor.execute("SET search_path TO clinica;")
            cursor.execute("DELETE FROM medico WHERE crm = %s;", (crm,))
            if cursor.rowcount > 0:
                self.conexao.commit()
                print("Médico excluído com sucesso!")
            else:
                print("Nenhum médico encontrado com esse CRM.")

    def marcar_consulta(self, data_horario, tipo_consulta, status, id_medico, id_paciente):
        with self.conexao.cursor() as cursor:
            cursor.execute("SET search_path TO clinica;")
            try:
                cursor.execute(""" 
                    INSERT INTO agendamento (data_horario, tipo_consulta, status, id_medico, id_paciente) 
                    VALUES (%s, %s, %s, %s, %s);
                """, (data_horario, tipo_consulta, status, id_medico, id_paciente))
                self.conexao.commit()
                print("Consulta marcada com sucesso!")
            except Exception as e:
                print(f"Erro ao marcar consulta: {e}")

class Usuario:
    def __init__(self, nome, usuario, tipo):
        self.nome = nome
        self.usuario = usuario
        self.tipo = tipo

    def validar(self, nome_usuario, senha):
        return self.usuario == nome_usuario and self.senha == senha

def obter_escolha_usuario(mensagem, min_opcao, max_opcao):
    while True:
        try:
            escolha = int(input(mensagem))
            if min_opcao <= escolha <= max_opcao:
                return escolha
            else:
                print(f"Por favor, escolha uma opção entre {min_opcao} e {max_opcao}.")
        except ValueError:
            print("Entrada inválida. Tente novamente.")

def exibir_menu_admin():
    print("\nBem-vindo ao Menu Administrador")
    print("1. Cadastrar Médico")
    print("2. Listar Médicos")
    print("3. Excluir Médico")
    print("4. Sair")
    return obter_escolha_usuario("Escolha uma opção: ", 1, 4)

def exibir_menu_paciente():
    print("\nBem-vindo ao Menu Paciente")
    print("1. Marcar Consulta")
    print("2. Sair")
    return obter_escolha_usuario("Escolha uma opção: ", 1, 2)

def cadastrar_medico(database):
    nome = input("Nome do médico: ")
    crm = input("CRM: ")
    id_especialidade = input("ID da especialidade: ")
    id_clinica = input("ID da clínica: ")
    database.adicionar_medico(nome, crm, id_especialidade, id_clinica)

def listar_medicos(database):
    print("\nMédicos Disponíveis:")
    medicos = database.listar_medicos()
    for medico in medicos:
        print(f"ID: {medico[0]}, Nome: {medico[1]}, CRM: {medico[2]}, ID Especialidade: {medico[3]}, ID Clínica: {medico[4]}")

def excluir_medico(database):
    crm = input("Digite o CRM do médico que deseja excluir: ")
    database.excluir_medico(crm)

def marcar_consulta(database):
    print("Para marcar uma consulta:")
    data_horario = input("Digite a data e hora da consulta (YYYY-MM-DD HH:MM): ")
    tipo_consulta = input("Digite o tipo de consulta: ")
    status = "Agendado"
    
    listar_medicos(database)
    id_medico = input("Digite o ID do médico: ")
    id_paciente = input("Digite o ID do paciente: ")
    
    database.marcar_consulta(data_horario, tipo_consulta, status, id_medico, id_paciente)

def main():
    database = Database()
    
    usuario_admin = Usuario("admin", "usuario_admin", "admin")
    usuario_paciente = Usuario("paciente", "usuario_paciente", "comum")

    nome_usuario = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")

    if usuario_admin.validar(nome_usuario, senha):
        print("Bem-vindo, administrador!")
        while True:
            escolha = exibir_menu_admin()
            if escolha == 1:
                cadastrar_medico(database)
            elif escolha == 2:
                listar_medicos(database)
            elif escolha == 3:
                excluir_medico(database)
            elif escolha == 4:
                print("Saindo do sistema. Obrigado!")
                break
    elif usuario_paciente.validar(nome_usuario, senha):
        print("Bem-vindo, paciente!")
        while True:
            escolha = exibir_menu_paciente()
            if escolha == 1:
                marcar_consulta(database)
            elif escolha == 2:
                print("Saindo do sistema. Obrigado!")
                break
    else:
        print("Credenciais inválidas. Acesso negado.")

    database.fechar_conexao()

if __name__ == "__main__":
    main()
