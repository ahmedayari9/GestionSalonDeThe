"""
Configuration du système de logging
"""

import logging
from pathlib import Path
from datetime import datetime
from config.settings import LOG_FOLDER


def setup_logger():
    """Configurer le logger principal"""
    # Créer le dossier logs
    log_dir = Path(LOG_FOLDER)
    log_dir.mkdir(exist_ok=True)
    
    # Nom du fichier log
    log_file = log_dir / f"sultan_ahmed_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger('SultanAhmed')
    return logger


def get_logger():
    """Récupérer le logger"""
    return logging.getLogger('SultanAhmed')