from database import Database
from controllers.departaments import Departamento

class Curso:
    
    def __init__(self, nome=None, codigo=None, departamento_id=None, duracao_semestres=None, id=None):
        self.id = id
        self.nome = nome
        self.codigo = codigo
        self.departamento_id = departamento_id
        self.duracao_semestres = duracao_semestres
        self.db = Database()
    
    def salvar(self):
        if self.id:
            return self.atualizar()
        else:
            return self.inserir()
    
    def inserir(self):
        query = """
        INSERT INTO curso (nome, codigo, departamento_id, duracao_semestres)
        VALUES (%s, %s, %s, %s)
        """
        params = (self.nome, self.codigo, self.departamento_id, self.duracao_semestres)
        
        return self.db.execute_query(query, params)
    
    def atualizar(self):
        query = """
        UPDATE curso
        SET nome = %s, codigo = %s, departamento_id = %s, duracao_semestres = %s
        WHERE id = %s
        """
        params = (self.nome, self.codigo, self.departamento_id, self.duracao_semestres, self.id)
        
        return self.db.execute_query(query, params)
    
    def excluir(self):
        if not self.id:
            return False
            
        query = "DELETE FROM curso WHERE id = %s"
        params = (self.id,)
        
        return self.db.execute_query(query, params)
    
    def get_departamento(self):
        if not self.departamento_id:
            return None
        
        return Departamento.buscar_por_id(self.departamento_id)
    
    @classmethod
    def buscar_por_id(cls, id):
        db = Database()
        query = "SELECT * FROM curso WHERE id = %s"
        params = (id,)
        
        curso_data = db.fetch_one(query, params)
        
        if curso_data:
            return cls(
                nome=curso_data['nome'],
                codigo=curso_data['codigo'],
                departamento_id=curso_data['departamento_id'],
                duracao_semestres=curso_data['duracao_semestres'],
                id=curso_data['id']
            )
        return None
    
    @classmethod
    def buscar_por_codigo(cls, codigo):
        db = Database()
        query = "SELECT * FROM curso WHERE codigo = %s"
        params = (codigo,)
        
        curso_data = db.fetch_one(query, params)
        
        if curso_data:
            return cls(
                nome=curso_data['nome'],
                codigo=curso_data['codigo'],
                departamento_id=curso_data['departamento_id'],
                duracao_semestres=curso_data['duracao_semestres'],
                id=curso_data['id']
            )
        return None
    
    @classmethod
    def listar_todos(cls):
        db = Database()
        query = "SELECT * FROM curso ORDER BY nome"
        
        cursos_data = db.fetch_all(query)
        cursos = []
        
        if cursos_data:
            for curso_data in cursos_data:
                curso = cls(
                    nome=curso_data['nome'],
                    codigo=curso_data['codigo'],
                    departamento_id=curso_data['departamento_id'],
                    duracao_semestres=curso_data['duracao_semestres'],
                    id=curso_data['id']
                )
                cursos.append(curso)
                
        return cursos
    
    @classmethod
    def listar_por_departamento(cls, departamento_id):
        db = Database()
        query = "SELECT * FROM curso WHERE departamento_id = %s ORDER BY nome"
        params = (departamento_id,)
        
        cursos_data = db.fetch_all(query, params)
        cursos = []
        
        if cursos_data:
            for curso_data in cursos_data:
                curso = cls(
                    nome=curso_data['nome'],
                    codigo=curso_data['codigo'],
                    departamento_id=curso_data['departamento_id'],
                    duracao_semestres=curso_data['duracao_semestres'],
                    id=curso_data['id']
                )
                cursos.append(curso)
                
        return cursos
    
    def __str__(self):
        return f"{self.codigo} - {self.nome} ({self.duracao_semestres} semestres)"

if __name__ == "__main__":
    dept = Departamento.buscar_por_sigla("DCC")
    if not dept:
        dept = Departamento(
            nome="Departamento de Ciência da Computação",
            sigla="DCC",
            descricao="Departamento responsável pelos cursos de computação"
        )
        dept.salvar()
        dept = Departamento.buscar_por_sigla("DCC")

    curso = Curso(
        nome="Ciência da Computação",
        codigo="BCC",
        departamento_id=dept.id,
        duracao_semestres=8
    )
    if curso.salvar():
        print(f"Curso {curso.nome} salvo com sucesso!")

    todos_cursos = Curso.listar_todos()
    print("\nCursos cadastrados:")
    for c in todos_cursos:
        dept = c.get_departamento()
        print(f"{c} - Departamento: {dept}")