#!/usr/bin/env python3
"""
Module pour gérer la classe Car, ses attributs, méthodes associées et DAO
"""
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Cars:
    brand: str
    model: str
    link: str
    title: str
    year: int
    original_price: float
    current_price: float
    mileage: int
    gearbox: str
    first_publication_date: datetime = None
    update_date: datetime = None
    duration_on_site: int = 0  # in days
    price_variation: float = 0.0  # in percentage
    def __str__(self) -> str:
        return f"{self.title} ({self.year}) -- {self.original_price}€ - {self.current_price}€ - {self.mileage} km - {self.gearbox} - {self.link}"
    def to_dict(self) -> dict:
        return {
            "brand": self.brand,
            "model": self.model,
            "link": self.link,
            "title": self.title,
            "year": self.year,
            "original_price": self.original_price,
            "current_price": self.current_price,
            "mileage": self.mileage,
            "gearbox": self.gearbox,
            "first_publication_date": self.first_publication_date,
            "update_date": self.update_date,
            "duration_on_site": self.duration_on_site,
            "price_variation": self.price_variation
        }
    @classmethod
    def from_dict(cls, data: dict) -> 'Cars':
        return cls(
            brand=data.get("brand", ""),
            model=data.get("model", ""),
            link=data.get("link", ""),
            title=data.get("title", ""),
            year=data.get("year", 0),
            original_price=data.get("original_price", 0.0),
            current_price=data.get("current_price", 0.0),
            mileage=data.get("mileage", 0),
            gearbox=data.get("gearbox", ""),
            first_publication_date=data.get("first_publication_date", None),
            update_date=data.get("update_date", None),
            duration_on_site=data.get("duration_on_site", 0),
            price_variation=data.get("price_variation", 0.0)
        )
# Example usage:
# car_data = {
#     "brand": "Peugeot",
#     "model": "208",
#     "link": "http://example.com/car1",
#     "title": "Peugeot 208",
#     "year": 2018,
#     "original_price": 18000.0,
#     "current_price": 15000.0,
#     "mileage": 30000,
#     "gearbox": "Manual",
#     "first_publication_date": datetime(2020, 1, 1, 10, 30, 0),
#     "update_date": datetime(2020, 1, 1, 10, 30, 0),
#     "duration_on_site": 10,
#     "price_variation": -16.67
# }
# car = Cars.from_dict(car_data)
# print(car)
# print(car.to_dict())
