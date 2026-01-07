#!/usr/bin/env python3
"""
Module pour gérer la classe Car, ses attributs, méthodes associées et DAO
"""
from dataclasses import dataclass
@dataclass
class Cars:
    link: str
    title: str
    year: int
    original_price: float
    current_price: float
    mileage: int
    gearbox: str
    def __str__(self) -> str:
        return f"{self.title} ({self.year}) -- {self.original_price}€ - {self.current_price}€ - {self.mileage} km - {self.gearbox} - {self.link}"
    def to_dict(self) -> dict:
        return {
            "link": self.link,
            "title": self.title,
            "year": self.year,
            "original_price": self.original_price,
            "current_price": self.current_price,
            "mileage": self.mileage,
            "gearbox": self.gearbox
        }
    @classmethod
    def from_dict(cls, data: dict) -> 'Cars':
        return cls(
            link=data.get("link", ""),
            title=data.get("title", ""),
            year=data.get("year", 0),
            original_price=data.get("original_price", 0.0),
            current_price=data.get("current_price", 0.0),
            mileage=data.get("mileage", 0),
            gearbox=data.get("gearbox", "")
        )
# Example usage:
# car_data = {
#     "link": "http://example.com/car1",
#     "title": "Peugeot 208",
#     "year": 2018,
#     "original_price": 18000.0,
#     "current_price": 15000.0,
#     "mileage": 30000,
#     "gearbox": "Manual"
# }
# car = Cars.from_dict(car_data)
# print(car)
# print(car.to_dict())
