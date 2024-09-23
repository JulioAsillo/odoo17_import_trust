import xmlrpc.client
from src.utils.config import ODOO_URL, DB_NAME, USERNAME, API_KEY


class OdooClient:
    def __init__(self):
        self.url = ODOO_URL
        self.db = DB_NAME
        self.username = USERNAME
        self.password = API_KEY
        self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        self.uid = self.common.authenticate(self.db, self.username, self.password, {})
        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')

    def get_or_create_partner(self, name):
        partner_id = self.models.execute_kw(self.db, self.uid, self.password,
                                            'res.partner', 'search', [[('name', '=', name)]])
        if partner_id:
            return partner_id[0]
        else:
            return self.models.execute_kw(self.db, self.uid, self.password,
                                          'res.partner', 'create', [{'name': name}])

    def get_or_create_product(self, name):
        product_id = self.models.execute_kw(self.db, self.uid, self.password,
                                            'product.product', 'search', [[('name', '=', name)]])
        if product_id:
            return product_id[0]
        else:
            return self.models.execute_kw(self.db, self.uid, self.password,
                                          'product.product', 'create', [{'name': name}])

    def create_purchase_order(self, order_data):
        try:
            order_id = self.models.execute_kw(self.db, self.uid, self.password,
                                              'purchase.order', 'create', [order_data])
            return order_id
        except xmlrpc.client.Fault as error:
            print(f"Error al crear la orden de compra: {error}")
            return None

    def confirm_purchase_order(self, order_id):
        try:
            self.models.execute_kw(self.db, self.uid, self.password,
                                   'purchase.order', 'button_confirm', [order_id])
            print(f"Orden de compra {order_id} confirmada.")
        except xmlrpc.client.Fault as error:
            print(f"Error al confirmar la orden de compra {order_id}: {error}")

    def receive_purchase_order(self, order_id):
        try:
            # Buscar el albarán (stock.picking) asociado a la orden de compra
            picking_ids = self.models.execute_kw(self.db, self.uid, self.password,
                                                 'stock.picking', 'search', [[('purchase_id', '=', order_id)]])

            if picking_ids:
                # Confirmar la recepción
                self.models.execute_kw(self.db, self.uid, self.password,
                                       'stock.picking', 'button_validate', [picking_ids[0]])
                print(f"Orden de compra {order_id} recibida.")
            else:
                print(f"No se encontró albarán para la orden de compra {order_id}")
        except xmlrpc.client.Fault as error:
            print(f"Error al recibir la orden de compra {order_id}: {error}")