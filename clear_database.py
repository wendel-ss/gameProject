#!/usr/bin/env python3

import sqlite3
import os

def clear_database():
    try:
        # Encontra o caminho do banco de dados
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        db_path = os.path.join(data_dir, 'scores.db')
        
        # Conecta ao banco
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Limpa a tabela
        cursor.execute('DELETE FROM scores')
        
        # Commit das mudanças
        conn.commit()
        
        # Opcional: reinicia a sequência de IDs
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="scores"')
        conn.commit()
        
        print("Banco de dados limpo com sucesso!")
        
    except Exception as e:
        print(f"Erro ao limpar o banco de dados: {e}")
        
    finally:
        # Fecha a conexão
        if conn:
            conn.close()

if __name__ == "__main__":
    resposta = input("Tem certeza que deseja limpar todos os scores? (s/n): ")
    if resposta.lower() == 's':
        clear_database()
    else:
        print("Operação cancelada.")
