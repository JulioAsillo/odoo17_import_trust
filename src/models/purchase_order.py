from dataclasses import dataclass, field
from typing import List
from datetime import datetime
from .product import Product

@dataclass
class PurchaseOrder:
    confirmation_date: datetime
    order_deadline: datetime
    supplier: str
    seller: str = "Operaciones"
    products: List[Product] = field(default_factory=list)
    state: str = "Orden de Compra"

    def add_product(self, product: Product):
        self.products.append(product)

    @classmethod
    def from_excel_row(cls, row):
        return cls(
            confirmation_date=datetime.strptime(str(row['Fecha confirmación']), '%Y-%m-%d %H:%M:%S'),
            order_deadline=datetime.strptime(str(row['Fecha límite de pedido']), '%Y-%m-%d %H:%M:%S'),
            supplier=row['Proveedor'],
            seller="Operaciones",
            state=row['Estado']
        )