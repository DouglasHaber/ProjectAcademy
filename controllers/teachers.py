from database import Database
from controllers.departaments import Departamento
from controllers.disciplines import Disciplina

class Professor:
    
    def __init__(self, nome=None, matricula=None, email=None, telefone=None, 
                 departamento_id=None, titulacao=None, id=None):
        self.id = id
        self.nome = nome
        self.matricula = matricula
        self.email = email
        self.telefone = telefone
        self.departamento_id = departamento_id
        self.titulacao = titulacao
        self.db = Database()
    
    def salvar(self):
        if self.id:
            return self.atualizar()
        else:
            return self.inserir()
    
    def inserir(self):
        query = """
        INSERT INTO professor (nome, matricula, email, telefone, departamento_id, titulacao)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (self.nome, self.matricula, self.email, self.telefone, 
                 self.departamento_id, self.titulacao)
        
        return self.db.execute_query(query, params)
    
    def atualizar(self):
        query = """
        UPDATE professor
        SET nome = %s, matricula = %s, email = %s, telefone = %s, 
            departamento_id = %s, titulacao = %s
        WHERE id = %s
        """
        params = (self.nome, self.matricula, self.email, self.telefone, 
                 self.departamento_id, self.titulacao, self.id)
        
        return self.db.execute_query(query, params)
    
    def excluir(self):
        if not self.id:
            return False
        
        db = Database()
        query_disciplinas = "SELECT COUNT(*) as total FROM professor_disciplina WHERE professor_id = %s"
        params = (self.id,)
        
        result = db.fetch_one(query_disciplinas, params)
        if result and result['total'] > 0:
            print(f"Não é possível excluir o professor pois existem {result['total']} disciplinas atribuídas a ele.")
            return False
        
        query = "DELETE FROM professor WHERE id = %s"
        
        return db.execute_query(query, params)
    
    def atribuir_disciplina(self, disciplina_id, semestre):
        if not self.id:
            return False
        
        query = """
        INSERT INTO professor_disciplina (professor_id, disciplina_id, semestre)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE professor_id = VALUES(professor_id)
        """
        params = (self.id, disciplina_id, semestre)
        
        return self.db.execute_query(query, params)
    
    def remover_disciplina(self, disciplina_id, semestre):
        if not self.id:
            return False
        
        query = """
        DELETE FROM professor_disciplina 
        WHERE professor_id = %s AND disciplina_id = %s AND semestre = %s
        """
        params = (self.id, disciplina_id, semestre)
        
        return self.db.execute_query(query, params)
    
    def esta_atribuido_a_disciplina(self, disciplina_id, semestre=None):
        if not self.id:
            return False
        
        query = """
        SELECT COUNT(*) as total
        FROM professor_disciplina
        WHERE professor_id = %s AND disciplina_id = %s
        """
        params = (self.id, disciplina_id)
        
        if semestre:
            query += " AND semestre = %s"
            params = (self.id, disciplina_id, semestre)
        
        db = Database()
        result = db.fetch_one(query, params)
        
        return result and result['total'] > 0
    
    def listar_disciplinas(self, semestre=None):
        if not self.id:
            return []
        
        query = """
        SELECT d.*, pd.semestre
        FROM disciplina d
        JOIN professor_disciplina pd ON d.id = pd.disciplina_id
        WHERE pd.professor_id = %s
        """
        params = (self.id,)
        
        if semestre:
            query += " AND pd.semestre = %s"
            params = (self.id, semestre)
            
        query += " ORDER BY pd.semestre, d.nome"
        
        disciplinas_data = self.db.fetch_all(query, params)
        resultado = []
        
        if disciplinas_data:
            for disc_data in disciplinas_data:
                semestre_letivo = disc_data['semestre']
                disciplina = Disciplina(
                    nome=disc_data['nome'],
                    codigo=disc_data['codigo'],
                    curso_id=disc_data['curso_id'],
                    carga_horaria=disc_data['carga_horaria'],
                    semestre=disc_data['semestre'],
                    id=disc_data['id']
                )
                resultado.append((disciplina, semestre_letivo))
                
        return resultado
    
    def get_departamento(self):
        if not self.departamento_id:
            return None
        
        return Departamento.buscar_por_id(self.departamento_id)
    
    @classmethod
    def buscar_por_id(cls, id):
        db = Database()
        query = "SELECT * FROM professor WHERE id = %s"
        params = (id,)
        
        professor_data = db.fetch_one(query, params)
        
        if professor_data:
            return cls(
                nome=professor_data['nome'],
                matricula=professor_data['matricula'],
                email=professor_data['email'],
                telefone=professor_data['telefone'],
                departamento_id=professor_data['departamento_id'],
                titulacao=professor_data['titulacao'],
                id=professor_data['id']
            )
        return None
    
    @classmethod
    def buscar_por_matricula(cls, matricula):
        db = Database()
        query = "SELECT * FROM professor WHERE matricula = %s"
        params = (matricula,)
        
        professor_data = db.fetch_one(query, params)
        
        if professor_data:
            return cls(
                nome=professor_data['nome'],
                matricula=professor_data['matricula'],
                email=professor_data['email'],
                telefone=professor_data['telefone'],
                departamento_id=professor_data['departamento_id'],
                titulacao=professor_data['titulacao'],
                id=professor_data['id']
            )
        return None
    
    @classmethod
    def listar_todos(cls):
        db = Database()
        query = "SELECT * FROM professor ORDER BY nome"
        
        professores_data = db.fetch_all(query)
        professores = []
        
        if professores_data:
            for prof_data in professores_data:
                professor = cls(
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
    def listar_por_departamento(cls, departamento_id):
        db = Database()
        query = "SELECT * FROM professor WHERE departamento_id = %s ORDER BY nome"
        params = (departamento_id,)
        
        professores_data = db.fetch_all(query, params)
        professores = []
        
        if professores_data:
            for prof_data in professores_data:
                professor = cls(
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
    def buscar_por_disciplina(cls, disciplina_id, semestre=None):
        db = Database()
        query = """
        SELECT p.*
        FROM professor p
        JOIN professor_disciplina pd ON p.id = pd.professor_id
        WHERE pd.disciplina_id = %s
        """
        params = (disciplina_id,)
        
        if semestre:
            query += " AND pd.semestre = %s"
            params = (disciplina_id, semestre)
            
        query += " ORDER BY p.nome"
        
        professores_data = db.fetch_all(query, params)
        professores = []
        
        if professores_data:
            for prof_data in professores_data:
                professor = cls(
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
    
    def __str__(self):
        return f"{self.nome} (Matrícula: {self.matricula}, Titulação: {self.titulacao})"