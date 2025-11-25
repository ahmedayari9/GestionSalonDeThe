"""
Modèle Salaire - Gestion des salaires mensuels
"""

from .base_model import BaseModel
from decimal import Decimal


class SalaireModel(BaseModel):
    """Gestion des salaires"""
    
    def create(self, mois, nom_employe, montant):
        """Ajouter un salaire"""
        query = "INSERT INTO salaires_mensuels (mois, nom_employe, montant) VALUES (%s, %s, %s)"
        return self._execute_query(query, (mois, nom_employe, montant))
    
    def get_by_month(self, mois):
        """Récupérer les salaires d'un mois"""
        query = "SELECT * FROM salaires_mensuels WHERE mois = %s ORDER BY nom_employe"
        return self._execute_query(query, (mois,), fetch_all=True)
    
    def delete(self, salaire_id):
        """Supprimer un salaire"""
        query = "DELETE FROM salaires_mensuels WHERE id = %s"
        return self._execute_query(query, (salaire_id,))
    
    def get_total_by_month(self, mois):
        """Total des salaires d'un mois"""
        salaires = self.get_by_month(mois)
        return sum(Decimal(str(s['montant'])) for s in salaires)