"""
Formateurs pour l'affichage des données
"""

from datetime import date
from decimal import Decimal
from config.settings import CURRENCY


def format_currency(amount):
    """Formater un montant en devise"""
    if isinstance(amount, (int, float, Decimal)):
        return f"{float(amount):.2f} {CURRENCY}"
    return f"0.00 {CURRENCY}"


def format_date(date_obj):
    """Formater une date (dd/mm/yyyy)"""
    if isinstance(date_obj, date):
        return date_obj.strftime('%d/%m/%Y')
    return str(date_obj)


def format_month(date_obj):
    """Formater un mois (Mois Année)"""
    if isinstance(date_obj, date):
        mois_fr = [
            'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
            'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
        ]
        return f"{mois_fr[date_obj.month - 1]} {date_obj.year}"
    return str(date_obj)


def format_percentage(value):
    """Formater un pourcentage"""
    if isinstance(value, (int, float, Decimal)):
        return f"{float(value):.1f}%"
    return "0.0%"


def format_number(value):
    """Formater un nombre avec séparateurs de milliers"""
    if isinstance(value, (int, float, Decimal)):
        return f"{float(value):,.2f}".replace(',', ' ')
    return "0"