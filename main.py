#!/usr/bin/env python3
"""
Point d'entrée principal du programme de scrapping des annonce de voitures

Usage:
    python main.py --url1
    python main.py --url2
"""

# Dependencies
import logging
import argparse
import time
from src.config import load_config
from src.scrapping import url_scrapper, results_scrapper, article_scrapper
from src.car import Car

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scrapping.log'),
        logging.StreamHandler()
    ]
)

# Parsing Method
def parse_args() -> argparse.Namespace:
    """
    Parse les arguments de ligne de commande
    
    Returns:
        argparse.Namespace: Arguments parsés
    """
    parser = argparse.ArgumentParser(
        description="Scrapping des annonces de voitures"
    )
    
    parser.add_argument(
        "--url1",
        action="store_true",
        help="Lance le scrapping pour le site URL1"
    )
    
    parser.add_argument(
        "--url2",
        action="store_true",
        help="Lance le scrapping pour le site URL2"
    )
    
    return parser.parse_args()

# Main Method
def main():
    # Parse command line arguments
    args = parse_args()
    
    if not args.url1 and not args.url2:
        logging.warning("Aucun site spécifié pour le scrapping. Veuillez utiliser --url1 ou --url2.")
        print("Usage: python src/main.py --url1 ou python src/main.py --url2")
        return

    try:
        logging.info("Démarrage du programme de scrapping des annonces de voitures")

        # Load the configuration
        logging.info("Chargement de la configuration")
        config = load_config("config.json")
        logging.info("Configuration chargée avec succès")

        if args.url1:
            logging.info("Démarrage du scrapping pour le site URL1")
            # Get url1 value from config
            url = config.get("url1")
            # Call the scrapping function for URL1
            # Loop through pages until url is None
            while url:
                print(f"\n")
                logging.info(f"\033[34mScrapping de la page : {url}\033[0m")
                # Get the BeautifulSoup content of the page
                page_content = url_scrapper(url)
                # Get next page link if exists
                try:
                    next_page = page_content.find("a", attrs={"aria-label": "Page suivante"}).get("href")
                    next_page = "https://www.leboncoin.fr" + next_page
                    url = next_page
                except AttributeError:
                    next_page = None
                    url = next_page
                # List the articles in the page
                articles = results_scrapper(page_content, "article", "relative h-[inherit] group/adcard")
                logging.info(f"Nombre d'annonces trouvées sur la page : {len(articles)}")
                # Parse each article in the page
                for article in articles:
                    announcement = article_scrapper(article)
                    #print(announcement)
                    # Init car object with values of announcement    
                    car = Car.from_dict(announcement)
                    # Store car objects in a list before saving to database or file

                # Pause between page requests to avoid being blocked
                time.sleep(2)

        if args.url2:
            logging.info("Démarrage du scrapping pour le site URL2")
            # Call the scrapping function for URL2
            # from scrapping.url2_scraper import main as url2_main
            # url2_main()
    
    except Exception as e:
        logging.error(f"Erreur fatale: {e}")
        raise

if __name__ == "__main__":
    main()