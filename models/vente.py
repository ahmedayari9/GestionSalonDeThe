"""
Modèle Vente - Gestion des ventes quotidiennes
"""

from .base_model import BaseModel
from datetime import date, timedelta


class VenteModel(BaseModel):
    """Gestion des ventes"""
    
    def save(self, date_vente, article_id, quantite):
        """Enregistrer ou mettre à jour une vente"""
        query = """
            INSERT INTO ventes (date_vente, article_id, quantite) 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE quantite = %s
        """
        return self._execute_query(query, (date_vente, article_id, quantite, quantite))
    
    def get_by_date(self, date_vente):
        """Récupérer les ventes d'une date"""
        query = """
            SELECT v.*, a.nom, a.prix_achat, a.prix_vente
            FROM ventes v
            JOIN articles a ON v.article_id = a.id
            WHERE v.date_vente = %s
        """
        return self._execute_query(query, (date_vente,), fetch_all=True)
    
    def get_quantite(self, date_vente, article_id):
        """Récupérer la quantité vendue"""
        query = "SELECT quantite FROM ventes WHERE date_vente = %s AND article_id = %s"
        result = self._execute_query(query, (date_vente, article_id), fetch_one=True)
        return result['quantite'] if result else 0
    
    def delete_by_date(self, date_vente):
        """Supprimer toutes les ventes d'une date"""
        query = "DELETE FROM ventes WHERE date_vente = %s"
        return self._execute_query(query, (date_vente,))
    
    def get_historique(self, limit=30):
        """Récupérer l'historique des ventes"""
        query = """
            SELECT 
                v.date_vente,
                SUM(v.quantite * a.prix_vente) as recette_brute,
                SUM(v.quantite * a.prix_achat) as cout_achat,
                SUM(v.quantite * (a.prix_vente - a.prix_achat)) as benefice_brut
            FROM ventes v
            JOIN articles a ON v.article_id = a.id
            GROUP BY v.date_vente
            ORDER BY v.date_vente DESC
            LIMIT %s
        """
        return self._execute_query(query, (limit,), fetch_all=True)
    
    def get_ventes_mois(self, premier_jour, dernier_jour):
        """Récupérer les ventes d'un mois"""
        query = """
            SELECT 
                SUM(v.quantite * a.prix_vente) as recette_brute,
                SUM(v.quantite * a.prix_achat) as cout_achat,
                SUM(v.quantite * (a.prix_vente - a.prix_achat)) as benefice_brut
            FROM ventes v
            JOIN articles a ON v.article_id = a.id
            WHERE v.date_vente BETWEEN %s AND %s
        """
        return self._execute_query(query, (premier_jour, dernier_jour), fetch_one=True)
    
    def get_quantites_articles_mois(self, premier_jour, dernier_jour):
        """Quantités vendues par article pour un mois"""
        query = """
            SELECT a.nom, SUM(v.quantite) as quantite_totale, a.prix_vente
            FROM ventes v
            JOIN articles a ON v.article_id = a.id
            WHERE v.date_vente BETWEEN %s AND %s
            GROUP BY a.id, a.nom, a.prix_vente
            ORDER BY quantite_totale DESC
        """
        return self._execute_query(query, (premier_jour, dernier_jour), fetch_all=True)