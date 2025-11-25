"""
Vue Historique - Historique des ventes
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from .base_view import BaseView
from controllers import VenteController
from utils.formatters import format_currency, format_date
from utils.export import export_historique_csv
from config.settings import COLORS


class HistoriqueView(BaseView):
    """Vue pour l'historique des ventes"""
    
    def __init__(self, parent):
        self.controller = VenteController()
        super().__init__(parent)
    
    def setup_ui(self):
        """Créer l'interface"""
        # Boutons
        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(btn_frame, text="🔄 Actualiser", command=self.charger_historique, 
                  style='Big.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text="📄 Exporter CSV", command=self.exporter_historique, 
                  style='Big.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🗑️ Supprimer jour sélectionné", command=self.supprimer_jour,
                  style='Big.TButton').pack(side='left', padx=5)
        
        # TreeView
        columns = ('Date', 'Recette Brute', 'Coût Achat', 'Bénéfice Brut', 'Charges', 'Bénéfice Net')
        self.historique_tree = ttk.Treeview(self.frame, columns=columns, show='headings', height=25)
        
        for col in columns:
            self.historique_tree.heading(col, text=col)
            self.historique_tree.column(col, width=180, anchor='center')
        
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.historique_tree.yview)
        self.historique_tree.configure(yscrollcommand=scrollbar.set)
        
        self.historique_tree.pack(side='left', fill='both', expand=True, padx=10)
        scrollbar.pack(side='right', fill='y')
        
        self.historique_tree.bind('<Double-1>', self.voir_details_jour)
        
        self.charger_historique()
    
    def charger_historique(self):
        """Charger l'historique"""
        for item in self.historique_tree.get_children():
            self.historique_tree.delete(item)
        
        historique = self.controller.get_historique(limit=90)
        
        for jour in historique:
            self.historique_tree.insert('', 'end', values=(
                format_date(jour['date_vente']),
                format_currency(jour['recette_brute']),
                format_currency(jour['cout_achat']),
                format_currency(jour['benefice_brut']),
                format_currency(jour['total_charges']),
                format_currency(jour['benefice_net'])
            ))
    
    def voir_details_jour(self, event):
        """Double-clic pour voir les détails"""
        selection = self.historique_tree.selection()
        if not selection:
            return
        
        item = self.historique_tree.item(selection[0])
        date_str = item['values'][0]
        
        # TODO: Basculer vers l'onglet ventes avec cette date
        self.show_success("Navigation", f"Voir détails du {date_str}\n\n(Fonctionnalité à implémenter)")
    
    def supprimer_jour(self):
        """Supprimer un jour"""
        selection = self.historique_tree.selection()
        if not selection:
            self.show_warning("Attention", "Veuillez sélectionner un jour!")
            return
        
        item = self.historique_tree.item(selection[0])
        date_str = item['values'][0]
        
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y').date()
        except Exception:
            self.show_error("Erreur", "Date invalide!")
            return
        
        if not self.confirm("⚠️ CONFIRMATION", 
            f"Supprimer toutes les ventes et charges du {date_str}?\n\n" +
            "CETTE ACTION EST IRRÉVERSIBLE!"):
            return
        
        if not self.confirm("⚠️ CONFIRMATION FINALE", "Êtes-vous absolument sûr?"):
            return
        
        try:
            resultat = self.controller.delete_jour(date_obj)
            ventes_suppr = resultat.get('ventes', 0)
            charges_suppr = resultat.get('charges', 0)
            
            self.show_success("Succès", 
                f"Suppression terminée:\n{ventes_suppr} vente(s) et {charges_suppr} charge(s) supprimées.")
            
            self.charger_historique()
            
        except Exception as e:
            self.show_error("Erreur", str(e))
    
    def exporter_historique(self):
        """Exporter l'historique"""
        historique = self.controller.get_historique(limit=365)
        filename = export_historique_csv(historique)
        if filename:
            self.show_success("Succès", f"Historique exporté:\n{filename}")
    
    def refresh(self):
        """Rafraîchir la vue"""
        self.charger_historique()