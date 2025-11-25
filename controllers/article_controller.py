"""
Contrôleur Article - Logique métier des articles
"""

from models import ArticleModel
from utils.validators import validate_price, validate_non_empty


class ArticleController:
    """Gestion de la logique métier des articles"""
    
    def __init__(self):
        self.model = ArticleModel()
    
    def create_article(self, nom, prix_achat, prix_vente):
        """Créer un article avec validation"""
        # Validation
        validate_non_empty(nom, "Nom de l'article")
        validate_price(prix_achat, "Prix d'achat")
        validate_price(prix_vente, "Prix de vente")
        
        # Créer
        article_id = self.model.create(nom.strip(), prix_achat, prix_vente)
        return article_id
    
    def update_article(self, article_id, nom, prix_achat, prix_vente):
        """Modifier un article"""
        validate_non_empty(nom, "Nom de l'article")
        validate_price(prix_achat, "Prix d'achat")
        validate_price(prix_vente, "Prix de vente")
        
        return self.model.update(article_id, nom.strip(), prix_achat, prix_vente)
    
    def delete_article(self, article_id):
        """Supprimer un article"""
        return self.model.delete(article_id)
    
    def get_all_articles(self):
        """Récupérer tous les articles"""
        return self.model.get_all()
    
    def get_article(self, article_id):
        """Récupérer un article"""
        return self.model.get_by_id(article_id)
    
    def delete_all_articles(self):
        """Supprimer tous les articles"""
        return self.model.delete_all()
    
    def calculate_margin(self, prix_achat, prix_vente):
        """Calculer la marge"""
        marge = prix_vente - prix_achat
        marge_pct = (marge / prix_achat * 100) if prix_achat > 0 else 0
        return marge, marge_pct
    
    def is_margin_negative(self, prix_achat, prix_vente):
        """Vérifier si la marge est négative"""
        return prix_vente < prix_achat