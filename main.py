#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sultan Ahmed - Application de Gestion Professionnelle
Point d'entrée principal
"""

import sys
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# Ajouter le dossier racine au path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from config.database import DatabaseConnection
from views.main_window import MainWindow
from utils.logger import setup_logger


def main():
    """Point d'entrée de l'application"""
    logger = setup_logger()
    logger.info("🚀 Démarrage de Sultan Ahmed")
    
    try:
        # Test connexion DB
        db = DatabaseConnection()
        if not db.test_connection():
            raise Exception("MySQL n'est pas accessible!\n\nVérifiez que XAMPP est lancé.")
        
        logger.info("✅ Connexion MySQL OK")
        
        # Lancer l'interface
        root = tk.Tk()
        app = MainWindow(root)
        root.mainloop()
        
    except Exception as e:
        logger.error(f"❌ Erreur fatale: {e}")
        messagebox.showerror("Erreur", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()