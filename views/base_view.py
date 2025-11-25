"""
Vue de base abstraite pour tous les onglets
"""

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod


class BaseView(ABC):
    """Classe abstraite pour toutes les vues"""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.setup_ui()
    
    @abstractmethod
    def setup_ui(self):
        """Méthode abstraite pour créer l'interface"""
        pass
    
    def get_frame(self):
        """Retourner le frame principal"""
        return self.frame
    
    def show_error(self, title, message):
        """Afficher un message d'erreur"""
        from tkinter import messagebox
        messagebox.showerror(title, message)
    
    def show_success(self, title, message):
        """Afficher un message de succès"""
        from tkinter import messagebox
        messagebox.showinfo(title, message)
    
    def show_warning(self, title, message):
        """Afficher un avertissement"""
        from tkinter import messagebox
        messagebox.showwarning(title, message)
    
    def confirm(self, title, message):
        """Demander confirmation"""
        from tkinter import messagebox
        return messagebox.askyesno(title, message)