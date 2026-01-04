import requests
from bs4 import BeautifulSoup

#!/usr/bin/env python3
"""
Module pour gérer les fonctions liées au scrapping
"""

def url_scrapper(url: str, headers: dict | None = None, timeout: int = 10):
    """
    Charge la page web correspond à l'url
    
    Args:
        url (str): URL de la page web à scrapper
        headers (dict, optional): en-têtes HTTP supplémentaires ou de remplacement
        timeout (int, optional): timeout en secondes pour la requête
    
    Returns:
        BeautifulSoup: objet soup de la page
    """
    session = requests.Session()

    default_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }
    if headers:
        default_headers.update(headers)
    session.headers.update(default_headers)

    # Retry simple pour erreurs transitoires
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["GET", "HEAD"])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


