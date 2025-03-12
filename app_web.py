from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from database import Database
from controllers.departaments import Departamento
from controllers.courses import Curso
from controllers.disciplines import Disciplina
from controllers.teachers import Professor
from controllers.students import Aluno

app = Flask(__name__)
app.secret_key = os.urandom(24)
db = Database()

db.create_tables()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/departamentos')
def listar_departamentos():
    departamentos = Departamento.listar_todos()
    return render_template('departamentos/listar.html', departamentos=departamentos)

@app.route('/departamentos/novo', methods=['GET', 'POST'])
def cadastrar_departamento():
    if request.method == 'POST':
        nome = request.form['nome']
        sigla = request.form['sigla']
        descricao = request.form['descricao']
        
        departamento = Departamento(nome=nome, sigla=sigla, descricao=descricao)
        
        if departamento.salvar():
            flash('Departamento cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_departamentos'))
        else:
            flash('Erro ao cadastrar departamento!', 'danger')
    
    return render_template('departamentos/form.html')

@app.route('/departamentos/editar/<int:id>', methods=['GET', 'POST'])
def editar_departamento(id):
    departamento = Departamento.buscar_por_id(id)
    
    if not departamento:
        flash('Departamento não encontrado!', 'danger')
        return redirect(url_for('listar_departamentos'))
    
    if request.method == 'POST':
        departamento.nome = request.form['nome']
        departamento.sigla = request.form['sigla']
        departamento.descricao = request.form['descricao']
        
        if departamento.salvar():
            flash('Departamento atualizado com sucesso!', 'success')
            return redirect(url_for('listar_departamentos'))
        else:
            flash('Erro ao atualizar departamento!', 'danger')
    
    return render_template('departamentos/form.html', departamento=departamento)

@app.route('/departamentos/excluir/<int:id>', methods=['POST'])
def excluir_departamento(id):
    departamento = Departamento.buscar_por_id(id)
    
    if not departamento:
        flash('Departamento não encontrado!', 'danger')
        return redirect(url_for('listar_departamentos'))
    
    if departamento.excluir():
        flash('Departamento excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir departamento! Verifique se não há dependências.', 'danger')
    
    return redirect(url_for('listar_departamentos'))

@app.route('/cursos')
def listar_cursos():
    cursos = Curso.listar_todos()
    return render_template('cursos/listar.html', cursos=cursos)

@app.route('/cursos/novo', methods=['GET', 'POST'])
def cadastrar_curso():
    departamentos = Departamento.listar_todos()
    
    if not departamentos:
        flash('Não há departamentos cadastrados! Cadastre um departamento primeiro.', 'warning')
        return redirect(url_for('cadastrar_departamento'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        codigo = request.form['codigo']
        departamento_id = int(request.form['departamento_id'])
        duracao_semestres = int(request.form['duracao_semestres'])
        
        curso = Curso(
            nome=nome, 
            codigo=codigo, 
            departamento_id=departamento_id, 
            duracao_semestres=duracao_semestres
        )
        
        if curso.salvar():
            flash('Curso cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_cursos'))
        else:
            flash('Erro ao cadastrar curso!', 'danger')
    
    return render_template('cursos/form.html', departamentos=departamentos)

@app.route('/cursos/editar/<int:id>', methods=['GET', 'POST'])
def editar_curso(id):
    curso = Curso.buscar_por_id(id)
    departamentos = Departamento.listar_todos()
    
    if not curso:
        flash('Curso não encontrado!', 'danger')
        return redirect(url_for('listar_cursos'))
    
    if request.method == 'POST':
        curso.nome = request.form['nome']
        curso.codigo = request.form['codigo']
        curso.departamento_id = int(request.form['departamento_id'])
        curso.duracao_semestres = int(request.form['duracao_semestres'])
        
        if curso.salvar():
            flash('Curso atualizado com sucesso!', 'success')
            return redirect(url_for('listar_cursos'))
        else:
            flash('Erro ao atualizar curso!', 'danger')
    
    return render_template('cursos/form.html', curso=curso, departamentos=departamentos)

@app.route('/cursos/excluir/<int:id>', methods=['POST'])
def excluir_curso(id):
    curso = Curso.buscar_por_id(id)
    
    if not curso:
        flash('Curso não encontrado!', 'danger')
        return redirect(url_for('listar_cursos'))
    
    if curso.excluir():
        flash('Curso excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir curso! Verifique se não há dependências.', 'danger')
    
    return redirect(url_for('listar_cursos'))

@app.route('/disciplinas')
def listar_disciplinas():
    disciplinas = Disciplina.listar_todos()
    return render_template('disciplinas/listar.html', disciplinas=disciplinas)

@app.route('/disciplinas/curso/<int:curso_id>')
def listar_disciplinas_por_curso(curso_id):
    curso = Curso.buscar_por_id(curso_id)
    if not curso:
        flash('Curso não encontrado!', 'danger')
        return redirect(url_for('listar_cursos'))
    
    disciplinas = Disciplina.listar_por_curso(curso_id)
    return render_template('disciplinas/listar.html', disciplinas=disciplinas, curso=curso)

@app.route('/disciplinas/nova', methods=['GET', 'POST'])
def cadastrar_disciplina():
    cursos = Curso.listar_todos()
    
    if not cursos:
        flash('Não há cursos cadastrados! Cadastre um curso primeiro.', 'warning')
        return redirect(url_for('cadastrar_curso'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        codigo = request.form['codigo']
        curso_id = int(request.form['curso_id'])
        carga_horaria = int(request.form['carga_horaria'])
        semestre = int(request.form['semestre'])
        
        disciplina = Disciplina(
            nome=nome, 
            codigo=codigo, 
            curso_id=curso_id, 
            carga_horaria=carga_horaria,
            semestre=semestre
        )
        
        if disciplina.salvar():
            flash('Disciplina cadastrada com sucesso!', 'success')
            return redirect(url_for('listar_disciplinas'))
        else:
            flash('Erro ao cadastrar disciplina!', 'danger')
    
    return render_template('disciplinas/form.html', cursos=cursos)

@app.route('/disciplinas/editar/<int:id>', methods=['GET', 'POST'])
def editar_disciplina(id):
    disciplina = Disciplina.buscar_por_id(id)
    cursos = Curso.listar_todos()
    
    if not disciplina:
        flash('Disciplina não encontrada!', 'danger')
        return redirect(url_for('listar_disciplinas'))
    
    if request.method == 'POST':
        disciplina.nome = request.form['nome']
        disciplina.codigo = request.form['codigo']
        disciplina.curso_id = int(request.form['curso_id'])
        disciplina.carga_horaria = int(request.form['carga_horaria'])
        disciplina.semestre = int(request.form['semestre'])
        
        if disciplina.salvar():
            flash('Disciplina atualizada com sucesso!', 'success')
            return redirect(url_for('listar_disciplinas'))
        else:
            flash('Erro ao atualizar disciplina!', 'danger')
    
    return render_template('disciplinas/form.html', disciplina=disciplina, cursos=cursos)

@app.route('/disciplinas/excluir/<int:id>', methods=['POST'])
def excluir_disciplina(id):
    disciplina = Disciplina.buscar_por_id(id)
    
    if not disciplina:
        flash('Disciplina não encontrada!', 'danger')
        return redirect(url_for('listar_disciplinas'))
    
    if disciplina.excluir():
        flash('Disciplina excluída com sucesso!', 'success')
    else:
        flash('Erro ao excluir disciplina! Verifique se não há dependências.', 'danger')
    
    return redirect(url_for('listar_disciplinas'))

@app.route('/professores')
def listar_professores():
    professores = Professor.listar_todos()
    return render_template('professores/listar.html', professores=professores)

@app.route('/professores/departamento/<int:departamento_id>')
def listar_professores_por_departamento(departamento_id):
    departamento = Departamento.buscar_por_id(departamento_id)
    if not departamento:
        flash('Departamento não encontrado!', 'danger')
        return redirect(url_for('listar_departamentos'))
    
    professores = Professor.listar_por_departamento(departamento_id)
    return render_template('professores/listar.html', professores=professores, departamento=departamento)

@app.route('/professores/novo', methods=['GET', 'POST'])
def cadastrar_professor():
    departamentos = Departamento.listar_todos()
    
    if not departamentos:
        flash('Não há departamentos cadastrados! Cadastre um departamento primeiro.', 'warning')
        return redirect(url_for('cadastrar_departamento'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        matricula = request.form['matricula']
        email = request.form['email']
        telefone = request.form['telefone']
        departamento_id = int(request.form['departamento_id'])
        titulacao = request.form['titulacao']
        
        professor = Professor(
            nome=nome,
            matricula=matricula,
            email=email,
            telefone=telefone,
            departamento_id=departamento_id,
            titulacao=titulacao
        )
        
        if professor.salvar():
            flash('Professor cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_professores'))
        else:
            flash('Erro ao cadastrar professor!', 'danger')
    
    return render_template('professores/form.html', departamentos=departamentos)

@app.route('/professores/editar/<int:id>', methods=['GET', 'POST'])
def editar_professor(id):
    professor = Professor.buscar_por_id(id)
    departamentos = Departamento.listar_todos()
    
    if not professor:
        flash('Professor não encontrado!', 'danger')
        return redirect(url_for('listar_professores'))
    
    if request.method == 'POST':
        professor.nome = request.form['nome']
        professor.matricula = request.form['matricula']
        professor.email = request.form['email']
        professor.telefone = request.form['telefone']
        professor.departamento_id = int(request.form['departamento_id'])
        professor.titulacao = request.form['titulacao']
        
        if professor.salvar():
            flash('Professor atualizado com sucesso!', 'success')
            return redirect(url_for('listar_professores'))
        else:
            flash('Erro ao atualizar professor!', 'danger')
    
    return render_template('professores/form.html', professor=professor, departamentos=departamentos)

@app.route('/professores/excluir/<int:id>', methods=['POST'])
def excluir_professor(id):
    professor = Professor.buscar_por_id(id)
    
    if not professor:
        flash('Professor não encontrado!', 'danger')
        return redirect(url_for('listar_professores'))
    
    if professor.excluir():
        flash('Professor excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir professor! Verifique se não há dependências.', 'danger')
    
    return redirect(url_for('listar_professores'))

@app.route('/professores/<int:id>/disciplinas')
def listar_disciplinas_professor(id):
    professor = Professor.buscar_por_id(id)
    
    if not professor:
        flash('Professor não encontrado!', 'danger')
        return redirect(url_for('listar_professores'))
    
    disciplinas = professor.listar_disciplinas()
    return render_template('professores/disciplinas.html', professor=professor, disciplinas=disciplinas)

@app.route('/professores/<int:id>/atribuir-disciplina', methods=['GET', 'POST'])
def atribuir_disciplina_professor(id):
    professor = Professor.buscar_por_id(id)
    
    if not professor:
        flash('Professor não encontrado!', 'danger')
        return redirect(url_for('listar_professores'))
    
    disciplinas = Disciplina.listar_todos()
    
    if request.method == 'POST':
        disciplina_id = int(request.form['disciplina_id'])
        semestre = request.form['semestre']
        
        if professor.atribuir_disciplina(disciplina_id, semestre):
            flash('Disciplina atribuída com sucesso!', 'success')
            return redirect(url_for('listar_disciplinas_professor', id=professor.id))
        else:
            flash('Erro ao atribuir disciplina!', 'danger')
    
    return render_template('professores/atribuir_disciplina.html', professor=professor, disciplinas=disciplinas)

@app.route('/alunos')
def listar_alunos():
    alunos = Aluno.listar_todos()
    return render_template('alunos/listar.html', alunos=alunos)

@app.route('/alunos/curso/<int:curso_id>')
def listar_alunos_por_curso(curso_id):
    curso = Curso.buscar_por_id(curso_id)
    if not curso:
        flash('Curso não encontrado!', 'danger')
        return redirect(url_for('listar_cursos'))
    
    alunos = Aluno.listar_por_curso(curso_id)
    return render_template('alunos/listar.html', alunos=alunos, curso=curso)

@app.route('/alunos/novo', methods=['GET', 'POST'])
def cadastrar_aluno():
    cursos = Curso.listar_todos()
    
    if not cursos:
        flash('Não há cursos cadastrados! Cadastre um curso primeiro.', 'warning')
        return redirect(url_for('cadastrar_curso'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        matricula = request.form['matricula']
        email = request.form['email']
        telefone = request.form['telefone']
        curso_id = int(request.form['curso_id'])
        data_ingresso = request.form['data_ingresso']
        
        aluno = Aluno(
            nome=nome,
            matricula=matricula,
            email=email,
            telefone=telefone,
            curso_id=curso_id,
            data_ingresso=data_ingresso
        )
        
        if aluno.salvar():
            flash('Aluno cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_alunos'))
        else:
            flash('Erro ao cadastrar aluno!', 'danger')
    
    return render_template('alunos/form.html', cursos=cursos)

@app.route('/alunos/editar/<int:id>', methods=['GET', 'POST'])
def editar_aluno(id):
    aluno = Aluno.buscar_por_id(id)
    cursos = Curso.listar_todos()
    
    if not aluno:
        flash('Aluno não encontrado!', 'danger')
        return redirect(url_for('listar_alunos'))
    
    if request.method == 'POST':
        aluno.nome = request.form['nome']
        aluno.matricula = request.form['matricula']
        aluno.email = request.form['email']
        aluno.telefone = request.form['telefone']
        aluno.curso_id = int(request.form['curso_id'])
        aluno.data_ingresso = request.form['data_ingresso']
        
        if aluno.salvar():
            flash('Aluno atualizado com sucesso!', 'success')
            return redirect(url_for('listar_alunos'))
        else:
            flash('Erro ao atualizar aluno!', 'danger')
    
    return render_template('alunos/form.html', aluno=aluno, cursos=cursos)

@app.route('/alunos/excluir/<int:id>', methods=['POST'])
def excluir_aluno(id):
    aluno = Aluno.buscar_por_id(id)
    
    if not aluno:
        flash('Aluno não encontrado!', 'danger')
        return redirect(url_for('listar_alunos'))
    
    if aluno.excluir():
        flash('Aluno excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir aluno! Verifique se não há dependências.', 'danger')
    
    return redirect(url_for('listar_alunos'))

@app.route('/alunos/<int:id>/historico')
def historico_aluno(id):
    aluno = Aluno.buscar_por_id(id)
    
    if not aluno:
        flash('Aluno não encontrado!', 'danger')
        return redirect(url_for('listar_alunos'))
    
    disciplinas = aluno.listar_disciplinas()
    cr = aluno.calcular_cr()
    
    return render_template('alunos/historico.html', aluno=aluno, disciplinas=disciplinas, cr=cr)

@app.route('/alunos/<int:id>/matricular', methods=['GET', 'POST'])
def matricular_aluno(id):
    aluno = Aluno.buscar_por_id(id)
    
    if not aluno:
        flash('Aluno não encontrado!', 'danger')
        return redirect(url_for('listar_alunos'))
    
    disciplinas = Disciplina.listar_todos()
    
    if request.method == 'POST':
        disciplina_id = int(request.form['disciplina_id'])
        semestre = request.form['semestre']
        
        if aluno.matricular_em_disciplina(disciplina_id, semestre):
            flash('Matrícula realizada com sucesso!', 'success')
            return redirect(url_for('historico_aluno', id=aluno.id))
        else:
            flash('Erro ao realizar matrícula!', 'danger')
    
    return render_template('alunos/matricular.html', aluno=aluno, disciplinas=disciplinas)

@app.route('/professores/<int:professor_id>/remover-disciplina/<int:disciplina_id>/<semestre>', methods=['POST'])
def remover_disciplina_professor(professor_id, disciplina_id, semestre):
    professor = Professor.buscar_por_id(professor_id)
    
    if not professor:
        flash('Professor não encontrado!', 'danger')
        return redirect(url_for('listar_professores'))
    
    if professor.remover_disciplina(disciplina_id, semestre):
        flash('Disciplina removida com sucesso!', 'success')
    else:
        flash('Erro ao remover disciplina!', 'danger')
    
    return redirect(url_for('listar_disciplinas_professor', id=professor_id))

@app.route('/disciplinas/<int:id>/detalhes')
def detalhes_disciplina(id):
    disciplina = Disciplina.buscar_por_id(id)
    
    if not disciplina:
        flash('Disciplina não encontrada!', 'danger')
        return redirect(url_for('listar_disciplinas'))
    
    professores = disciplina.listar_professores()
    
    alunos = Aluno.buscar_por_disciplina(disciplina.id)
    
    return render_template('disciplinas/detalhes.html', disciplina=disciplina, professores=professores, alunos=alunos, Professor=Professor)

@app.route('/disciplinas/<int:disciplina_id>/atribuir-professor', methods=['POST'])
def atribuir_professor_disciplina(disciplina_id):
    disciplina = Disciplina.buscar_por_id(disciplina_id)
    
    if not disciplina:
        flash('Disciplina não encontrada!', 'danger')
        return redirect(url_for('listar_disciplinas'))
    
    professor_id = int(request.form['professor_id'])
    semestre = request.form['semestre']
    
    professor = Professor.buscar_por_id(professor_id)
    
    if not professor:
        flash('Professor não encontrado!', 'danger')
        return redirect(url_for('detalhes_disciplina', id=disciplina_id))
    
    if professor.atribuir_disciplina(disciplina_id, semestre):
        flash('Professor atribuído com sucesso!', 'success')
    else:
        flash('Erro ao atribuir professor!', 'danger')
    
    return redirect(url_for('detalhes_disciplina', id=disciplina_id))

@app.route('/alunos/<int:id>/registrar-nota', methods=['GET', 'POST'])
def registrar_nota_aluno(id):
    aluno = Aluno.buscar_por_id(id)
    
    if not aluno:
        flash('Aluno não encontrado!', 'danger')
        return redirect(url_for('listar_alunos'))
    
    disciplinas = aluno.listar_disciplinas()
    disciplinas_matriculadas = [d[0] for d in disciplinas]
    
    if request.method == 'POST':
        disciplina_id = int(request.form['disciplina_id'])
        semestre = request.form['semestre']
        nota = float(request.form['nota'])
        
        if aluno.registrar_nota(disciplina_id, semestre, nota):
            flash('Nota registrada com sucesso!', 'success')
            return redirect(url_for('historico_aluno', id=aluno.id))
        else:
            flash('Erro ao registrar nota!', 'danger')
    
    return render_template('alunos/registrar_nota.html', aluno=aluno, disciplinas_matriculadas=disciplinas_matriculadas)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)