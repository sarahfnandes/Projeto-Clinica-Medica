from database import Database
from usuario import Usuario
from datetime import datetime

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

def cadastrar_medico(database):
    nome = input("Nome do médico: ")
    crm = input("CRM: ")
    id_especialidade = input("ID da especialidade: ")
    id_clinica = input("ID da clínica: ")
    
    database.adicionar_medico(nome, crm, id_especialidade, id_clinica)
    print("Médico cadastrado com sucesso!")

def listar_medicos(database):
    print("\nMédicos Disponíveis:")
    medicos = database.listar_medicos()
    for medico in medicos:
        print(f"ID: {medico[0]}, Nome: {medico[1]}, CRM: {medico[2]}, ID Especialidade: {medico[3]}, ID Clínica: {medico[4]}")

def excluir_medico(database):
    crm = input("Digite o CRM do médico que deseja excluir: ")
    database.excluir_medico(crm)
    print("Médico excluído com sucesso!")

def marcar_consulta(database):
    print("Para marcar uma consulta:")
    data_horario = input("Digite a data e hora da consulta (YYYY-MM-DD HH:MM): ")
    tipo_consulta = input("Digite o tipo de consulta: ")
    status = "Agendado" 
    
  
    listar_medicos(database)
    id_medico = input("Digite o ID do médico: ")
    
  
    id_paciente = input("Digite o ID do paciente: ") 
    
    database.marcar_consulta(data_horario, tipo_consulta, status, id_medico, id_paciente)
    print("Consulta marcada com sucesso!")

def main():
    database = Database()
    
   
    usuario_admin = Usuario("admin", "usuario_admin", "admin")
    usuario_paciente = Usuario("paciente", "usuario_paciente", "comum")


    nome_usuario = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")

    if usuario_admin.validar(nome_usuario, senha) or usuario_paciente.validar(nome_usuario, senha):
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
        else:
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

