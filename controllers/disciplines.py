from database import Database
from controllers.courses import Curso

class Disciplina:
    
    def __init__(self, nome=None, codigo=None, curso_id=None, carga_horaria=None, semestre=None, id=None):
        self.id = id
        self.nome = nome
        self.codigo = codigo
        self.curso_id = curso_id
        self.carga_horaria = carga_horaria
        self.semestre = semestre
        self.db = Database()
    
    def salvar(self):
        if self.id:
            return self.atualizar()
        else:
            return self.inserir()
    
    def inserir(self):
        query = """
        INSERT INTO disciplina (nome, codigo, curso_id, carga_horaria, semestre)
        VALUES (%s, %s, %s, %s, %s)
        """
        params = (self.nome, self.codigo, self.curso_id, self.carga_horaria, self.semestre)
        
        return self.db.execute_query(query, params)
    
    def atualizar(self):
        query = """
        UPDATE disciplina
        SET nome = %s, codigo = %s, curso_id = %s, carga_horaria = %s, semestre = %s
        WHERE id = %s
        """
        params = (self.nome, self.codigo, self.curso_id, self.carga_horaria, self.semestre, self.id)
        
        return self.db.execute_query(query, params)
    
    def excluir(self):
        if not self.id:
            return False
        
        db = Database()
        query_professor = "SELECT COUNT(*) as total FROM professor_disciplina WHERE disciplina_id = %s"
        params = (self.id,)
        
        result = db.fetch_one(query_professor, params)
        if result and result['total'] > 0:
            print(f"Não é possível excluir a disciplina pois existem {result['total']} professores associados a ela.")
            return False
        
        query_aluno = "SELECT COUNT(*) as total FROM matricula WHERE disciplina_id = %s"
        result = db.fetch_one(query_aluno, params)
        if result and result['total'] > 0:
            print(f"Não é possível excluir a disciplina pois existem {result['total']} alunos matriculados nela.")
            return False
        
        query = "DELETE FROM disciplina WHERE id = %s"
        
        return db.execute_query(query, params)
    
    def get_curso(self):
        if not self.curso_id:
            return None
        
        return Curso.buscar_por_id(self.curso_id)
    
    def tem_professores(self, semestre=None):
        if not self.id:
            return False
        
        query = """
        SELECT COUNT(*) as total
        FROM professor_disciplina
        WHERE disciplina_id = %s
        """
        params = (self.id,)
        
        if semestre:
            query += " AND semestre = %s"
            params = (self.id, semestre)
        
        db = Database()
        result = db.fetch_one(query, params)
        
        return result and result['total'] > 0
    
    def listar_professores(self, semestre=None):
        from controllers.teachers import Professor
        
        if not self.id:
            return []
        
        query = """
        SELECT p.*
        FROM professor p
        JOIN professor_disciplina pd ON p.id = pd.professor_id
        WHERE pd.disciplina_id = %s
        """
        params = (self.id,)
        
        if semestre:
            query += " AND pd.semestre = %s"
            params = (self.id, semestre)
            
        query += " ORDER BY p.nome"
        
        db = Database()
        professores_data = db.fetch_all(query, params)
        professores = []
        
        if professores_data:
            for prof_data in professores_data:
                professor = Professor(
                    nome=prof_data['nome'],
                    matricula=prof_data['matricula'],
                    email=prof_data['email'],
                    telefone=prof_data['telefone'],
                    departamento_id=prof_data['departamento_id'],
                    titulacao=prof_data['titulacao'],
                    id=prof_data['id']
                )
                professores.append(professor)
                
        return professores
    
    @classmethod
    def buscar_por_id(cls, id):
        db = Database()
        query = "SELECT * FROM disciplina WHERE id = %s"
        params = (id,)
        
        disciplina_data = db.fetch_one(query, params)
        
        if disciplina_data:
            return cls(
                nome=disciplina_data['nome'],
                codigo=disciplina_data['codigo'],
                curso_id=disciplina_data['curso_id'],
                carga_horaria=disciplina_data['carga_horaria'],
                semestre=disciplina_data['semestre'],
                id=disciplina_data['id']
            )
        return None
    
    @classmethod
    def buscar_por_codigo(cls, codigo):
        db = Database()
        query = "SELECT * FROM disciplina WHERE codigo = %s"
        params = (codigo,)
        
        disciplina_data = db.fetch_one(query, params)
        
        if disciplina_data:
            return cls(
                nome=disciplina_data['nome'],
                codigo=disciplina_data['codigo'],
                curso_id=disciplina_data['curso_id'],
                carga_horaria=disciplina_data['carga_horaria'],
                semestre=disciplina_data['semestre'],
                id=disciplina_data['id']
            )
        return None
    
    @classmethod
    def listar_todos(cls):
        db = Database()
        query = "SELECT * FROM disciplina ORDER BY nome"
        
        disciplinas_data = db.fetch_all(query)
        disciplinas = []
        
        if disciplinas_data:
            for disc_data in disciplinas_data:
                disciplina = cls(
                    nome=disc_data['nome'],
                    codigo=disc_data['codigo'],
                    curso_id=disc_data['curso_id'],
                    carga_horaria=disc_data['carga_horaria'],
                    semestre=disc_data['semestre'],
                    id=disc_data['id']
                )
                disciplinas.append(disciplina)
                
        return disciplinas
    
    @classmethod
    def listar_por_curso(cls, curso_id):
        db = Database()
        query = "SELECT * FROM disciplina WHERE curso_id = %s ORDER BY semestre, nome"
        params = (curso_id,)
        
        disciplinas_data = db.fetch_all(query, params)
        disciplinas = []
        
        if disciplinas_data:
            for disc_data in disciplinas_data:
                disciplina = cls(
                    nome=disc_data['nome'],
                    codigo=disc_data['codigo'],
                    curso_id=disc_data['curso_id'],
                    carga_horaria=disc_data['carga_horaria'],
                    semestre=disc_data['semestre'],
                    id=disc_data['id']
                )
                disciplinas.append(disciplina)
                
        return disciplinas
    
    def __str__(self):
        return f"{self.codigo} - {self.nome} ({self.carga_horaria}h, {self.semestre}º semestre)"