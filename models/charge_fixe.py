"""
Modèle ChargeFixe - Gestion des charges fixes mensuelles
"""

from .base_model import BaseModel


class ChargeFixeModel(BaseModel):
    """Gestion des charges fixes mensuelles"""
    
    def save(self, mois, loyer, electricite, eau, impot, municipalite, terrasse, internet, autres, autres_desc):
        """Enregistrer ou mettre à jour les charges fixes"""
        query = """
            INSERT INTO charges_fixes_mensuelles 
            (mois, loyer, electricite, eau, impot, municipalite, terrasse, internet, autres, autres_description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            loyer = %s, electricite = %s, eau = %s, impot = %s, 
            municipalite = %s, terrasse = %s, internet = %s, autres = %s, autres_description = %s
        """
        params = (
            mois, loyer, electricite, eau, impot, municipalite, terrasse, internet, autres, autres_desc,
            loyer, electricite, eau, impot, municipalite, terrasse, internet, autres, autres_desc
        )
        return self._execute_query(query, params)
    
    def get_by_month(self, mois):
        """Récupérer les charges fixes d'un mois"""
        query = "SELECT * FROM charges_fixes_mensuelles WHERE mois = %s"
        return self._execute_query(query, (mois,), fetch_one=True)