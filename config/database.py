"""
Gestion de la connexion à la base de données
Pattern Singleton pour une connexion unique
"""

import mysql.connector
from mysql.connector import Error
from .settings import DB_CONFIG


class DatabaseConnection:
    """Singleton pour la connexion MySQL"""
    
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._connection is None or not self._connection.is_connected():
            self.connect()
    
    def connect(self):
        """Établir la connexion"""
        try:
            self._connection = mysql.connector.connect(**DB_CONFIG)
            if self._connection.is_connected():
                self._create_tables()
                return True
        except Error as e:
            raise Exception(f"Erreur connexion MySQL: {e}")
    
    def get_connection(self):
        """Retourner la connexion active"""
        if not self._connection or not self._connection.is_connected():
            self.connect()
        return self._connection
    
    def test_connection(self):
        """Tester la connexion"""
        try:
            conn = self.get_connection()
            return conn.is_connected()
        except:
            return False
    
    def _create_tables(self):
        """Créer les tables si elles n'existent pas"""
        cursor = self._connection.cursor()
        
        # Table articles
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nom VARCHAR(255) NOT NULL,
                prix_achat DECIMAL(10, 2) NOT NULL,
                prix_vente DECIMAL(10, 2) NOT NULL,
                actif BOOLEAN DEFAULT TRUE,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Table ventes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date_vente DATE NOT NULL,
                article_id INT NOT NULL,
                quantite INT NOT NULL DEFAULT 0,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
                UNIQUE KEY unique_vente (date_vente, article_id)
            )
        """)
        
        # Table charges journalières
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS charges (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date_charge DATE NOT NULL,
                description VARCHAR(255) NOT NULL,
                montant DECIMAL(10, 2) NOT NULL,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_date (date_charge)
            )
        """)
        
        # Table charges fixes mensuelles
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS charges_fixes_mensuelles (
                id INT AUTO_INCREMENT PRIMARY KEY,
                mois DATE NOT NULL,
                loyer DECIMAL(10, 2) DEFAULT 0,
                electricite DECIMAL(10, 2) DEFAULT 0,
                eau DECIMAL(10, 2) DEFAULT 0,
                impot DECIMAL(10, 2) DEFAULT 0,
                municipalite DECIMAL(10, 2) DEFAULT 0,
                terrasse DECIMAL(10, 2) DEFAULT 0,
                internet DECIMAL(10, 2) DEFAULT 0,
                autres DECIMAL(10, 2) DEFAULT 0,
                autres_description TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_mois (mois)
            )
        """)
        
        # Table salaires
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS salaires_mensuels (
                id INT AUTO_INCREMENT PRIMARY KEY,
                mois DATE NOT NULL,
                nom_employe VARCHAR(255) NOT NULL,
                montant DECIMAL(10, 2) NOT NULL,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_mois (mois)
            )
        """)
        
        self._connection.commit()
        cursor.close()
    
    def close(self):
        """Fermer la connexion"""
        if self._connection and self._connection.is_connected():
            self._connection.close()