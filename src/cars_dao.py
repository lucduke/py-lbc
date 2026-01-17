#!/usr/bin/env python3
"""
Module pour gérer la persistance de la classe Cars dans une base de données sqlite
"""
import sqlite3
import csv
from src.cars import Cars
from datetime import date

class CarsDAO:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cars (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand TEXT,
                    model TEXT,
                    link TEXT,
                    title TEXT,
                    year INTEGER,
                    original_price REAL,
                    current_price REAL,
                    mileage INTEGER,
                    gearbox TEXT,
                    first_publication_date TIMESTAMP DEFAULT NULL,
                    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    duration_on_site INTEGER DEFAULT NULL,
                    price_variation REAL DEFAULT NULL
                )
            """)
            conn.commit()

    def insert_car(self, car: Cars):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cars (brand, model, link, title, year, original_price, current_price, mileage, gearbox, first_publication_date, update_date, duration_on_site, price_variation)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (car.brand, car.model, car.link, car.title, car.year, car.original_price, car.current_price, car.mileage, car.gearbox, car.first_publication_date, date.today(), car.duration_on_site, car.price_variation))
            conn.commit()
    
    def get_all_cars(self) -> list[Cars]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT brand, model, link, title, year, original_price, current_price, mileage, gearbox, first_publication_date, update_date FROM cars")
            rows = cursor.fetchall()
            cars = [Cars(brand=row[0], model=row[1], link=row[2], title=row[3], year=row[4], original_price=row[5], current_price=row[6], mileage=row[7], gearbox=row[8], first_publication_date=row[9], update_date=row[10]) for row in rows]
            return cars
    
    def update_car(self, car: Cars):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE cars
                SET brand = ?, model = ?, title = ?, year = ?, original_price = ?, current_price = ?, mileage = ?, gearbox = ?, first_publication_date = ?, update_date = ?
                WHERE link = ?
            """, (car.brand, car.model, car.title, car.year, car.original_price, car.current_price, car.mileage, car.gearbox, car.first_publication_date, date.today(), car.link))
            conn.commit()
    
    def update_car_current_price(self, link: str, current_price: float):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE cars
                SET current_price = ?, update_date = ?
                WHERE link = ?
            """, (current_price, date.today(), link))
            conn.commit()
    
    def update_car_first_publication_date(self, link: str, first_publication_date):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE cars
                SET first_publication_date = ?, update_date = ?
                WHERE link = ?
            """, (first_publication_date, date.today(), link))
            conn.commit()
    
    def calculate_statistics(self) -> dict:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT brand, model, year, gearbox, round(AVG(current_price)) AS moyenne_prix, round(AVG(mileage)) as moyenne_km \
                           FROM cars \
                           WHERE update_date=(select max(update_date) from cars) \
                           GROUP BY brand, model, year, gearbox;")
            # Return statistics as a dictionary keyed by 'brand|model|year|gearbox'
            rows = cursor.fetchall()
            statistics = {}
            for row in rows:
                key = f"{row[0]}|{row[1]}|{row[2]}|{row[3]}"
                statistics[key] = {
                    "brand": row[0],
                    "model": row[1],
                    "year": row[2],
                    "gearbox": row[3],
                    "average_price": row[4],
                    "average_mileage": row[5]
                }
            return statistics

    def export_statistics_to_csv(self, statistics: dict, file_path: str):
        with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['brand', 'model', 'year', 'gearbox', 'average_price', 'average_mileage']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for stat in statistics.values():
                writer.writerow(stat)
    
    def calculate_duration_on_site_and_price_variation(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE cars
                SET duration_on_site = round(julianday(update_date) - julianday(first_publication_date)),
                    price_variation = CASE 
                        WHEN original_price IS NOT NULL AND original_price > 0 THEN round(((current_price - original_price) / original_price) * 100, 2)
                        ELSE NULL
                    END
                WHERE first_publication_date IS NOT NULL
            """)
            conn.commit()