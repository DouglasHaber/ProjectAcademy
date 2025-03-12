from database import Database
from controllers.courses import Curso
from controllers.disciplines import Disciplina
from datetime import datetime

class Aluno:
    
    def __init__(self, nome=None, matricula=None, email=None, telefone=None, 
                 curso_id=None, data_ingresso=None, id=None):
        self.id = id
        self.nome = nome
        self.matricula = matricula
        self.email = email
        self.telefone = telefone
        self.curso_id = curso_id
        
        if isinstance(data_ingresso, str):
            self.data_ingresso = datetime.strptime(data_ingresso, '%Y-%m-%d').date()
        else:
            self.data_ingresso = data_ingresso
            
        self.db = Database()
    
    def salvar(self):
        if self.id:
            return self.atualizar()
        else:
            return self.inserir()
    
    def inserir(self):
        query = """
        INSERT INTO aluno (nome, matricula, email, telefone, curso_id, data_ingresso)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (self.nome, self.matricula, self.email, self.telefone, 
                 self.curso_id, self.data_ingresso)
        
        return self.db.execute_query(query, params)
    
    def atualizar(self):
        query = """
        UPDATE aluno
        SET nome = %s, matricula = %s, email = %s, telefone = %s, 
            curso_id = %s, data_ingresso = %s
        WHERE id = %s
        """
        params = (self.nome, self.matricula, self.email, self.telefone, 
                 self.curso_id, self.data_ingresso, self.id)
        
        return self.db.execute_query(query, params)
    
    def excluir(self):
        if not self.id:
            return False
            
        query = "DELETE FROM aluno WHERE id = %s"
        params = (self.id,)
        
        return self.db.execute_query(query, params)
    
    def matricular_em_disciplina(self, disciplina_id, semestre):
        if not self.id:
            return False
        
        query = """
        INSERT INTO matricula (aluno_id, disciplina_id, semestre, situacao)
        VALUES (%s, %s, %s, 'Matriculado')
        ON DUPLICATE KEY UPDATE situacao = 'Matriculado'
        """
        params = (self.id, disciplina_id, semestre)
        
        return self.db.execute_query(query, params)
    
    def cancelar_matricula(self, disciplina_id, semestre):
        if not self.id:
            return False
        
        query = """
        DELETE FROM matricula 
        WHERE aluno_id = %s AND disciplina_id = %s AND semestre = %s
        """
        params = (self.id, disciplina_id, semestre)
        
        return self.db.execute_query(query, params)
    
    def trancar_matricula(self, disciplina_id, semestre):
        if not self.id:
            return False
        
        query = """
        UPDATE matricula 
        SET situacao = 'Trancado'
        WHERE aluno_id = %s AND disciplina_id = %s AND semestre = %s
        """
        params = (self.id, disciplina_id, semestre)
        
        return self.db.execute_query(query, params)
    
    def registrar_nota(self, disciplina_id, semestre, nota):
        if not self.id:
            return False
        
        if nota < 0 or nota > 10:
            return False
            
        situacao = 'Aprovado' if nota >= 6 else 'Reprovado'
        
        query = """
        UPDATE matricula 
        SET nota = %s, situacao = %s
        WHERE aluno_id = %s AND disciplina_id = %s AND semestre = %s
        """
        params = (nota, situacao, self.id, disciplina_id, semestre)
        
        return self.db.execute_query(query, params)
    
    def listar_disciplinas(self, semestre=None):
        if not self.id:
            return []
        
        query = """
        SELECT d.*, m.semestre, m.nota, m.situacao
        FROM disciplina d
        JOIN matricula m ON d.id = m.disciplina_id
        WHERE m.aluno_id = %s
        """
        params = (self.id,)
        
        if semestre:
            query += " AND m.semestre = %s"
            params = (self.id, semestre)
            
        query += " ORDER BY m.semestre, d.nome"
        
        disciplinas_data = self.db.fetch_all(query, params)
        resultado = []
        
        if disciplinas_data:
            for disc_data in disciplinas_data:
                semestre_letivo = disc_data['semestre']
                nota = disc_data['nota']
                situacao = disc_data['situacao']
                
                disciplina = Disciplina(
                    nome=disc_data['nome'],
                    codigo=disc_data['codigo'],
                    curso_id=disc_data['curso_id'],
                    carga_horaria=disc_data['carga_horaria'],
                    semestre=disc_data['semestre'],
                    id=disc_data['id']
                )
                resultado.append((disciplina, semestre_letivo, nota, situacao))
                
        return resultado
    
    def get_curso(self):
        if not self.curso_id:
            return None
        
        return Curso.buscar_por_id(self.curso_id)
    
    def calcular_cr(self):
        if not self.id:
            return None
        
        query = """
        SELECT AVG(nota) as cr
        FROM matricula
        WHERE aluno_id = %s AND nota IS NOT NULL
        """
        params = (self.id,)
        
        resultado = self.db.fetch_one(query, params)
        
        if resultado and resultado['cr'] is not None:
            return round(resultado['cr'], 2)
        
        return None
    
    @classmethod
    def buscar_por_id(cls, id):
        db = Database()
        query = "SELECT * FROM aluno WHERE id = %s"
        params = (id,)
        
        aluno_data = db.fetch_one(query, params)
        
        if aluno_data:
            return cls(
                nome=aluno_data['nome'],
                matricula=aluno_data['matricula'],
                email=aluno_data['email'],
                telefone=aluno_data['telefone'],
                curso_id=aluno_data['curso_id'],
                data_ingresso=aluno_data['data_ingresso'],
                id=aluno_data['id']
            )
        return None
    
    @classmethod
    def buscar_por_matricula(cls, matricula):
        db = Database()
        query = "SELECT * FROM aluno WHERE matricula = %s"
        params = (matricula,)
        
        aluno_data = db.fetch_one(query, params)
        
        if aluno_data:
            return cls(
                nome=aluno_data['nome'],
                matricula=aluno_data['matricula'],
                email=aluno_data['email'],
                telefone=aluno_data['telefone'],
                curso_id=aluno_data['curso_id'],
                data_ingresso=aluno_data['data_ingresso'],
                id=aluno_data['id']
            )
        return None
    
    @classmethod
    def listar_todos(cls):
        db = Database()
        query = "SELECT * FROM aluno ORDER BY nome"
        
        alunos_data = db.fetch_all(query)
        alunos = []
        
        if alunos_data:
            for aluno_data in alunos_data:
                aluno = cls(
                    nome=aluno_data['nome'],
                    matricula=aluno_data['matricula'],
                    email=aluno_data['email'],
                    telefone=aluno_data['telefone'],
                    curso_id=aluno_data['curso_id'],
                    data_ingresso=aluno_data['data_ingresso'],
                    id=aluno_data['id']
                )
                alunos.append(aluno)
                
        return alunos
    
    @classmethod
    def listar_por_curso(cls, curso_id):
        db = Database()
        query = "SELECT * FROM aluno WHERE curso_id = %s ORDER BY nome"
        params = (curso_id,)
        
        alunos_data = db.fetch_all(query, params)
        alunos = []
        
        if alunos_data:
            for aluno_data in alunos_data:
                aluno = cls(
                    nome=aluno_data['nome'],
                    matricula=aluno_data['matricula'],
                    email=aluno_data['email'],
                    telefone=aluno_data['telefone'],
                    curso_id=aluno_data['curso_id'],
                    data_ingresso=aluno_data['data_ingresso'],
                    id=aluno_data['id']
                )
                alunos.append(aluno)
                
        return alunos
    
    @classmethod
    def buscar_por_disciplina(cls, disciplina_id, semestre=None):
        db = Database()
        query = """
        SELECT a.*
        FROM aluno a
        JOIN matricula m ON a.id = m.aluno_id
        WHERE m.disciplina_id = %s
        """
        params = (disciplina_id,)
        
        if semestre:
            query += " AND m.semestre = %s"
            params = (disciplina_id, semestre)
            
        query += " ORDER BY a.nome"
        
        alunos_data = db.fetch_all(query, params)
        alunos = []
        
        if alunos_data:
            for aluno_data in alunos_data:
                aluno = cls(
                    nome=aluno_data['nome'],
                    matricula=aluno_data['matricula'],
                    email=aluno_data['email'],
                    telefone=aluno_data['telefone'],
                    curso_id=aluno_data['curso_id'],
                    data_ingresso=aluno_data['data_ingresso'],
                    id=aluno_data['id']
                )
                alunos.append(aluno)
                
        return alunos
    
    def __str__(self):
        return f"{self.nome} (Matrícula: {self.matricula})"

if __name__ == "__main__":
    curso = Curso.buscar_por_id(1)
    if curso:
        aluno = Aluno(
            nome="Maria Souza",
            matricula="2023001",
            email="maria.souza@email.com",
            telefone="(11) 97654-3210",
            curso_id=curso.id,
            data_ingresso="2023-01-15"
        )
        if aluno.salvar():
            print(f"Aluno {aluno.nome} salvo com sucesso!")
        
        alunos = Aluno.listar_por_curso(curso.id)
        print(f"\nAlunos do curso {curso.nome}:")
        for a in alunos:
            print(a)