"""
Modèle Charge - Gestion des charges journalières
"""

from .base_model import BaseModel


class ChargeModel(BaseModel):
    """Gestion des charges journalières"""
    
    def create(self, date_charge, description, montant):
        """Ajouter une charge"""
        query = "INSERT INTO charges (date_charge, description, montant) VALUES (%s, %s, %s)"
        return self._execute_query(query, (date_charge, description, montant))
    
    def get_by_date(self, date_charge):
        """Récupérer les charges d'une date"""
        query = "SELECT * FROM charges WHERE date_charge = %s ORDER BY date_creation"
        return self._execute_query(query, (date_charge,), fetch_all=True)
    
    def delete(self, charge_id):
        """Supprimer une charge"""
        query = "DELETE FROM charges WHERE id = %s"
        return self._execute_query(query, (charge_id,))
    
    def delete_by_date(self, date_charge):
        """Supprimer toutes les charges d'une date"""
        query = "DELETE FROM charges WHERE date_charge = %s"
        return self._execute_query(query, (date_charge,))
    
    def get_total_by_date(self, date_charge):
        """Total des charges d'une date"""
        query = "SELECT SUM(montant) as total FROM charges WHERE date_charge = %s"
        result = self._execute_query(query, (date_charge,), fetch_one=True)
        return result['total'] if result and result['total'] else 0
    
    def get_charges_mois(self, premier_jour, dernier_jour):
        """Charges d'un mois"""
        query = """
            SELECT SUM(montant) as total_charges_journalieres
            FROM charges
            WHERE date_charge BETWEEN %s AND %s
        """
        result = self._execute_query(query, (premier_jour, dernier_jour), fetch_one=True)
        return result if result else {'total_charges_journalieres': 0}
    
    def get_liste_charges_mois(self, premier_jour, dernier_jour):
        """Liste détaillée des charges d'un mois"""
        query = """
            SELECT date_charge, description, montant
            FROM charges
            WHERE date_charge BETWEEN %s AND %s
            ORDER BY date_charge DESC
        """
        return self._execute_query(query, (premier_jour, dernier_jour), fetch_all=True)