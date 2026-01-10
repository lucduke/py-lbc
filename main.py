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
from src.scrapping import url_scrapper, results_scrapper, results_scrapper_detail, article_scrapper
from src.cars import Cars
from src.cars_dao import CarsDAO

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
        "--grab-data",
        action="store_true",
        help="Lance le scrapping pour le site LeBonCoin.fr"
    )
    
    parser.add_argument(
        "--calculate-stats",
        action="store_true",
        help="Calcule les statistiques sur les données scrappées"
    )
    
    return parser.parse_args()

# Main Method
def main():
    # Parse command line arguments
    args = parse_args()
    
    if not args.grab_data and not args.calculate_stats:
        logging.warning("Aucun paramètre spécifié. Veuillez utiliser --grab-data ou --calculate-stats.")
        print("Usage: python src/main.py --grab-data ou python src/main.py --calculate-stats")
        return

    try:
        logging.info("Démarrage du programme de scrapping des annonces de voitures")

        # Load the configuration
        logging.info("Chargement de la configuration")
        config = load_config("config.json")
        logging.info("Configuration chargée avec succès")

        # Initialize database connection if needed and create the cars table
        database_path = config.get("database_path", "cars.db")
        logging.info(f"Initialisation de la base de données à {database_path}")
        cars_dao = CarsDAO(database_path)

        # Scrapping
        if args.grab_data:
            logging.info("Démarrage du scrapping pour le site LeBonCoin.fr")
            # Get values from config
            brand_filter = config.get("brand_filter", "")
            model_filter = config.get("model_filter", "")
            url = config.get("url")
            url = url.replace("u_car_brand=?", f"u_car_brand={brand_filter}").replace("u_car_model=?", f"u_car_model={model_filter}")
            # Call the scrapping function
            # Loop through pages until url is None
            while url:
                logging.info(f"Scrapping de la page : {url}")
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
                # Initialize list to store car objects
                list_car = []
                # Parse each article in the page
                for article in articles:
                    #announcement = article_scrapper(article)
                    announcement = results_scrapper_detail(article, ["link", "title", "year", "current_price", "mileage", "gearbox"])
                    # Merge both dictionaries
                    # Init car object with values of announcement    
                    car = Cars.from_dict(announcement)
                    car.brand = brand_filter
                    car.model = model_filter
                    #logging.info(f"Annonce scrappée : {car}")
                    # Store car objects in a list
                    list_car.append(car)
                # Insert cars into database
                for car in list_car:
                    # Check if car already exists in database to avoid duplicates
                    existing_cars = cars_dao.get_all_cars()
                    if any(existing_car.link == car.link for existing_car in existing_cars):
                        logging.info(f"L'annonce existe déjà dans la base de données : {car.link}. Mise à jour du prix de l'annonce en BDD.")
                        cars_dao.update_car_current_price(car.link, car.current_price)
                        continue
                    else:
                        cars_dao.insert_car(car)
                # Pause between page requests to avoid being blocked
                time.sleep(2)
            # Find missing original prices and update them in the database
            logging.info("Vérification des prix originaux manquants")
            all_cars = cars_dao.get_all_cars()
            for car in all_cars:
                if car.original_price is None or car.original_price == 0.0:
                    logging.info(f"Recherche du prix original pour l'annonce : {car.link}")
                    # Scrape the article page to find the original price and first publication date
                    url = "https://www.leboncoin.fr" + car.link
                    article_page = url_scrapper(url)
                    if article_page is None:
                        logging.error(f"Impossible de récupérer la page de l'annonce : {car.link}")
                        continue
                    #original_price, first_publication_date = article_scrapper_find_old_price_and_first_publication_date(article_page)
                    original_price, first_publication_date = article_scrapper(article_page, ["old_price", "first_publication_date"])
                    if original_price:
                        car.original_price = original_price
                        cars_dao.update_car(car)
                        logging.info(f"Prix original mis à jour pour l'annonce : {car.link} - Prix original : {car.original_price}€")
                    else:
                        car.original_price = car.current_price
                        cars_dao.update_car(car)
                        logging.info(f"Prix original mis à jour avec prix courant pour l'annonce : {car.link} - Prix original : {car.original_price}€")
                    if first_publication_date:
                        car.first_publication_date = first_publication_date
                        cars_dao.update_car_first_publication_date(car.link, first_publication_date)
                        logging.info(f"Date de première publication trouvée pour l'annonce : {car.link} - Date : {first_publication_date}")
                    # Pause between requests
                    time.sleep(2)
        
        # Calculate statistics
        if args.calculate_stats:
            logging.info("Démarrage du calcul des statistiques sur les données scrappées")
            statistics = cars_dao.calculate_statistics()
            for stat, value in statistics.items():
                logging.info(f"{stat} : {value}")
            # Export statistics to a csv file
            stats_file = config.get("statistics_file", "statistics.csv")
            cars_dao.export_statistics_to_csv(statistics, stats_file)
            logging.info("Statistiques calculées avec succès")
    
    except Exception as e:
        logging.error(f"Erreur fatale: {e}")
        raise

if __name__ == "__main__":
    main()