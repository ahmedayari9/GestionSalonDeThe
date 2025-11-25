"""
Validateurs pour les entrées utilisateur
"""


def validate_non_empty(value, field_name):
    """Valider qu'un champ n'est pas vide"""
    if not value or not value.strip():
        raise ValueError(f"{field_name} ne peut pas être vide!")
    return True


def validate_price(value, field_name):
    """Valider qu'un prix est valide"""
    try:
        price = float(value)
        if price < 0:
            raise ValueError(f"{field_name} ne peut pas être négatif!")
        return True
    except (ValueError, TypeError):
        raise ValueError(f"{field_name} doit être un nombre valide!")


def validate_quantity(value):
    """Valider une quantité"""
    try:
        qty = int(value)
        if qty < 0:
            raise ValueError("La quantité ne peut pas être négative!")
        return True
    except (ValueError, TypeError):
        raise ValueError("La quantité doit être un nombre entier valide!")


def validate_date(date_obj):
    """Valider une date"""
    from datetime import date
    if not isinstance(date_obj, date):
        raise ValueError("Date invalide!")
    return True