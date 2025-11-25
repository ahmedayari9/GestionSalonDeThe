"""
Contrôleur Bilan - Logique métier des bilans mensuels
"""

from models import VenteModel, ChargeModel, ChargeFixeModel, SalaireModel
from decimal import Decimal
from datetime import date, timedelta
from config.database import DatabaseConnection
from datetime import timedelta

class BilanController:
    """Gestion de la logique métier des bilans"""
    
    def __init__(self):
        self.vente_model = VenteModel()
        self.charge_model = ChargeModel()
        self.charge_fixe_model = ChargeFixeModel()
        self.salaire_model = SalaireModel()
        self.db = DatabaseConnection()

    
    def get_bilan_complet(self, mois):
        """Récupérer le bilan complet d'un mois"""
        # Calculer les bornes du mois
        premier_jour, dernier_jour = self._get_month_bounds(mois)
        
        # Ventes du mois
        ventes = self.vente_model.get_ventes_mois(premier_jour, dernier_jour)
        
        # Charges journalières
        charges_jour = self.charge_model.get_charges_mois(premier_jour, dernier_jour)
        
        # Charges fixes
        charges_fixes = self.charge_fixe_model.get_by_month(premier_jour) or {}
        
        # Salaires
        salaires = self.salaire_model.get_by_month(premier_jour)
        total_salaires = self.salaire_model.get_total_by_month(premier_jour)
        
        # Quantités vendues
        quantites_articles = self.vente_model.get_quantites_articles_mois(premier_jour, dernier_jour)
        
        # Liste des dépenses
        depenses_journalieres = self.charge_model.get_liste_charges_mois(premier_jour, dernier_jour)
        
        return {
            'ventes': ventes,
            'charges_journalieres': charges_jour,
            'charges_fixes': charges_fixes,
            'salaires': salaires,
            'total_salaires': total_salaires,
            'quantites_articles': quantites_articles,
            'depenses_journalieres': depenses_journalieres,
            'premier_jour': premier_jour,
            'dernier_jour': dernier_jour
        }
    
    def calculate_bilan_financier(self, bilan_data):
        """Calculer le bilan financier complet"""
        ventes = bilan_data['ventes']
        charges_jour = bilan_data['charges_journalieres']
        charges_fixes = bilan_data['charges_fixes']
        total_salaires = bilan_data['total_salaires']
        
        # Ventes
        recette = Decimal(str(ventes['recette_brute'] or 0))
        cout = Decimal(str(ventes['cout_achat'] or 0))
        benefice_brut = Decimal(str(ventes['benefice_brut'] or 0))
        
        # Charges journalières
        charges_journalieres = Decimal(str(charges_jour['total_charges_journalieres'] or 0))
        
        # Charges fixes
        total_charges_fixes = sum(
            Decimal(str(charges_fixes.get(key, 0)))
            for key in ['loyer', 'electricite', 'eau', 'impot', 'municipalite', 'terrasse', 'internet', 'autres']
        ) if charges_fixes else Decimal('0')
        
        # Total dépenses
        total_depenses = charges_journalieres + total_charges_fixes + total_salaires
        
        # Bénéfice net
        benefice_net = benefice_brut - total_depenses
        
        return {
            'recette_brute': recette,
            'cout_achat': cout,
            'benefice_brut': benefice_brut,
            'charges_journalieres': charges_journalieres,
            'charges_fixes': total_charges_fixes,
            'total_salaires': total_salaires,
            'total_depenses': total_depenses,
            'benefice_net': benefice_net
        }
    
    def _get_month_bounds(self, mois):
        """Calculer le premier et dernier jour du mois"""
        annee, mois_num = mois.year, mois.month
        premier_jour = date(annee, mois_num, 1)
        
        if mois_num == 12:
            dernier_jour = date(annee + 1, 1, 1) - timedelta(days=1)
        else:
            dernier_jour = date(annee, mois_num + 1, 1) - timedelta(days=1)
        
        return premier_jour, dernier_jour
    
    def get_charges_fixes_mois(self, mois_date):
        """Récupérer toutes les charges fixes du mois"""
        try:
            premier_jour = mois_date.replace(day=1)
            
            print("\n" + "="*60)
            print(f"🔍 DEBUG get_charges_fixes_mois")
            print(f"📅 Date recherchée: {premier_jour}")
            print("="*60)
            
            charges = []
            
            # Obtenir la connexion et créer le curseur
            conn = self.db.get_connection()
            cursor = conn.cursor()
            
            # TEST 1: Voir TOUTES les entrées de la table
            query_all_entries = "SELECT mois FROM charges_fixes_mensuelles"
            cursor.execute(query_all_entries)
            all_dates = cursor.fetchall()
            print(f"\n📋 Dates dans charges_fixes_mensuelles:")
            for d in all_dates:
                print(f"   - {d[0]}")
            
            # TEST 2: Compter les entrées pour ce mois
            query_test = "SELECT COUNT(*) FROM charges_fixes_mensuelles WHERE mois = %s"
            cursor.execute(query_test, (premier_jour,))
            count = cursor.fetchone()[0]
            print(f"\n✅ Entrées trouvées pour {premier_jour}: {count}")
            
            if count == 0:
                print("⚠️  AUCUNE DONNÉE - Enregistrez d'abord les charges fixes!")
                cursor.close()
                return []
            
            # Récupérer les données
            query_all = """
                SELECT 
                    loyer, electricite, eau, impot, municipalite, 
                    terrasse, internet, autres, autres_description, mois
                FROM charges_fixes_mensuelles
                WHERE mois = %s
            """
            cursor.execute(query_all, (premier_jour,))
            result = cursor.fetchone()
            
            if result:
                print(f"\n📊 Données trouvées:")
                
                # Loyer
                if result[0] and float(result[0]) > 0:
                    charges.append({
                        'type': 'loyer',
                        'description': 'Loyer du local',
                        'montant': float(result[0]),
                        'date': result[9]
                    })
                    print(f"   ✅ Loyer: {result[0]} DT")
                
                # Électricité
                if result[1] and float(result[1]) > 0:
                    charges.append({
                        'type': 'electricite',
                        'description': 'Électricité (STEG)',
                        'montant': float(result[1]),
                        'date': result[9]
                    })
                    print(f"   ✅ Électricité: {result[1]} DT")
                
                # Eau
                if result[2] and float(result[2]) > 0:
                    charges.append({
                        'type': 'eau',
                        'description': 'Eau (SONEDE)',
                        'montant': float(result[2]),
                        'date': result[9]
                    })
                    print(f"   ✅ Eau: {result[2]} DT")
                
                # Impôt
                if result[3] and float(result[3]) > 0:
                    charges.append({
                        'type': 'impot',
                        'description': 'Impôt',
                        'montant': float(result[3]),
                        'date': result[9]
                    })
                    print(f"   ✅ Impôt: {result[3]} DT")
                
                # Municipalité
                if result[4] and float(result[4]) > 0:
                    charges.append({
                        'type': 'municipalite',
                        'description': 'Municipalité',
                        'montant': float(result[4]),
                        'date': result[9]
                    })
                    print(f"   ✅ Municipalité: {result[4]} DT")
                
                # Terrasse
                if result[5] and float(result[5]) > 0:
                    charges.append({
                        'type': 'terrasse',
                        'description': 'Terrasse',
                        'montant': float(result[5]),
                        'date': result[9]
                    })
                    print(f"   ✅ Terrasse: {result[5]} DT")
                
                # Internet
                if result[6] and float(result[6]) > 0:
                    charges.append({
                        'type': 'internet',
                        'description': 'Internet',
                        'montant': float(result[6]),
                        'date': result[9]
                    })
                    print(f"   ✅ Internet: {result[6]} DT")
                
                # Autres
                if result[7] and float(result[7]) > 0:
                    desc = result[8] if result[8] else 'Autres charges'
                    charges.append({
                        'type': 'autres',
                        'description': desc,
                        'montant': float(result[7]),
                        'date': result[9]
                    })
                    print(f"   ✅ Autres: {result[7]} DT ({desc})")
            
            # Salaires mensuels
            print(f"\n🔍 Recherche des salaires pour {premier_jour}...")
            
            query_salaires = """
                SELECT 
                    nom_employe,
                    montant,
                    mois
                FROM salaires_mensuels
                WHERE mois = %s
            """
            
            cursor.execute(query_salaires, (premier_jour,))
            results_salaires = cursor.fetchall()
            
            print(f"   Salaires trouvés: {len(results_salaires)}")
            
            for row in results_salaires:
                charges.append({
                    'type': 'salaire',
                    'description': f'Salaire - {row[0]}',
                    'montant': float(row[1]),
                    'date': row[2]
                })
                print(f"   ✅ {row[0]}: {row[1]} DT")
            
            cursor.close()
            
            print(f"\n📊 TOTAL: {len(charges)} charge(s)")
            print("="*60 + "\n")
            
            return charges
            
        except Exception as e:
            print(f"\n❌ ERREUR: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_articles_vendus_mois(self, mois_date):
        """Récupérer les articles vendus dans le mois avec quantités"""
        try:
            from datetime import timedelta
            
            premier_jour = mois_date.replace(day=1)
            if mois_date.month == 12:
                dernier_jour = mois_date.replace(year=mois_date.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                dernier_jour = mois_date.replace(month=mois_date.month + 1, day=1) - timedelta(days=1)
            
            query = """
                SELECT 
                    a.nom,
                    a.prix_vente,
                    SUM(v.quantite) as quantite_totale,
                    SUM(v.quantite * a.prix_vente) as total_vente
                FROM ventes v
                JOIN articles a ON v.article_id = a.id
                WHERE v.date_vente BETWEEN %s AND %s
                AND v.quantite > 0
                GROUP BY a.id, a.nom, a.prix_vente
                ORDER BY quantite_totale DESC
            """
            
            self.db.cursor.execute(query, (premier_jour, dernier_jour))
            results = self.db.cursor.fetchall()
            
            articles = []
            for row in results:
                articles.append({
                    'nom': row[0],
                    'prix_vente': float(row[1]),
                    'quantite_totale': int(row[2]),
                    'total_vente': float(row[3])
                })
            
            return articles
            
        except Exception as e:
            print(f"Erreur get_articles_vendus_mois: {e}")
            return []