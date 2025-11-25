"""
Vue Articles - Gestion des articles
"""

import tkinter as tk
from tkinter import ttk
from .base_view import BaseView
from controllers import ArticleController
from utils.formatters import format_currency
from config.settings import COLORS


class ArticlesView(BaseView):
    """Vue pour la gestion des articles"""
    
    def __init__(self, parent):
        self.controller = ArticleController()
        self.article_id_modif = None
        super().__init__(parent)
    
    def setup_ui(self):
        """Créer l'interface"""
        # Formulaire
        self.create_form()
        
        # Liste
        self.create_list()
    
    def create_form(self):
        """Formulaire d'ajout/modification"""
        form_frame = ttk.LabelFrame(self.frame, text="Ajouter/Modifier un article", padding=15)
        form_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(form_frame, text="Nom de l'article:", font=('Arial', 11)).grid(row=0, column=0, sticky='w', padx=5, pady=8)
        self.article_nom_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.article_nom_var, width=35, font=('Arial', 11)).grid(row=0, column=1, padx=5, pady=8)
        
        ttk.Label(form_frame, text="Prix d'achat (DT):", font=('Arial', 11)).grid(row=1, column=0, sticky='w', padx=5, pady=8)
        self.article_achat_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.article_achat_var, width=20, font=('Arial', 11)).grid(row=1, column=1, sticky='w', padx=5, pady=8)
        
        ttk.Label(form_frame, text="Prix de vente (DT):", font=('Arial', 11)).grid(row=2, column=0, sticky='w', padx=5, pady=8)
        self.article_vente_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=self.article_vente_var, width=20, font=('Arial', 11)).grid(row=2, column=1, sticky='w', padx=5, pady=8)
        
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        ttk.Button(btn_frame, text="💾 Enregistrer", command=self.enregistrer_article).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔄 Nouveau", command=self.reset_form).pack(side='left', padx=5)
    
    def create_list(self):
        """Liste des articles"""
        list_frame = ttk.LabelFrame(self.frame, text="Liste des articles", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('ID', 'Nom', 'Prix Achat', 'Prix Vente', 'Marge', 'Marge %')
        self.articles_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=18)
        
        self.articles_tree.heading('ID', text='ID')
        self.articles_tree.heading('Nom', text='Nom')
        self.articles_tree.heading('Prix Achat', text='Prix Achat (DT)')
        self.articles_tree.heading('Prix Vente', text='Prix Vente (DT)')
        self.articles_tree.heading('Marge', text='Marge (DT)')
        self.articles_tree.heading('Marge %', text='Marge %')
        
        self.articles_tree.column('ID', width=50, anchor='center')
        self.articles_tree.column('Nom', width=300)
        self.articles_tree.column('Prix Achat', width=120, anchor='center')
        self.articles_tree.column('Prix Vente', width=120, anchor='center')
        self.articles_tree.column('Marge', width=120, anchor='center')
        self.articles_tree.column('Marge %', width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.articles_tree.yview)
        self.articles_tree.configure(yscrollcommand=scrollbar.set)
        
        self.articles_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Boutons d'action
        action_frame = ttk.Frame(list_frame)
        action_frame.pack(fill='x', pady=5)
        
        ttk.Button(action_frame, text="✏️ Modifier", 
                command=self.modifier_article).pack(side='left', padx=5)
        
        ttk.Button(action_frame, text="🗑️ Supprimer", 
                command=self.supprimer_article).pack(side='left', padx=5)
        
        ttk.Button(action_frame, text="🗑️ Supprimer tout", 
                command=self.supprimer_tous_articles).pack(side='left', padx=5)
        
        self.charger_articles()
    
    def charger_articles(self):
        """Charger la liste"""
        for item in self.articles_tree.get_children():
            self.articles_tree.delete(item)
        
        articles = self.controller.get_all_articles()
        for article in articles:
            prix_achat = float(article['prix_achat'])
            prix_vente = float(article['prix_vente'])
            marge, marge_pct = self.controller.calculate_margin(prix_achat, prix_vente)
            
            self.articles_tree.insert('', 'end', values=(
                article['id'],
                article['nom'],
                f"{prix_achat:.2f}",
                f"{prix_vente:.2f}",
                f"{marge:.2f}",
                f"{marge_pct:.1f}%"
            ))
    
    def enregistrer_article(self):
        """Enregistrer"""
        nom = self.article_nom_var.get().strip()
        
        try:
            prix_achat = float(self.article_achat_var.get())
            prix_vente = float(self.article_vente_var.get())
        except ValueError:
            self.show_error("Erreur", "Veuillez entrer des prix valides!")
            return
        
        if self.controller.is_margin_negative(prix_achat, prix_vente):
            if not self.confirm("Attention", 
                "Le prix de vente est inférieur au prix d'achat!\nContinuer quand même?"):
                return
        
        try:
            if self.article_id_modif:
                self.controller.update_article(self.article_id_modif, nom, prix_achat, prix_vente)
                self.show_success("Succès", "Article modifié avec succès!")
            else:
                self.controller.create_article(nom, prix_achat, prix_vente)
                self.show_success("Succès", "Article ajouté avec succès!")
            
            self.reset_form()
            self.charger_articles()
        except Exception as e:
            self.show_error("Erreur", str(e))
    
    def modifier_article(self):
        """Modifier"""
        selection = self.articles_tree.selection()
        if not selection:
            self.show_warning("Attention", "Veuillez sélectionner un article!")
            return
        
        item = self.articles_tree.item(selection[0])
        values = item['values']
        
        self.article_id_modif = values[0]
        self.article_nom_var.set(values[1])
        self.article_achat_var.set(values[2])
        self.article_vente_var.set(values[3])
    
    def supprimer_article(self):
        """Supprimer"""
        selection = self.articles_tree.selection()
        if not selection:
            self.show_warning("Attention", "Veuillez sélectionner un article!")
            return
        
        item = self.articles_tree.item(selection[0])
        article_id = item['values'][0]
        article_nom = item['values'][1]
        
        if self.confirm("Confirmation", 
            f"Supprimer l'article '{article_nom}'?\nCela supprimera aussi toutes les ventes associées!"):
            try:
                self.controller.delete_article(article_id)
                self.show_success("Succès", "Article supprimé!")
                self.charger_articles()
            except Exception as e:
                self.show_error("Erreur", str(e))
    
    def supprimer_tous_articles(self):
        """Supprimer tout"""
        articles = self.controller.get_all_articles()
        nb_articles = len(articles)
        
        if nb_articles == 0:
            self.show_success("Information", "Aucun article à supprimer!")
            return
        
        if self.confirm("⚠️ ATTENTION", 
            f"Voulez-vous vraiment supprimer TOUS les {nb_articles} articles?\n\n" +
            "⚠️ CETTE ACTION EST IRRÉVERSIBLE!\n" +
            "⚠️ Toutes les ventes associées seront également supprimées!"):
            
            if self.confirm("⚠️ CONFIRMATION FINALE", 
                "Êtes-vous ABSOLUMENT SÛR?\n\n" +
                "Cette action va tout supprimer !"):
                
                try:
                    nb_supprimes = self.controller.delete_all_articles()
                    
                    self.show_success("✅ Succès", 
                        f"{nb_supprimes} article(s) supprimé(s) avec succès!")
                    
                    self.charger_articles()
                    
                except Exception as e:
                    self.show_error("❌ Erreur", str(e))
    
    def reset_form(self):
        """Réinitialiser le formulaire"""
        self.article_id_modif = None
        self.article_nom_var.set('')
        self.article_achat_var.set('')
        self.article_vente_var.set('')