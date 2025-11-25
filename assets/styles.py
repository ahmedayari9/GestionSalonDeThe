"""
Styles et thèmes pour l'interface
"""

from config.settings import COLORS

# Polices
FONTS = {
    'title': ('Arial', 24, 'bold'),
    'header': ('Arial', 14, 'bold'),
    'normal': ('Arial', 11),
    'small': ('Arial', 9),
    'big_button': ('Arial', 12, 'bold')
}

# Export des couleurs
__all__ = ['COLORS', 'FONTS']