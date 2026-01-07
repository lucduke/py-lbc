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


def results_scrapper(soup: BeautifulSoup, tag: str, class_name: str, attrs: dict | None = None):
    """
    Extrait les résultats de la page scrappée
    
    Args:
        soup (BeautifulSoup): objet soup de la page
        tag (str): balise HTML à rechercher
        class_name (str): nom de la classe CSS à rechercher
        attrs (dict, optional): autres attributs HTML à rechercher
    
    Returns:
        list: liste des éléments trouvés
    """
    if attrs is None:
        attrs = {}
    results = soup.find_all(tag, class_=class_name, attrs=attrs)
    return results


def article_scrapper(soup: BeautifulSoup):
    """
    Extrait les informations d'un article spécifique
    
    Args:
        article (BeautifulSoup): objet soup de l'article
        tag (str): balise HTML à rechercher
        class_name (str): nom de la classe CSS à rechercher
        attrs (dict, optional): autres attributs HTML à rechercher
    
    Returns:
        dict: dictionnaire des informations extraites
    """
    link = soup.find("a", class_="absolute inset-0", attrs={"aria-label": "Voir l’annonce"}).get("href")
    title = soup.find("h3").get_text().strip()
    year = int(soup.find("p", class_="text-neutral", string="Année").find_next_sibling("p").get_text(strip=True))
    
    current_price_text = soup.find('p', attrs={"data-test-id": "price"}).span.get_text(strip=True)
    if current_price_text:
        current_price = int(current_price_text.replace("\u202f", "").replace("€", ""))
    else:
        current_price = None

    mileage = int(soup.find("p", class_="text-neutral", string="Kilométrage").find_next_sibling("p").get_text(strip=True).replace(" km",""))
    gearbox = soup.find("p", class_="text-neutral", string="Boîte de vitesse").find_next_sibling("p").get_text(strip=True)

    return {"link": link, "title": title, "year": year, "original_price": None, "current_price": current_price, "mileage": mileage, "gearbox": gearbox}

def article_scrapper_find_old_price(soup: BeautifulSoup):
    """
    Extrait le prix original d'un article spécifique
    
    Args:
        article (BeautifulSoup): objet soup de l'article
    
    Returns:
        float | None: prix original ou None si non trouvé
    """
    old_price_tag = soup.find('script', type="application/json")
    if old_price_tag:
        old_price_text = old_price_tag.get_text(strip=True)
        old_price = float(old_price_text.replace("\u202f", "").replace("€", ""))
        return old_price
    return None