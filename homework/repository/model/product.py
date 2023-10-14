import sqlite3
from dataclasses import dataclass
from uuid import UUID


@dataclass
class Product:
    id: UUID
    name: str
    price: str

    def __post_init__(self):
        self.price = f'{self.price:.2f}'

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Product':
        return cls(*row)
