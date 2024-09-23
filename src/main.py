from src.data_processing.excel_reader import read_excel_file, process_excel_data, prepare_data_for_api
from src.api.odoo_client import OdooClient

def main():
    file_path = 'data/OrdenCompra.xlsx'
    try:
        df = read_excel_file(file_path)
        purchase_orders = process_excel_data(df)

        odoo_client = OdooClient()
        api_data = prepare_data_for_api(purchase_orders, odoo_client)

        for order_data in api_data:
            order_id = odoo_client.create_purchase_order(order_data)
            if order_id:
                print(f"Orden de compra creada en Odoo con ID: {order_id}")
                odoo_client.confirm_purchase_order(order_id)
                odoo_client.receive_purchase_order(order_id)
            else:
                print("Error al crear la orden de compra")

        print("Proceso completado exitosamente.")

    except Exception as e:
        print(f"Se produjo un error en la ejecución del programa: {e}")
        print("Detalles del error:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()