#!/usr/bin/env python3
"""
Module pour gérer la persistance de la classe Cars dans une base de données sqlite
"""
import sqlite3
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
                    link TEXT,
                    title TEXT,
                    year INTEGER,
                    original_price REAL,
                    current_price REAL,
                    mileage INTEGER,
                    gearbox TEXT,
                    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def insert_car(self, car: Cars):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cars (link, title, year, original_price, current_price, mileage, gearbox, update_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (car.link, car.title, car.year, car.original_price, car.current_price, car.mileage, car.gearbox, date.today()))
            conn.commit()
    
    def get_all_cars(self) -> list[Cars]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT link, title, year, original_price, current_price, mileage, gearbox, update_date FROM cars")
            rows = cursor.fetchall()
            cars = [Cars(link=row[0], title=row[1], year=row[2], original_price=row[3], current_price=row[4], mileage=row[5], gearbox=row[6]) for row in rows]
            return cars
    
    def update_car(self, car: Cars):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE cars
                SET title = ?, year = ?, original_price = ?, current_price = ?, mileage = ?, gearbox = ?, update_date = ?
                WHERE link = ?
            """, (car.title, car.year, car.original_price, car.current_price, car.mileage, car.gearbox, date.today(), car.link))
            conn.commit()