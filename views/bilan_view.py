"""
Vue Bilan - Bilan mensuel complet (Interface centrée)
"""

import tkinter as tk
from tkinter import ttk
from datetime import date, timedelta
from .base_view import BaseView
from controllers import BilanController, ChargeController
from utils.formatters import format_currency, format_date, format_month
from utils.export import exporter_bilan_pdf
from config.settings import COLORS


class BilanView(BaseView):
    """Vue pour le bilan mensuel"""
    
    def __init__(self, parent):
        self.bilan_controller = BilanController()
        self.charge_controller = ChargeController()
        self.mois_selectionne = date.today().replace(day=1)
        self.charges_fixes_vars = {}
        super().__init__(parent)
    
    def setup_ui(self):
        """Créer l'interface (UNE SEULE COLONNE CENTRÉE)"""
        # Canvas avec scrollbar
        main_canvas = tk.Canvas(self.frame, highlightthickness=0, bd=0)
        main_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=main_canvas.yview)
        
        # Frame scrollable CENTRÉ
        scrollable_frame = ttk.Frame(main_canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        canvas_window = main_canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        # Centrer le contenu horizontalement
        def _on_canvas_configure(event):
            canvas_width = event.width
            frame_width = scrollable_frame.winfo_reqwidth()
            # Centrer si le frame est plus petit que le canvas
            x_position = max(0, (canvas_width - frame_width) // 2)
            main_canvas.coords(canvas_window, x_position, 0)
            # Si le frame est plus grand, utiliser toute la largeur
            if frame_width < canvas_width:
                main_canvas.itemconfig(canvas_window, width=canvas_width)
        
        main_canvas.bind('<Configure>', _on_canvas_configure)
        
        # ✅ TOUT LE CONTENU DANS UNE SEULE COLONNE
        container = ttk.Frame(scrollable_frame, padding=10)
        container.pack(fill='both', expand=True)
        
        self.create_month_selector(container)
        self.create_charges_fixes(container)
        self.create_salaires(container)
        self.create_resume_financier(container)
        self.create_quantites_vendues(container)
        self.create_depenses_journalieres(container)
        self.create_export_button(container)
        
        # Pack sans espace
        main_canvas.pack(side="left", fill="both", expand=True)
        main_scrollbar.pack(side="right", fill="y")
        
        self.charger_bilan()
    
    def create_month_selector(self, parent):
        """Sélecteur de mois"""
        mois_frame = ttk.LabelFrame(parent, text="📅 Sélection du mois", padding=15)
        mois_frame.pack(fill='x', pady=(0, 15))
        
        mois_controls = ttk.Frame(mois_frame)
        mois_controls.pack()
        
        ttk.Button(mois_controls, text="◀ Mois précédent", 
                command=self.mois_precedent).pack(side='left', padx=5)
        
        self.mois_var = tk.StringVar(value=format_month(self.mois_selectionne))
        mois_label = ttk.Label(mois_controls, textvariable=self.mois_var, 
                            font=('Arial', 14, 'bold'), foreground=COLORS['primary'])
        mois_label.pack(side='left', padx=15)
        
        ttk.Button(mois_controls, text="Mois suivant ▶", 
                command=self.mois_suivant).pack(side='left', padx=5)
        ttk.Button(mois_controls, text="Mois actuel", 
                command=self.aller_mois_actuel).pack(side='left', padx=20)
        ttk.Button(mois_controls, text="🔄 Actualiser", 
                command=self.charger_bilan,
                style='Big.TButton').pack(side='left', padx=20)
    
    def create_charges_fixes(self, parent):
        """Charges fixes mensuelles"""
        charges_frame = ttk.LabelFrame(parent, text="💰 Charges fixes mensuelles", padding=15)
        charges_frame.pack(fill='x', pady=(0, 15))
        
        charges_list = [
            ('loyer', 'Loyer du local'),
            ('electricite', 'Électricité (STEG)'),
            ('eau', 'Eau (SONEDE)'),
            ('impot', 'Impôt'),
            ('municipalite', 'Municipalité'),
            ('terrasse', 'Terrasse'),
            ('internet', 'Internet'),
            ('autres', 'Autres')
        ]
        
        row = 0
        for key, label in charges_list:
            ttk.Label(charges_frame, text=f"{label}:", 
                    font=('Arial', 10)).grid(row=row, column=0, sticky='w', padx=5, pady=5)
            var = tk.StringVar(value="0")
            self.charges_fixes_vars[key] = var
            ttk.Entry(charges_frame, textvariable=var, 
                    width=15, font=('Arial', 10)).grid(row=row, column=1, padx=5, pady=5)
            ttk.Label(charges_frame, text="DT").grid(row=row, column=2, sticky='w', padx=5, pady=5)
            row += 1
        
        ttk.Label(charges_frame, text="Description (Autres):", 
                font=('Arial', 10)).grid(row=row, column=0, sticky='w', padx=5, pady=5)
        self.autres_description_var = tk.StringVar()
        ttk.Entry(charges_frame, textvariable=self.autres_description_var, 
                width=40, font=('Arial', 10)).grid(row=row, column=1, columnspan=2, sticky='w', padx=5, pady=5)
        row += 1
        
        ttk.Button(charges_frame, text="💾 Enregistrer charges fixes", 
                command=self.enregistrer_charges_fixes,
                style='Big.TButton').grid(row=row, column=0, columnspan=3, pady=15)
    
    def create_salaires(self, parent):
        """Salaires des employés"""
        salaires_frame = ttk.LabelFrame(parent, text="👥 Salaires des employés", padding=15)
        salaires_frame.pack(fill='x', pady=(0, 15))
        
        input_salaire_frame = ttk.Frame(salaires_frame)
        input_salaire_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(input_salaire_frame, text="Nom de l'employé:", 
                font=('Arial', 10)).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.salaire_nom_var = tk.StringVar()
        ttk.Entry(input_salaire_frame, textvariable=self.salaire_nom_var, 
                width=25, font=('Arial', 10)).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_salaire_frame, text="Montant (DT):", 
                font=('Arial', 10)).grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.salaire_montant_var = tk.StringVar()
        ttk.Entry(input_salaire_frame, textvariable=self.salaire_montant_var, 
                width=15, font=('Arial', 10)).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(input_salaire_frame, text="➕ Ajouter salaire", 
                command=self.ajouter_salaire).grid(row=0, column=4, padx=10, pady=5)
        
        self.salaires_listbox = tk.Listbox(salaires_frame, height=4, font=('Arial', 10))
        self.salaires_listbox.pack(fill='x', pady=(0, 10))
        
        ttk.Button(salaires_frame, text="🗑️ Supprimer salaire sélectionné", 
                command=self.supprimer_salaire).pack()
    
    def create_resume_financier(self, parent):
        """Résumé financier du mois"""
        resume_frame = ttk.LabelFrame(parent, text="💵 Résumé financier du mois", padding=20)
        resume_frame.pack(fill='x', pady=(0, 15))
        
        self.mois_recette_var = tk.StringVar(value="0.00 DT")
        self.mois_cout_var = tk.StringVar(value="0.00 DT")
        self.mois_benefice_brut_var = tk.StringVar(value="0.00 DT")
        self.mois_charges_jour_var = tk.StringVar(value="0.00 DT")
        self.mois_charges_fixes_var = tk.StringVar(value="0.00 DT")
        self.mois_salaires_var = tk.StringVar(value="0.00 DT")
        self.mois_total_depenses_var = tk.StringVar(value="0.00 DT")
        self.mois_benefice_net_var = tk.StringVar(value="0.00 DT")
        
        resume_grid = ttk.Frame(resume_frame)
        resume_grid.pack(fill='x')
        
        row = 0
        ttk.Label(resume_grid, text="Recette brute", font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=8, padx=5)
        ttk.Label(resume_grid, textvariable=self.mois_recette_var, font=('Arial', 11, 'bold'), foreground=COLORS['info']).grid(row=row, column=1, sticky='e', pady=8, padx=5)
        row += 1
        
        ttk.Label(resume_grid, text="Coût d'achat", font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=8, padx=5)
        ttk.Label(resume_grid, textvariable=self.mois_cout_var, font=('Arial', 11, 'bold'), foreground=COLORS['danger']).grid(row=row, column=1, sticky='e', pady=8, padx=5)
        row += 1
        
        ttk.Label(resume_grid, text="Bénéfice brut", font=('Arial', 11)).grid(row=row, column=0, sticky='w', pady=8, padx=5)
        ttk.Label(resume_grid, textvariable=self.mois_benefice_brut_var, font=('Arial', 11, 'bold'), foreground=COLORS['success']).grid(row=row, column=1, sticky='e', pady=8, padx=5)
        row += 1
        
        ttk.Separator(resume_grid, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky='ew', pady=10)
        row += 1
        
        ttk.Label(resume_grid, text="Dépenses journalières", font=('Arial', 10, 'italic')).grid(row=row, column=0, sticky='w', pady=5, padx=15)
        ttk.Label(resume_grid, textvariable=self.mois_charges_jour_var, font=('Arial', 10, 'italic'), foreground=COLORS['danger']).grid(row=row, column=1, sticky='e', pady=5, padx=5)
        row += 1
        
        ttk.Label(resume_grid, text="Charges fixes", font=('Arial', 10, 'italic')).grid(row=row, column=0, sticky='w', pady=5, padx=15)
        ttk.Label(resume_grid, textvariable=self.mois_charges_fixes_var, font=('Arial', 10, 'italic'), foreground=COLORS['danger']).grid(row=row, column=1, sticky='e', pady=5, padx=5)
        row += 1
        
        ttk.Label(resume_grid, text="Salaires", font=('Arial', 10, 'italic')).grid(row=row, column=0, sticky='w', pady=5, padx=15)
        ttk.Label(resume_grid, textvariable=self.mois_salaires_var, font=('Arial', 10, 'italic'), foreground=COLORS['danger']).grid(row=row, column=1, sticky='e', pady=5, padx=5)
        row += 1
        
        ttk.Label(resume_grid, text="TOTAL DÉPENSES", font=('Arial', 11, 'bold')).grid(row=row, column=0, sticky='w', pady=8, padx=5)
        ttk.Label(resume_grid, textvariable=self.mois_total_depenses_var, font=('Arial', 11, 'bold'), foreground=COLORS['danger']).grid(row=row, column=1, sticky='e', pady=8, padx=5)
        row += 1
        
        ttk.Separator(resume_grid, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky='ew', pady=15)
        row += 1
        
        ttk.Label(resume_grid, text="BÉNÉFICE NET DU MOIS", font=('Arial', 14, 'bold')).grid(row=row, column=0, sticky='w', pady=15, padx=5)
        ttk.Label(resume_grid, textvariable=self.mois_benefice_net_var, font=('Arial', 18, 'bold'), foreground=COLORS['success']).grid(row=row, column=1, sticky='e', pady=15, padx=5)
        
        resume_grid.columnconfigure(0, weight=1)
        resume_grid.columnconfigure(1, weight=1)
    
    def create_quantites_vendues(self, parent):
        """Quantités vendues par article"""
        quantites_frame = ttk.LabelFrame(parent, text="📦 Quantités vendues par article", padding=15)
        quantites_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        columns_q = ('Article', 'Quantité', 'Prix Unitaire', 'Total')
        self.quantites_tree = ttk.Treeview(quantites_frame, columns=columns_q, show='headings', height=10)
        
        self.quantites_tree.heading('Article', text='Article')
        self.quantites_tree.heading('Quantité', text='Quantité')
        self.quantites_tree.heading('Prix Unitaire', text='Prix Unitaire')
        self.quantites_tree.heading('Total', text='Total')
        
        self.quantites_tree.column('Article', width=300)
        self.quantites_tree.column('Quantité', width=150, anchor='center')
        self.quantites_tree.column('Prix Unitaire', width=150, anchor='center')
        self.quantites_tree.column('Total', width=150, anchor='center')
        
        scrollbar_q = ttk.Scrollbar(quantites_frame, orient='vertical', command=self.quantites_tree.yview)
        self.quantites_tree.configure(yscrollcommand=scrollbar_q.set)
        
        self.quantites_tree.pack(side='left', fill='both', expand=True)
        scrollbar_q.pack(side='right', fill='y')
    
    def create_depenses_journalieres(self, parent):
        """Liste des dépenses journalières"""
        depenses_frame = ttk.LabelFrame(parent, text="💸 Toutes les dépenses journalières du mois", padding=15)
        depenses_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        columns_d = ('Date', 'Description', 'Montant')
        self.depenses_tree = ttk.Treeview(depenses_frame, columns=columns_d, show='headings', height=10)
        
        self.depenses_tree.heading('Date', text='Date')
        self.depenses_tree.heading('Description', text='Description')
        self.depenses_tree.heading('Montant', text='Montant (DT)')
        
        self.depenses_tree.column('Date', width=150, anchor='center')
        self.depenses_tree.column('Description', width=450)
        self.depenses_tree.column('Montant', width=150, anchor='center')
        
        scrollbar_d = ttk.Scrollbar(depenses_frame, orient='vertical', command=self.depenses_tree.yview)
        self.depenses_tree.configure(yscrollcommand=scrollbar_d.set)
        
        self.depenses_tree.pack(side='left', fill='both', expand=True)
        scrollbar_d.pack(side='right', fill='y')
    
    def create_export_button(self, parent):
        """Bouton d'export"""
        ttk.Button(parent, text="📄 Exporter le bilan en PDF", 
                command=self.exporter_bilan,
                style='Big.TButton').pack(pady=20)
    
    def charger_bilan(self):
        """Charger le bilan complet"""
        charges_fixes = self.charge_controller.get_charges_fixes(self.mois_selectionne)
        if charges_fixes:
            for key in self.charges_fixes_vars:
                self.charges_fixes_vars[key].set(str(float(charges_fixes[key])))
            self.autres_description_var.set(charges_fixes.get('autres_description', ''))
        else:
            for key in self.charges_fixes_vars:
                self.charges_fixes_vars[key].set('0')
            self.autres_description_var.set('')
        
        self.charger_salaires()
        bilan = self.bilan_controller.get_bilan_complet(self.mois_selectionne)
        financier = self.bilan_controller.calculate_bilan_financier(bilan)
        
        self.mois_recette_var.set(format_currency(financier['recette_brute']))
        self.mois_cout_var.set(format_currency(financier['cout_achat']))
        self.mois_benefice_brut_var.set(format_currency(financier['benefice_brut']))
        self.mois_charges_jour_var.set(format_currency(financier['charges_journalieres']))
        self.mois_charges_fixes_var.set(format_currency(financier['charges_fixes']))
        self.mois_salaires_var.set(format_currency(financier['total_salaires']))
        self.mois_total_depenses_var.set(format_currency(financier['total_depenses']))
        self.mois_benefice_net_var.set(format_currency(financier['benefice_net']))
        
        for item in self.quantites_tree.get_children():
            self.quantites_tree.delete(item)
        
        for article in bilan['quantites_articles']:
            quantite = int(article['quantite_totale'])
            prix = float(article['prix_vente'])
            total = quantite * prix
            self.quantites_tree.insert('', 'end', values=(
                article['nom'],
                quantite,
                format_currency(prix),
                format_currency(total)
            ))
        
        for item in self.depenses_tree.get_children():
            self.depenses_tree.delete(item)
        
        for depense in bilan['depenses_journalieres']:
            self.depenses_tree.insert('', 'end', values=(
                format_date(depense['date_charge']),
                depense['description'],
                f"{float(depense['montant']):.2f}"
            ))
    
    def charger_salaires(self):
        """Charger les salaires"""
        self.salaires_listbox.delete(0, tk.END)
        salaires = self.charge_controller.get_salaires(self.mois_selectionne)
        
        for salaire in salaires:
            self.salaires_listbox.insert(tk.END, 
                f"{salaire['nom_employe']} - {format_currency(salaire['montant'])} [ID:{salaire['id']}]")
    
    def enregistrer_charges_fixes(self):
        """Enregistrer les charges fixes"""
        try:
            charges_dict = {
                key: float(var.get() or 0)
                for key, var in self.charges_fixes_vars.items()
            }
            autres_desc = self.autres_description_var.get().strip()
            
            self.charge_controller.save_charges_fixes(self.mois_selectionne, charges_dict, autres_desc)
            
            self.show_success("Succès", "Charges fixes enregistrées!")
            self.charger_bilan()
            
        except ValueError:
            self.show_error("Erreur", "Veuillez entrer des montants valides!")
    
    def ajouter_salaire(self):
        """Ajouter un salaire"""
        nom = self.salaire_nom_var.get().strip()
        montant_str = self.salaire_montant_var.get()
        
        try:
            montant = float(montant_str)
            self.charge_controller.add_salaire(self.mois_selectionne, nom, montant)
            self.salaire_nom_var.set('')
            self.salaire_montant_var.set('')
            self.charger_salaires()
            self.charger_bilan()
        except Exception as e:
            self.show_error("Erreur", str(e))
    
    def supprimer_salaire(self):
        """Supprimer un salaire"""
        selection = self.salaires_listbox.curselection()
        if not selection:
            self.show_warning("Attention", "Sélectionnez un salaire!")
            return
        
        texte = self.salaires_listbox.get(selection[0])
        salaire_id = int(texte.split('[ID:')[1].split(']')[0])
        
        if self.confirm("Confirmation", "Supprimer ce salaire?"):
            self.charge_controller.delete_salaire(salaire_id)
            self.charger_salaires()
            self.charger_bilan()
    
    def mois_precedent(self):
        """Mois précédent"""
        if self.mois_selectionne.month == 1:
            self.mois_selectionne = date(self.mois_selectionne.year - 1, 12, 1)
        else:
            self.mois_selectionne = date(self.mois_selectionne.year, self.mois_selectionne.month - 1, 1)
        self.mois_var.set(format_month(self.mois_selectionne))
        self.charger_bilan()
    
    def mois_suivant(self):
        """Mois suivant"""
        if self.mois_selectionne.month == 12:
            self.mois_selectionne = date(self.mois_selectionne.year + 1, 1, 1)
        else:
            self.mois_selectionne = date(self.mois_selectionne.year, self.mois_selectionne.month + 1, 1)
        self.mois_var.set(format_month(self.mois_selectionne))
        self.charger_bilan()
    
    def aller_mois_actuel(self):
        """Mois actuel"""
        self.mois_selectionne = date.today().replace(day=1)
        self.mois_var.set(format_month(self.mois_selectionne))
        self.charger_bilan()
    
    def exporter_bilan(self):
        """Exporter le bilan en PDF"""
        from utils.export import exporter_bilan_pdf
        
        # Récupérer les données des quantités vendues
        quantites_data = []
        for item in self.quantites_tree.get_children():
            values = self.quantites_tree.item(item)['values']
            quantites_data.append(values)
        
        # Récupérer les données des dépenses journalières
        depenses_data = []
        for item in self.depenses_tree.get_children():
            values = self.depenses_tree.item(item)['values']
            depenses_data.append(values)
        
        # Récupérer les totaux depuis les variables
        totaux = {
            'recette_totale': float(self.mois_recette_var.get().replace(' DT', '').replace(',', '')),
            'cout_achat': float(self.mois_cout_var.get().replace(' DT', '').replace(',', '')),
            'benefice_brut': float(self.mois_benefice_brut_var.get().replace(' DT', '').replace(',', '')),
            'charges_jour': float(self.mois_charges_jour_var.get().replace(' DT', '').replace(',', '')),
            'charges_fixes': float(self.mois_charges_fixes_var.get().replace(' DT', '').replace(',', '')),
            'salaires': float(self.mois_salaires_var.get().replace(' DT', '').replace(',', '')),
            'total_charges': float(self.mois_total_depenses_var.get().replace(' DT', '').replace(',', '')),
            'benefice_net': float(self.mois_benefice_net_var.get().replace(' DT', '').replace(',', ''))
        }
        
        # Appeler la fonction d'export PDF
        exporter_bilan_pdf(
            self.bilan_controller,
            self.mois_selectionne,
            quantites_data,
            depenses_data,
            totaux
        )

    def refresh(self):
        """Rafraîchir la vue"""
        self.charger_bilan()