"""
Configuration globale de l'application
"""

# Configuration MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'sultanahmed',
    'port': 3306
}

# Paramètres de l'application
APP_CONFIG = {
    'title': '☕ Sultan Ahmed - Gestion Salon de Thé',
    'version': '2.0.0',
    'width': 1400,
    'height': 850,
}

# Couleurs
COLORS = {
    'primary': '#D97706',      # Orange
    'success': '#059669',      # Vert
    'danger': '#DC2626',       # Rouge
    'info': '#2563EB',         # Bleu
    'warning': '#F59E0B',      # Jaune
    'secondary': '#6B7280',    # Gris
}

# Devise
CURRENCY = 'DT'

# Dossiers
EXPORT_FOLDER = 'exports'
LOG_FOLDER = 'logs'