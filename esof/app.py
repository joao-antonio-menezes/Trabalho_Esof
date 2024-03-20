from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_all_projects, get_completed_tasks, get_incomplete_tasks, get_project, update_task_status, add_task_to_project, delete_project, update_project, create_project

app = Flask(__name__)

@app.route('/')
def index():
    projetos = get_all_projects()
    return render_template('index.html', projetos=projetos)

@app.route('/projeto/<int:projeto_id>')
def detalhes_projeto(projeto_id):
    projeto = get_project(projeto_id)
    if projeto:
        tarefas_concluidas = get_completed_tasks(projeto_id)
        tarefas_nao_concluidas = get_incomplete_tasks(projeto_id)
        return render_template('detalhes_projeto.html', projeto=projeto,
                                tarefas_concluidas=tarefas_concluidas,
                                tarefas_nao_concluidas=tarefas_nao_concluidas)
    else:
        return render_template('error.html', message="Projeto não encontrado.")   
   

@app.route('/marcar_tarefa_concluida', methods=['POST'])
def marcar_tarefa_concluida():
    tarefa_id = request.form['tarefa_id']
    update_task_status(tarefa_id)
    return '', 204

@app.route('/projeto/<int:projeto_id>/adicionar_tarefa', methods=['POST'])
def adicionar_tarefa(projeto_id):
    descricao = request.form['descricao']
    add_task_to_project(descricao, projeto_id)
    tarefas_concluidas = get_completed_tasks(projeto_id)
    tarefas_nao_concluidas = get_incomplete_tasks(projeto_id)
    return render_template('detalhes_projeto.html', projeto=get_project(projeto_id),
                           tarefas_concluidas=tarefas_concluidas,
                           tarefas_nao_concluidas=tarefas_nao_concluidas)

@app.route('/projeto/<int:projeto_id>/excluir_projeto', methods=['POST'])
def excluir_projeto(projeto_id):
    delete_project(projeto_id)
    return redirect(url_for('index'))

@app.route('/projeto/<int:projeto_id>/editar', methods=['GET'])
def editar_projeto_form(projeto_id):
    projeto = get_project(projeto_id)
    projeto = {'id': projeto_id, 'nome': projeto[1], 'descricao': projeto[2]}
    return render_template('editar_projeto.html', projeto=projeto)

@app.route('/projeto/<int:projeto_id>/editar', methods=['POST'])
def editar_projeto(projeto_id):
    novo_nome = request.form['novo_nome']
    nova_descricao = request.form['nova_descricao']
    update_project(projeto_id, novo_nome, nova_descricao)
    return redirect(url_for('detalhes_projeto', projeto_id=projeto_id))


@app.route('/criar_projeto', methods=['GET','POST'])
def criar_projeto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        create_project(nome, descricao)  
        return redirect(url_for('index'))
    else:
        return render_template('criar_projeto.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)