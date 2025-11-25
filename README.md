# ☕ Sultan Ahmed - Application de Gestion Professionnelle

Application complète de gestion pour salon de thé avec architecture MVC professionnelle.

## 🎯 Fonctionnalités

### ✅ Gestion des Articles
- CRUD complet (Créer, Lire, Modifier, Supprimer)
- Calcul automatique des marges
- Import/Export CSV

### 📅 Ventes Quotidiennes
- Saisie rapide des quantités vendues
- Navigation par date (jour précédent/suivant)
- Calcul automatique des totaux
- Gestion des charges journalières

### 📊 Bilan Mensuel
- Résumé financier complet
- Charges fixes mensuelles
- Gestion des salaires
- Quantités vendues par article
- Export CSV du bilan

### 📈 Historique
- Consultation de l'historique des ventes
- Export CSV
- Suppression de journées

## 🏗️ Architecture

```
sultan_ahmed/
├── config/           # Configuration (DB, Settings)
├── models/           # Couche d'accès aux données
├── views/            # Interface utilisateur (Tkinter)
├── controllers/      # Logique métier
├── utils/            # Utilitaires (Validators, Formatters, Export, Logger)
├── assets/           # Styles et thèmes
└── main.py          # Point d'entrée
```

### Design Patterns Utilisés
- **MVC (Model-View-Controller)**
- **Singleton** : Connexion DB unique
- **Repository Pattern** : Abstraction de l'accès aux données
- **Observer** : Communication entre vues

## 🚀 Installation

### Prérequis
- Python 3.8+
- MySQL (XAMPP recommandé)
- Git (optionnel)

### Étapes

1. **Cloner le projet**
```bash
git clone https://github.com/ahmedayari9/sultan-ahmed-gestion.git
cd sultan-ahmed-gestion
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer la base de données**
- Démarrer XAMPP (MySQL)
- Créer la base de données :
```sql
CREATE DATABASE sultan_ahmed;
```

5. **Configuration**
```bash
cp .env.example .env
# Éditer .env si nécessaire
```

6. **Lancer l'application**
```bash
python main.py
```

## 📖 Utilisation

### Premier lancement
1. Ajouter des articles (onglet **Articles**)
2. Saisir les ventes du jour (onglet **Ventes du Jour**)
3. Consulter le bilan mensuel (onglet **Bilan Mensuel**)

### Workflow quotidien
1. Ouvrir l'application
2. Aller à l'onglet **Ventes du Jour**
3. Entrer les quantités vendues
4. Ajouter les dépenses du jour
5. Cliquer sur **Enregistrer et Jour suivant**

### Fin de mois
1. Onglet **Bilan Mensuel**
2. Entrer les charges fixes (loyer, électricité, etc.)
3. Ajouter les salaires des employés
4. Consulter le bénéfice net
5. Exporter le bilan en CSV

## 🛠️ Technologies

- **Python 3.8+**
- **Tkinter** : Interface graphique
- **MySQL** : Base de données
- **mysql-connector-python** : Connexion MySQL
- **python-dotenv** : Gestion de la configuration

## 📊 Structure de la Base de Données

### Tables
- `articles` : Liste des produits
- `ventes` : Ventes quotidiennes
- `charges` : Charges journalières
- `charges_fixes_mensuelles` : Charges fixes mensuelles
- `salaires_mensuels` : Salaires des employés

## 🤝 Contribution

Ce projet est ouvert aux contributions !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit (`git commit -m 'Ajout de...'`)
4. Push (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT.

## 👤 Auteur

**Ahmed Ayari** - [@ahmedayari9](https://github.com/ahmedayari9)

## 🐛 Bugs & Suggestions

Ouvrir une [issue](https://github.com/ahmedayari9/sultan-ahmed-gestion/issues) sur GitHub.

## 📞 Support

Pour toute question : ayari.ahmed@example.com

---

**Version :** 2.0.0  
**Date :** 2025-01-24  
**Statut :** ✅ Production Ready