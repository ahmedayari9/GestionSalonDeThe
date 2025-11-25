"""
Contrôleur Charge - Logique métier des charges
"""

from models import ChargeModel, ChargeFixeModel, SalaireModel
from utils.validators import validate_non_empty, validate_price


class ChargeController:
    """Gestion de la logique métier des charges"""
    
    def __init__(self):
        self.charge_model = ChargeModel()
        self.charge_fixe_model = ChargeFixeModel()
        self.salaire_model = SalaireModel()
    
    def add_charge_journaliere(self, date_charge, description, montant):
        """Ajouter une charge journalière"""
        validate_non_empty(description, "Description")
        validate_price(montant, "Montant")
        
        return self.charge_model.create(date_charge, description.strip(), montant)
    
    def get_charges_jour(self, date_charge):
        """Récupérer les charges d'un jour"""
        return self.charge_model.get_by_date(date_charge)
    
    def delete_charge(self, charge_id):
        """Supprimer une charge"""
        return self.charge_model.delete(charge_id)
    
    def save_charges_fixes(self, mois, charges_dict, autres_desc):
        """Enregistrer les charges fixes mensuelles"""
        return self.charge_fixe_model.save(
            mois,
            charges_dict.get('loyer', 0),
            charges_dict.get('electricite', 0),
            charges_dict.get('eau', 0),
            charges_dict.get('impot', 0),
            charges_dict.get('municipalite', 0),
            charges_dict.get('terrasse', 0),
            charges_dict.get('internet', 0),
            charges_dict.get('autres', 0),
            autres_desc
        )
    
    def get_charges_fixes(self, mois):
        """Récupérer les charges fixes"""
        return self.charge_fixe_model.get_by_month(mois)
    
    def add_salaire(self, mois, nom_employe, montant):
        """Ajouter un salaire"""
        validate_non_empty(nom_employe, "Nom de l'employé")
        validate_price(montant, "Montant")
        
        return self.salaire_model.create(mois, nom_employe.strip(), montant)
    
    def get_salaires(self, mois):
        """Récupérer les salaires"""
        return self.salaire_model.get_by_month(mois)
    
    def delete_salaire(self, salaire_id):
        """Supprimer un salaire"""
        return self.salaire_model.delete(salaire_id)