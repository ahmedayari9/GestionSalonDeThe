"""
Modèle de base pour tous les modèles
Pattern Repository
"""

from config.database import DatabaseConnection


class BaseModel:
    """Classe de base pour tous les modèles"""
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.connection = self.db.get_connection()
    
    def _execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Exécuter une requête SQL de manière sécurisée"""
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            self.connection.commit()
            result = cursor.lastrowid if cursor.lastrowid else cursor.rowcount
        
        cursor.close()
        return result
    
    def _execute_many(self, query, data_list):
        """Exécuter plusieurs insertions"""
        cursor = self.connection.cursor()
        cursor.executemany(query, data_list)
        self.connection.commit()
        cursor.close()
        return cursor.rowcount