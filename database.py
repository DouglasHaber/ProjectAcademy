import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", "3306"))
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.database = os.getenv("DB_NAME", "project_academy")
        self.connection = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Erro ao executar query: {e}")
            return False
    
    def fetch_all(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Erro ao buscar dados: {e}")
            return None
    
    def fetch_one(self, query, params=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"Erro ao buscar dados: {e}")
            return None
    
    def create_tables(self):
        
        create_departamento_table = """
        CREATE TABLE IF NOT EXISTS departamento (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            sigla VARCHAR(10) NOT NULL,
            descricao TEXT
        );
        """
        
        create_professor_table = """
        CREATE TABLE IF NOT EXISTS professor (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            matricula VARCHAR(20) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            telefone VARCHAR(20),
            departamento_id INT,
            titulacao VARCHAR(50),
            FOREIGN KEY (departamento_id) REFERENCES departamento(id)
        );
        """
        
        create_curso_table = """
        CREATE TABLE IF NOT EXISTS curso (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            codigo VARCHAR(20) UNIQUE NOT NULL,
            departamento_id INT,
            duracao_semestres INT NOT NULL,
            FOREIGN KEY (departamento_id) REFERENCES departamento(id)
        );
        """
        
        create_disciplina_table = """
        CREATE TABLE IF NOT EXISTS disciplina (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            codigo VARCHAR(20) UNIQUE NOT NULL,
            curso_id INT,
            carga_horaria INT NOT NULL,
            semestre INT NOT NULL,
            FOREIGN KEY (curso_id) REFERENCES curso(id)
        );
        """
        
        create_aluno_table = """
        CREATE TABLE IF NOT EXISTS aluno (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            matricula VARCHAR(20) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            telefone VARCHAR(20),
            curso_id INT,
            data_ingresso DATE NOT NULL,
            FOREIGN KEY (curso_id) REFERENCES curso(id)
        );
        """
        
        create_professor_disciplina_table = """
        CREATE TABLE IF NOT EXISTS professor_disciplina (
            professor_id INT,
            disciplina_id INT,
            semestre VARCHAR(6) NOT NULL,
            PRIMARY KEY (professor_id, disciplina_id, semestre),
            FOREIGN KEY (professor_id) REFERENCES professor(id),
            FOREIGN KEY (disciplina_id) REFERENCES disciplina(id)
        );
        """
        
        create_matricula_table = """
        CREATE TABLE IF NOT EXISTS matricula (
            aluno_id INT,
            disciplina_id INT,
            semestre VARCHAR(6) NOT NULL,
            nota FLOAT,
            situacao ENUM('Matriculado', 'Aprovado', 'Reprovado', 'Trancado') DEFAULT 'Matriculado',
            PRIMARY KEY (aluno_id, disciplina_id, semestre),
            FOREIGN KEY (aluno_id) REFERENCES aluno(id),
            FOREIGN KEY (disciplina_id) REFERENCES disciplina(id)
        );
        """
        
        self.execute_query(create_departamento_table)
        self.execute_query(create_professor_table)
        self.execute_query(create_curso_table)
        self.execute_query(create_disciplina_table)
        self.execute_query(create_aluno_table)
        self.execute_query(create_professor_disciplina_table)
        self.execute_query(create_matricula_table)
        
        print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    db = Database()
    connection = db.connect()
    
    if connection:
        print("Conexão bem sucedida!")
        db.create_tables()
        db.disconnect()
    else:
        print("Falha na conexão.")