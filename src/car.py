#!/usr/bin/env python3
"""
Module pour gérer la classe Car, ses attributs, méthodes associées et DAO
"""
from dataclasses import dataclass
@dataclass
class Car:
    link: str
    title: str
    year: int
    current_price: float
    mileage: int
    gearbox: str
    def __str__(self) -> str:
        return f"{self.title} ({self.year}) - {self.current_price}€ - {self.mileage} km - {self.gearbox} - {self.link}"
    def to_dict(self) -> dict:
        return {
            "link": self.link,
            "title": self.title,
            "year": self.year,
            "current_price": self.current_price,
            "mileage": self.mileage,
            "gearbox": self.gearbox
        }
    @classmethod
    def from_dict(cls, data: dict) -> 'Car':
        return cls(
            link=data.get("link", ""),
            title=data.get("title", ""),
            year=data.get("year", 0),
            current_price=data.get("current_price", 0.0),
            mileage=data.get("mileage", 0),
            gearbox=data.get("gearbox", "")
        )
# Example usage:
# car_data = {
#     "link": "http://example.com/car1",
#     "title": "Peugeot 208",
#     "year": 2018,
#     "current_price": 15000.0,
#     "mileage": 30000,
#     "gearbox": "Manual"
# }
# car = Car.from_dict(car_data)
# print(car)
# print(car.to_dict())
