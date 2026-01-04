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
        from src.config import load_config
        config = load_config("config.json")
        logging.info("Configuration chargée avec succès")

        if args.url1:
            logging.info("Démarrage du scrapping pour le site URL1")
            # Get url1 value from config
            url = config.get("url1")
            # Call the scrapping function for URL1
            from src.scrapping import url_scrapper, results_scrapper, article_scrapper
            bs_content = url_scrapper(url)
            # List the articles in the page
            articles = results_scrapper(bs_content, "article", "relative h-[inherit] group/adcard")
            logging.info(f"Nombre d'annonces trouvées sur la page : {len(articles)}")
            # pp
            for article in articles:
                announcement = article_scrapper(article)
                #logging.info(f"Titre: {title}, Lien: {link}, Année: {year}, Prix: {actualprice}, Kilométrage: {mileage}")


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