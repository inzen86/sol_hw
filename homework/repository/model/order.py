import sqlite3
import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class Amount:
    discount: str
    paid: str
    returns: str
    total: str

    def __post_init__(self):
        self.discount = f'{self.discount:.2f}'
        self.paid = f'{self.paid:.2f}'
        self.returns = f'{self.returns:.2f}'
        self.total = f'{self.total:.2f}'

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Amount':
        return cls(*row)


@dataclass
class OrderProduct:
    id: uuid.UUID
    name: str
    price: str
    product_id: int
    quantity: int
    replaced_with: Optional['OrderProduct']

    def __post_init__(self):
        self.price = f'{self.price:.2f}'

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'OrderProduct':
        replacement = None
        if row['r_id']:
            replacement = OrderProduct(
                id=row['r_id'],
                name=row['r_name'],
                price=row['r_price'],
                product_id=row['r_product_id'],
                quantity=row['r_quantity'],
                replaced_with=None
            )
        return OrderProduct(
            id=row['id'],
            name=row['name'],
            price=row['price'],
            product_id=row['product_id'],
            quantity=row['quantity'],
            replaced_with=replacement
        )


@dataclass
class Order:
    amount: Amount
    id: uuid.UUID
    products: Optional[list[OrderProduct]]
    status: str

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Order':
        amount = Amount(
            discount=row['discount'],
            paid=row['paid'],
            returns=row['returns'],
            total=row['total']
        )
        return Order(
            amount=amount,
            id=row['id'],
            products=[],
            status=row['status']
        )
