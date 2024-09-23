from dataclasses import dataclass


@dataclass
class Product:
    name: str
    description: str
    quantity: float
    price: float
    tax_id: int
    tax_amount: float

    @classmethod
    def from_excel_row(cls, row):
        tax_id = 8 if '18% (Included in price)' in str(row['Líneas de Pedido/Impuestos/Nombre del impuesto']) else 7
        return cls(
            name=row['Líneas de Pedido/Producto/Nombre'],
            description=row['Líneas de Pedido/Descripción'],
            quantity=row['Líneas de Pedido/Cantidad'],
            price=row['Líneas de Pedido/Precio Unitario'],
            tax_id=tax_id,
            tax_amount=row['Líneas de Pedido/Impuestos/Nombre del impuesto']
        )