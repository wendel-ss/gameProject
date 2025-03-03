import sqlite3
import os
import sys

class ScoreDatabase:
    def __init__(self):
        # Obtém o caminho base do executável
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.dirname(__file__))
        
        # Cria o diretório 'data' se não existir
        data_dir = os.path.join(application_path, 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Define o caminho do banco de dados
        self.db_path = os.path.join(data_dir, 'scores.db')
        
        # Conecta ao banco de dados e cria a tabela se não existir
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Cria a tabela de scores se não existir
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def save_score(self, player_name, score):
        self.cursor.execute('INSERT INTO scores (player_name, score) VALUES (?, ?)',
                          (player_name, score))
        self.conn.commit()
    
    def get_top_scores(self, limit=5):
        self.cursor.execute('SELECT player_name, score FROM scores ORDER BY score DESC LIMIT ?',
                          (limit,))
        return self.cursor.fetchall()
    
    def __del__(self):
        self.conn.close() 