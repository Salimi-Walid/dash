from nicegui import ui
from firebase.service import db
import asyncio

def myOrder(content):
    content.clear()

    async def fetch_orders():
        """Fetch orders from Firestore and return them as a list of dictionaries."""
        try:
            orders_ref = db.collection('orders')
            orders_docs = await asyncio.to_thread(orders_ref.get)  # Fetch asynchronously

            orders = []
            for doc in orders_docs:
                order_data = doc.to_dict()

                # Ensure required fields exist before adding
                if 'name' in order_data and 'phone' in order_data:
                    orders.append({
                        'name': order_data.get('name', 'N/A'),
                        'phone': str(order_data.get('phone', 'N/A')),  # Convert to string
                        'address': order_data.get('address', 'N/A'),
                        'city': order_data.get('city', 'N/A'),
                        'postal_code': str(order_data.get('postal_code', 'N/A')),
                        'payment_method': order_data.get('payment_method', 'N/A'),
                        'status': order_data.get('status', 'Pending')
                    })

            return orders
        except Exception as e:
            ui.notify(f"Error fetching orders: {e}", color='negative')
            return []

    async def load_orders():
        """Load orders into the NiceGUI table."""
        orders = await fetch_orders()
        order_table.rows = orders
        order_table.update()

    with content:
        ui.label('📦 Orders Table').classes('text-h5')

        # Orders Table
        global order_table
        order_table = ui.table(
            columns=[
                {'name': 'name', 'label': 'Name', 'field': 'name'},
                {'name': 'phone', 'label': 'Phone', 'field': 'phone'},
                {'name': 'address', 'label': 'Address', 'field': 'address'},
                {'name': 'city', 'label': 'City', 'field': 'city'},
                {'name': 'postal_code', 'label': 'Postal Code', 'field': 'postal_code'},
                {'name': 'payment_method', 'label': 'Payment Method', 'field': 'payment_method'},
                {'name': 'status', 'label': 'Status', 'field': 'status'},
            ],
            rows=[],  # Initially empty
        ).classes('w-full')

        # Refresh Button
        ui.button('🔄 Refresh Orders', icon='refresh', on_click=load_orders).props('color=primary')

    # Load data on UI startup
    ui.timer(1, load_orders, once=True)
