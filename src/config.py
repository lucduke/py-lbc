#!/usr/bin/env python3
"""
Module pour gérer les fonctions liées au fichier de configuration
"""

import json
import os
from typing import Any, Dict
def load_config(config_path: str) -> Dict[str, Any]:
    """
    Charge le fichier de configuration JSON

    Args:
        config_path (str): Chemin vers le fichier de configuration

    Returns:
        Dict[str, Any]: Dictionnaire contenant la configuration
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Le fichier de configuration '{config_path}' est introuvable.")
    
    with open(config_path, 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
    
    return config
