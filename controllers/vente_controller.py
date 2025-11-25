"""
Contrôleur Vente - Logique métier des ventes
"""

from models import VenteModel, ChargeModel
from decimal import Decimal
from datetime import date, timedelta


class VenteController:
    """Gestion de la logique métier des ventes"""
    
    def __init__(self):
        self.vente_model = VenteModel()
        self.charge_model = ChargeModel()
    
    def save_vente(self, date_vente, article_id, quantite):
        """Enregistrer une vente"""
        if quantite < 0:
            quantite = 0
        return self.vente_model.save(date_vente, article_id, quantite)
    
    def get_ventes_jour(self, date_vente):
        """Récupérer les ventes d'un jour"""
        return self.vente_model.get_by_date(date_vente)
    
    def get_quantite(self, date_vente, article_id):
        """Récupérer la quantité vendue"""
        return self.vente_model.get_quantite(date_vente, article_id)
    
    def calculate_totaux_jour(self, date_vente, quantites_dict):
        """Calculer les totaux d'un jour"""
        recette_brute = Decimal('0')
        cout_achat = Decimal('0')
        
        for article_id, data in quantites_dict.items():
            quantite = int(data['quantite'] or 0)
            prix_achat = Decimal(str(data['prix_achat']))
            prix_vente = Decimal(str(data['prix_vente']))
            
            recette_brute += prix_vente * quantite
            cout_achat += prix_achat * quantite
        
        benefice_brut = recette_brute - cout_achat
        
        # Charges
        total_charges = self.charge_model.get_total_by_date(date_vente)
        total_charges = Decimal(str(total_charges))
        
        benefice_net = benefice_brut - total_charges
        
        return {
            'recette_brute': recette_brute,
            'cout_achat': cout_achat,
            'benefice_brut': benefice_brut,
            'total_charges': total_charges,
            'benefice_net': benefice_net
        }
    
    def delete_jour(self, date_vente):
        """Supprimer toutes les ventes et charges d'un jour"""
        ventes_suppr = self.vente_model.delete_by_date(date_vente)
        charges_suppr = self.charge_model.delete_by_date(date_vente)
        return {'ventes': ventes_suppr, 'charges': charges_suppr}
    
    def get_historique(self, limit=30):
        """Récupérer l'historique avec charges"""
        historique = self.vente_model.get_historique(limit)
        
        # Ajouter les charges pour chaque jour
        for jour in historique:
            total_charges = self.charge_model.get_total_by_date(jour['date_vente'])
            jour['total_charges'] = total_charges
            jour['benefice_net'] = jour['benefice_brut'] - Decimal(str(total_charges))
        
        return historique