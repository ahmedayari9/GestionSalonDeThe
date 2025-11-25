"""
Vue Ventes - Onglet de saisie des ventes quotidiennes
"""

import tkinter as tk
from tkinter import ttk
from datetime import date, timedelta
from .base_view import BaseView
from controllers import VenteController, ArticleController, ChargeController
from utils.formatters import format_currency, format_date
from config.settings import COLORS


class VentesView(BaseView):
    """Vue pour la gestion des ventes quotidiennes"""
    
    def __init__(self, parent):
        # Contrôleurs
        self.vente_controller = VenteController()
        self.article_controller = ArticleController()
        self.charge_controller = ChargeController()
        
        # État
        self.date_selectionnee = date.today()
        self.quantite_entries = {}
        
        # ✅ VARIABLES TKINTER (créées AVANT super().__init__)
        self.date_var = tk.StringVar(value=format_date(self.date_selectionnee))
        self.charge_desc_var = tk.StringVar()
        self.charge_montant_var = tk.StringVar()
        
        self.recette_brute_var = tk.StringVar(value="0.00 DT")
        self.cout_achat_var = tk.StringVar(value="0.00 DT")
        self.benefice_brut_var = tk.StringVar(value="0.00 DT")
        self.charges_var = tk.StringVar(value="0.00 DT")
        self.charges_journalieres_var = tk.StringVar(value="0.00 DT")
        self.benefice_net_var = tk.StringVar(value="0.00 DT")
        
        # Appeler le constructeur parent (qui appelle setup_ui)
        super().__init__(parent)
    
    def setup_ui(self):
        """Créer l'interface"""
        # Conteneur principal
        main_container = ttk.Frame(self.frame)
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Colonne gauche (65%)
        left_column = ttk.Frame(main_container)
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.create_date_selector(left_column)
        self.create_ventes_input(left_column)
        self.create_charges_input(left_column)
        
        # Colonne droite (35%)
        right_column = ttk.Frame(main_container)
        right_column.pack(side='right', fill='both', padx=(10, 0))
        
        self.create_resume_financier(right_column)
    
    def create_date_selector(self, parent):
        """Sélecteur de date"""
        date_frame = ttk.LabelFrame(parent, text="📅 Date de vente", padding=15)
        date_frame.pack(fill='x', pady=(0, 15))
        
        date_controls = ttk.Frame(date_frame)
        date_controls.pack()
        
        ttk.Button(date_controls, text="◀", command=self.jour_precedent, width=3).pack(side='left', padx=5)
        
        date_label = ttk.Label(date_controls, textvariable=self.date_var, 
                              font=('Arial', 14, 'bold'), foreground=COLORS['primary'])
        date_label.pack(side='left', padx=15)
        
        ttk.Button(date_controls, text="▶", command=self.jour_suivant, width=3).pack(side='left', padx=5)
        ttk.Button(date_controls, text="Aujourd'hui", command=self.aller_aujourdhui).pack(side='left', padx=20)
    
    def create_ventes_input(self, parent):
        """Zone de saisie des ventes"""
        ventes_frame = ttk.LabelFrame(parent, text="🛒 Saisie des ventes", padding=15)
        ventes_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        instructions = ttk.Label(ventes_frame, 
                                text="Entrez la quantité vendue pour chaque article :", 
                                font=('Arial', 11, 'italic'),
                                foreground=COLORS['secondary'])
        instructions.pack(pady=(0, 10))
        
        # Canvas avec scrollbar
        canvas_frame = ttk.Frame(ventes_frame)
        canvas_frame.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(canvas_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        self.articles_saisie_frame = ttk.Frame(canvas)
        
        self.articles_saisie_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas_window_id = canvas.create_window((0, 0), window=self.articles_saisie_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window_id, width=event.width)
        
        canvas.bind('<Configure>', _on_canvas_configure)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.charger_articles_saisie()
    
    def create_charges_input(self, parent):
        """Zone de saisie des charges"""
        charges_frame = ttk.LabelFrame(parent, text="💸 Dépenses du jour", padding=15)
        charges_frame.pack(fill='both')
        
        input_frame = ttk.Frame(charges_frame)
        input_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(input_frame, text="Description:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.charge_desc_var, width=25, font=('Arial', 10)).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Montant (DT):", font=('Arial', 10)).grid(row=0, column=2, sticky='w', padx=5, pady=5)
        ttk.Entry(input_frame, textvariable=self.charge_montant_var, width=15, font=('Arial', 10)).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(input_frame, text="➕ Ajouter", command=self.ajouter_charge).grid(row=0, column=4, padx=5, pady=5)
        
        # ✅ Bouton Supprimer sur la même ligne
        ttk.Button(input_frame, text="🗑️ Supprimer", 
                command=self.supprimer_charge).grid(row=0, column=5, padx=5, pady=5)
        
        # Liste des charges
        self.charges_listbox = tk.Listbox(charges_frame, height=3, font=('Arial', 10))
        self.charges_listbox.pack(fill='x', pady=(10, 0))
        
        self.charger_charges()
    
    def create_resume_financier(self, parent):
        """Résumé financier"""
        resume_frame = ttk.LabelFrame(parent, text="💰 Résumé de la journée", padding=20)
        resume_frame.pack(fill='both', expand=True)
        
        row = 0
        
        ttk.Label(resume_frame, text="Recette brute", font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=10, padx=5)
        ttk.Label(resume_frame, textvariable=self.recette_brute_var, font=('Arial', 11, 'bold'), foreground=COLORS['info']).grid(row=row, column=1, sticky='e', pady=10, padx=5)
        row += 1
        
        ttk.Label(resume_frame, text="Coût d'achat", font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=10, padx=5)
        ttk.Label(resume_frame, textvariable=self.cout_achat_var, font=('Arial', 11, 'bold'), foreground=COLORS['danger']).grid(row=row, column=1, sticky='e', pady=10, padx=5)
        row += 1
        
        ttk.Label(resume_frame, text="Bénéfice brut", font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=10, padx=5)
        ttk.Label(resume_frame, textvariable=self.benefice_brut_var, font=('Arial', 11, 'bold'), foreground=COLORS['success']).grid(row=row, column=1, sticky='e', pady=10, padx=5)
        row += 1
        
        ttk.Label(resume_frame, text="Dépenses", font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=10, padx=5)
        ttk.Label(resume_frame, textvariable=self.charges_var, font=('Arial', 11, 'bold'), foreground=COLORS['danger']).grid(row=row, column=1, sticky='e', pady=10, padx=5)
        row += 1
        
        ttk.Label(resume_frame, text="Charges journalières", font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=10, padx=5)
        ttk.Label(resume_frame, textvariable=self.charges_journalieres_var, font=('Arial', 11, 'bold'), foreground=COLORS['warning']).grid(row=row, column=1, sticky='e', pady=10, padx=5)
        row += 1
        
        ttk.Separator(resume_frame, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky='ew', pady=20)
        row += 1
        
        ttk.Label(resume_frame, text="BÉNÉFICE NET", font=('Arial', 14, 'bold')).grid(row=row, column=0, sticky='w', pady=15, padx=5)
        ttk.Label(resume_frame, textvariable=self.benefice_net_var, font=('Arial', 22, 'bold'), foreground=COLORS['success']).grid(row=row, column=1, sticky='e', pady=15, padx=5)
        row += 1
        
        ttk.Separator(resume_frame, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky='ew', pady=20)
        row += 1
        
        # Boutons
        ttk.Button(resume_frame, text="💾 Enregistrer la journée", 
                  command=self.enregistrer_journee).grid(row=row, column=0, columnspan=2, sticky='ew', pady=10)
        row += 1
        
        ttk.Button(resume_frame, text="✅ Enregistrer et Jour suivant", 
                  command=self.enregistrer_et_jour_suivant).grid(row=row, column=0, columnspan=2, sticky='ew', pady=10)
        row += 1
        
        ttk.Button(resume_frame, text="🔄 Réinitialiser", 
                  command=self.reinitialiser_quantites).grid(row=row, column=0, columnspan=2, sticky='ew', pady=10)
        
        resume_frame.columnconfigure(0, weight=1)
        resume_frame.columnconfigure(1, weight=1)
    
    # ... (le reste du code reste identique) ...
    
    def charger_articles_saisie(self):
        """Charger les articles pour saisie"""
        for widget in self.articles_saisie_frame.winfo_children():
            widget.destroy()
        
        self.quantite_entries.clear()
        articles = self.article_controller.get_all_articles()
        
        if not articles:
            ttk.Label(self.articles_saisie_frame, 
                     text="Aucun article. Ajoutez des articles dans l'onglet 'Articles'.",
                     font=('Arial', 11),
                     foreground=COLORS['danger']).pack(pady=20)
            return
        
        # En-tête
        header = ttk.Frame(self.articles_saisie_frame)
        header.pack(fill='x', pady=(0, 10))
        
        ttk.Label(header, text="Article", font=('Arial', 11, 'bold'), width=30).pack(side='left', padx=10)
        ttk.Label(header, text="Prix", font=('Arial', 11, 'bold'), width=12).pack(side='left', padx=10)
        ttk.Label(header, text="Quantité vendue", font=('Arial', 11, 'bold'), width=15).pack(side='left', padx=10)
        
        ttk.Separator(self.articles_saisie_frame, orient='horizontal').pack(fill='x', pady=5)
        
        # Articles
        for idx, article in enumerate(articles):
            article_frame = ttk.Frame(self.articles_saisie_frame)
            article_frame.pack(fill='x', pady=8, padx=5)
            
            bg_color = '#F9FAFB' if idx % 2 == 0 else '#FFFFFF'
            
            nom_label = tk.Label(article_frame, text=article['nom'], 
                                font=('Arial', 11), 
                                width=30, anchor='w',
                                bg=bg_color)
            nom_label.pack(side='left', padx=10)
            
            prix_label = tk.Label(article_frame, 
                                 text=format_currency(article['prix_vente']), 
                                 font=('Arial', 11),
                                 width=12,
                                 fg=COLORS['success'],
                                 bg=bg_color)
            prix_label.pack(side='left', padx=10)
            
            quantite_var = tk.StringVar()
            quantite = self.vente_controller.get_quantite(self.date_selectionnee, article['id'])
            quantite_var.set(str(quantite))
            
            entry = ttk.Entry(article_frame, textvariable=quantite_var, 
                            width=15, font=('Arial', 12), justify='center')
            entry.pack(side='left', padx=10)
            
            self.quantite_entries[article['id']] = {
                'var': quantite_var,
                'entry': entry,
                'article': article
            }
            
            entry.bind('<FocusOut>', lambda e, aid=article['id']: self.enregistrer_quantite_auto(aid))
            entry.bind('<Return>', lambda e, aid=article['id']: self.enregistrer_quantite_auto(aid))
        
        self.calculer_totaux()
    
    def enregistrer_quantite_auto(self, article_id):
        """Enregistrer automatiquement"""
        try:
            quantite_str = self.quantite_entries[article_id]['var'].get()
            quantite = int(quantite_str) if quantite_str else 0
            
            if quantite < 0:
                quantite = 0
                self.quantite_entries[article_id]['var'].set('0')
            
            self.vente_controller.save_vente(self.date_selectionnee, article_id, quantite)
            self.calculer_totaux()
            
        except ValueError:
            self.quantite_entries[article_id]['var'].set('0')
            self.show_warning("Attention", "Veuillez entrer un nombre valide!")
    
    def charger_charges(self):
        """Charger les charges"""
        self.charges_listbox.delete(0, tk.END)
        charges = self.charge_controller.get_charges_jour(self.date_selectionnee)
        
        for charge in charges:
            self.charges_listbox.insert(tk.END, 
                f"{charge['description']} - {format_currency(charge['montant'])} [ID:{charge['id']}]")
        
        self.calculer_totaux()
    
    def ajouter_charge(self):
        """Ajouter une charge"""
        description = self.charge_desc_var.get().strip()
        montant_str = self.charge_montant_var.get()
        
        if not description:
            self.show_warning("Attention", "Entrez une description!")
            return
        
        try:
            montant = float(montant_str)
            if montant <= 0:
                raise ValueError("Le montant doit être positif")
            
            self.charge_controller.add_charge_journaliere(self.date_selectionnee, description, montant)
            self.charge_desc_var.set('')
            self.charge_montant_var.set('')
            self.charger_charges()
            
        except ValueError as e:
            self.show_error("Erreur", f"Montant invalide: {e}")
    
    def supprimer_charge(self):
        """Supprimer une charge"""
        selection = self.charges_listbox.curselection()
        if not selection:
            self.show_warning("Attention", "Sélectionnez une charge!")
            return
        
        texte = self.charges_listbox.get(selection[0])
        charge_id = int(texte.split('[ID:')[1].split(']')[0])
        
        if self.confirm("Confirmation", "Supprimer cette charge?"):
            self.charge_controller.delete_charge(charge_id)
            self.charger_charges()
    
    def calculer_totaux(self):
        """Calculer les totaux"""
        quantites_dict = {
            aid: {
                'quantite': data['var'].get(),
                'prix_achat': data['article']['prix_achat'],
                'prix_vente': data['article']['prix_vente']
            }
            for aid, data in self.quantite_entries.items()
        }
        
        totaux = self.vente_controller.calculate_totaux_jour(self.date_selectionnee, quantites_dict)
        
        self.recette_brute_var.set(format_currency(totaux['recette_brute']))
        self.cout_achat_var.set(format_currency(totaux['cout_achat']))
        self.benefice_brut_var.set(format_currency(totaux['benefice_brut']))
        self.charges_var.set(format_currency(totaux['total_charges']))
        self.charges_journalieres_var.set(format_currency(totaux['charges_journalieres_mensuelles']))
        self.benefice_net_var.set(format_currency(totaux['benefice_net']))
    
    def jour_precedent(self):
        """Jour précédent"""
        self.date_selectionnee -= timedelta(days=1)
        self.date_var.set(format_date(self.date_selectionnee))
        self.charger_articles_saisie()
        self.charger_charges()
    
    def jour_suivant(self):
        """Jour suivant"""
        self.date_selectionnee += timedelta(days=1)
        self.date_var.set(format_date(self.date_selectionnee))
        self.charger_articles_saisie()
        self.charger_charges()
    
    def aller_aujourdhui(self):
        """Aujourd'hui"""
        self.date_selectionnee = date.today()
        self.date_var.set(format_date(self.date_selectionnee))
        self.charger_articles_saisie()
        self.charger_charges()
    
    def enregistrer_journee(self):
        """Enregistrer"""
        self.show_success("Succès", 
            f"Ventes du {format_date(self.date_selectionnee)} enregistrées!\n\n" +
            f"Bénéfice net : {self.benefice_net_var.get()}")
    
    def enregistrer_et_jour_suivant(self):
        """Enregistrer et passer au jour suivant"""
        if self.confirm("Confirmation", 
            f"Enregistrer les ventes du {format_date(self.date_selectionnee)} et passer au jour suivant?"):
            
            self.show_success("Succès", 
                f"Journée enregistrée!\nBénéfice net : {self.benefice_net_var.get()}")
            
            self.jour_suivant()
    
    def reinitialiser_quantites(self):
        """Réinitialiser"""
        if self.confirm("Confirmation", 
            "Remettre toutes les quantités à 0 pour ce jour?"):
            
            articles = self.article_controller.get_all_articles()
            for article in articles:
                self.vente_controller.save_vente(self.date_selectionnee, article['id'], 0)
            
            charges = self.charge_controller.get_charges_jour(self.date_selectionnee)
            for charge in charges:
                self.charge_controller.delete_charge(charge['id'])
            
            self.charger_articles_saisie()
            self.charger_charges()
            self.show_success("Succès", "Quantités réinitialisées!")