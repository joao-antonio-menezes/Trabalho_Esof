import sqlite3
import csv
from pathlib import Path

DB_FILE = 'projeto_agil.db'
PROJETOS_CSV_FILE = 'pojetos.csv'
TAREFAS_CSV_FILE = 'tarefas.csv'

def init_db():
    if not Path(DB_FILE).is_file():
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # Criação da tabela de projetos
        c.execute('''CREATE TABLE projetos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        descricao TEXT NOT NULL,
                        data_criacao DATE NOT NULL DEFAULT CURRENT_DATE
                     )''')

        # Criação da tabela de tarefas
        c.execute('''CREATE TABLE tarefas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        descricao TEXT NOT NULL,
                        data_criacao DATE NOT NULL DEFAULT CURRENT_DATE,
                        status BOOLEAN NOT NULL,
                        projeto_id INTEGER NOT NULL,
                        FOREIGN KEY (projeto_id) REFERENCES projetos(id)
                     )''')
        conn.commit()
        conn.close()
        populate_projetos()
        populate_tarefas()

def get_all_projects():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM projetos')
    projetos = c.fetchall()
    conn.close()
    return projetos

def get_completed_tasks(project_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM tarefas WHERE projeto_id = ? AND status = 1', (project_id,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_incomplete_tasks(project_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM tarefas WHERE projeto_id = ? AND status = 0', (project_id,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_project(id):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projetos WHERE id = ?', (id,))
    projeto = cursor.fetchone()
    conn.close()
    return projeto

def update_task_status(tarefa_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('UPDATE tarefas SET status = CASE WHEN status = 1 THEN 0 ELSE 1 END WHERE id = ?', (tarefa_id,))
    conn.commit()
    conn.close()

def add_task_to_project(descricao, projeto_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tarefas (descricao, status, projeto_id) VALUES (?, ?, ?)', (descricao, '0', projeto_id))
    conn.commit()
    conn.close()

def delete_project(projeto_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM projetos WHERE id = ?', (projeto_id,))
    cursor.execute('DELETE FROM tarefas WHERE projeto_id = ?', (projeto_id,))
    conn.commit()
    conn.close()

def update_project(projeto_id, novo_nome, nova_descricao):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('UPDATE projetos SET nome = ?, descricao = ? WHERE id = ?', (novo_nome, nova_descricao, projeto_id))
    conn.commit()
    conn.close()

def create_project(nome, descricao):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO projetos (nome, descricao) VALUES (?, ?)', (nome, descricao))
    conn.commit()
    conn.close()

#----------------------------------- Popular o Banco de dados --------------------------------

def populate_projetos():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Populando a tabela projetos
    with open(PROJETOS_CSV_FILE, newline='', encoding='utf-8') as csvfile:
        projetos_reader = csv.DictReader(csvfile)
        for row in projetos_reader:
            cursor.execute('INSERT INTO projetos (nome, descricao, data_criacao) VALUES (?, ?, ?)',
                           (row['nome'], row['descricao'], row['data_criacao']))

    conn.commit()
    conn.close()

def populate_tarefas():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Populando a tabela tarefas
    with open(TAREFAS_CSV_FILE, newline='', encoding='utf-8') as csvfile:
        tarefas_reader = csv.DictReader(csvfile)
        for row in tarefas_reader:
            # Convertendo 'True'/'False' para True/False
            status = row['status'].lower() == 'true'
            cursor.execute('INSERT INTO tarefas (descricao, data_criacao, status, projeto_id) VALUES (?, ?, ?, ?)',
                           (row['descricao'], row['data_criacao'], status, row['projeto_id']))
    conn.commit()
    conn.close()