from database import Database

class Departamento:
    
    def __init__(self, nome=None, sigla=None, descricao=None, id=None):
        self.id = id
        self.nome = nome
        self.sigla = sigla
        self.descricao = descricao
        self.db = Database()
    
    def salvar(self):
        if self.id:
            return self.atualizar()
        else:
            return self.inserir()
    
    def inserir(self):
        query = """
        INSERT INTO departamento (nome, sigla, descricao)
        VALUES (%s, %s, %s)
        """
        params = (self.nome, self.sigla, self.descricao)
        
        return self.db.execute_query(query, params)
    
    def atualizar(self):
        query = """
        UPDATE departamento
        SET nome = %s, sigla = %s, descricao = %s
        WHERE id = %s
        """
        params = (self.nome, self.sigla, self.descricao, self.id)
        
        return self.db.execute_query(query, params)
    
    def excluir(self):
        if not self.id:
            return False
            
        query = "DELETE FROM departamento WHERE id = %s"
        params = (self.id,)
        
        return self.db.execute_query(query, params)
    
    @classmethod
    def buscar_por_id(cls, id):
        db = Database()
        query = "SELECT * FROM departamento WHERE id = %s"
        params = (id,)
        
        departamento_data = db.fetch_one(query, params)
        
        if departamento_data:
            return cls(
                nome=departamento_data['nome'],
                sigla=departamento_data['sigla'],
                descricao=departamento_data['descricao'],
                id=departamento_data['id']
            )
        return None
    
    @classmethod
    def buscar_por_sigla(cls, sigla):
        db = Database()
        query = "SELECT * FROM departamento WHERE sigla = %s"
        params = (sigla,)
        
        departamento_data = db.fetch_one(query, params)
        
        if departamento_data:
            return cls(
                nome=departamento_data['nome'],
                sigla=departamento_data['sigla'],
                descricao=departamento_data['descricao'],
                id=departamento_data['id']
            )
        return None
    
    @classmethod
    def listar_todos(cls):
        db = Database()
        query = "SELECT * FROM departamento ORDER BY nome"
        
        departamentos_data = db.fetch_all(query)
        departamentos = []
        
        if departamentos_data:
            for dept_data in departamentos_data:
                departamento = cls(
                    nome=dept_data['nome'],
                    sigla=dept_data['sigla'],
                    descricao=dept_data['descricao'],
                    id=dept_data['id']
                )
                departamentos.append(departamento)
                
        return departamentos
    
    def __str__(self):
        return f"{self.sigla} - {self.nome}"


if __name__ == "__main__":
    dept = Departamento(
        nome="Departamento de Ciência da Computação",
        sigla="DCC",
        descricao="Departamento responsável pelos cursos de computação"
    )
    if dept.salvar():
        print(f"Departamento {dept.nome} salvo com sucesso!")
    
    todos_departamentos = Departamento.listar_todos()
    print("\nDepartamentos cadastrados:")
    for d in todos_departamentos:
        print(d)