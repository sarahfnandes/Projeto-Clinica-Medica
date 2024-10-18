from consulta import Consulta

class Medico:
    def __init__(self, nome, crm, especialidade):
        self.nome = nome
        self.crm = crm
        self.especialidade = especialidade
        self.consultas = [[] for _ in range(5)]  

    def adicionar_consulta(self, dia, consulta):
        self.consultas[dia].append(consulta)

    def listar_consultas(self):
        return self.consultas
    
    

