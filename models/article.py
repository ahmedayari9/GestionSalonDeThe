"""
Modèle Article - Gestion des articles
"""

from .base_model import BaseModel


class ArticleModel(BaseModel):
    """Gestion des articles"""
    
    def create(self, nom, prix_achat, prix_vente):
        """Créer un article"""
        query = "INSERT INTO articles (nom, prix_achat, prix_vente) VALUES (%s, %s, %s)"
        return self._execute_query(query, (nom, prix_achat, prix_vente))
    
    def get_all(self, actif_only=True):
        """Récupérer tous les articles"""
        query = "SELECT * FROM articles"
        if actif_only:
            query += " WHERE actif = TRUE"
        query += " ORDER BY id ASC"
        return self._execute_query(query, fetch_all=True)
    
    def get_by_id(self, article_id):
        """Récupérer un article par ID"""
        query = "SELECT * FROM articles WHERE id = %s"
        return self._execute_query(query, (article_id,), fetch_one=True)
    
    def update(self, article_id, nom, prix_achat, prix_vente):
        """Modifier un article"""
        query = """
            UPDATE articles 
            SET nom = %s, prix_achat = %s, prix_vente = %s 
            WHERE id = %s
        """
        return self._execute_query(query, (nom, prix_achat, prix_vente, article_id))
    
    def delete(self, article_id):
        """Supprimer un article"""
        query = "DELETE FROM articles WHERE id = %s"
        return self._execute_query(query, (article_id,))
    
    def delete_all(self):
        """Supprimer tous les articles"""
        # Supprimer les ventes d'abord (CASCADE devrait le faire automatiquement)
        self._execute_query("DELETE FROM ventes")
        return self._execute_query("DELETE FROM articles")
    
    def get_count(self):
        """Compter les articles"""
        query = "SELECT COUNT(*) as count FROM articles WHERE actif = TRUE"
        result = self._execute_query(query, fetch_one=True)
        return result['count'] if result else 0