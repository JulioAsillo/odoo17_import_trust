import pandas as pd
from src.models.purchase_order import PurchaseOrder
from src.models.product import Product

def read_excel_file(file_path):
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        raise

def process_excel_data(df):
    purchase_orders = []
    current_order = None

    for index, row in df.iterrows():
        try:
            if pd.notna(row['Fecha confirmación']):
                if current_order:
                    purchase_orders.append(current_order)
                current_order = PurchaseOrder.from_excel_row(row)

            if pd.notna(row['Líneas de Pedido/Producto/Nombre']):
                product = Product.from_excel_row(row)
                current_order.add_product(product)
        except Exception as e:
            print(f"Error procesando la fila {index}:")
            print(row)
            print(f"Error: {e}")
            raise

    if current_order:
        purchase_orders.append(current_order)

    return purchase_orders

def prepare_data_for_api(purchase_orders, odoo_client):
    api_data = []
    for order in purchase_orders:
        partner_id = odoo_client.get_or_create_partner(order.supplier)
        order_data = {
            'partner_id': partner_id,
            'date_order': order.confirmation_date.strftime('%Y-%m-%d %H:%M:%S'),
            'date_planned': order.order_deadline.strftime('%Y-%m-%d %H:%M:%S'),
            'state': 'draft',
            'order_line': []
        }
        for product in order.products:
            product_id = odoo_client.get_or_create_product(product.name)
            line_data = {
                'product_id': product_id,
                'name': product.description or product.name,
                'product_qty': product.quantity,
                'price_unit': product.price,
                'taxes_id': [(6, 0, [product.tax_id])] if product.tax_id else [(6, 0, [])]
            }
            order_data['order_line'].append((0, 0, line_data))
        api_data.append(order_data)
    return api_data
