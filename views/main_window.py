"""
Fenêtre principale de l'application
"""

import tkinter as tk
from tkinter import ttk, messagebox
from config.settings import APP_CONFIG, COLORS
from views.ventes_view import VentesView
from views.articles_view import ArticlesView
from views.bilan_view import BilanView
from views.historique_view import HistoriqueView
from utils.logger import get_logger


class MainWindow:
    """Fenêtre principale avec onglets"""
    
    def __init__(self, root):
        self.root = root
        self.logger = get_logger()
        self.setup_window()
        self.create_header()
        self.create_notebook()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_window(self):
        """Configuration de la fenêtre"""
        self.root.title(APP_CONFIG['title'])
        self.root.geometry(f"{APP_CONFIG['width']}x{APP_CONFIG['height']}")
        self.root.state('zoomed')
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 20, 'bold'), foreground=COLORS['primary'])
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Big.TButton', font=('Arial', 12, 'bold'), padding=12)
        style.configure('Success.TButton', font=('Arial', 12, 'bold'), padding=12, background=COLORS['success'])
    
    def create_header(self):
        """Créer l'en-tête"""
        header = tk.Frame(self.root, bg=COLORS['primary'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text=f"☕ Sultan Ahmed - Salon de Thé (v{APP_CONFIG['version']})",
            font=('Arial', 24, 'bold'),
            bg=COLORS['primary'],
            fg='white'
        )
        title.pack(pady=20)
    
    def create_notebook(self):
        """Créer les onglets"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Créer les vues
        self.ventes_view = VentesView(self.notebook)
        self.articles_view = ArticlesView(self.notebook)
        self.bilan_view = BilanView(self.notebook)
        self.historique_view = HistoriqueView(self.notebook)
        
        # Ajouter les onglets
        self.notebook.add(self.ventes_view.get_frame(), text='📅 Ventes du Jour')
        self.notebook.add(self.articles_view.get_frame(), text='🛍️ Articles')
        self.notebook.add(self.bilan_view.get_frame(), text='📊 Bilan Mensuel')
        self.notebook.add(self.historique_view.get_frame(), text='📊 Historique')
        
        # Observer les changements d'onglets
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
    
    def on_tab_changed(self, event):
        """Événement changement d'onglet"""
        current_tab = self.notebook.select()
        tab_text = self.notebook.tab(current_tab, "text")
        self.logger.info(f"Changement d'onglet: {tab_text}")
        
        # Rafraîchir la vue si nécessaire
        if "Historique" in tab_text:
            self.historique_view.refresh()
        elif "Bilan" in tab_text:
            self.bilan_view.refresh()
    
    def on_closing(self):
        """Fermeture de l'application"""
        if messagebox.askokcancel("Quitter", "Voulez-vous quitter Sultan Ahmed?"):
            self.logger.info("🛑 Fermeture de l'application")
            self.root.destroy()