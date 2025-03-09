import asyncio
from nicegui import ui
from firebase.service import db

def orders_page():
    with ui.column().classes('w-full'):
        ui.label('Orders Management').classes('text-h5')
        orders_container = ui.column()

    async def refresh_orders():
        orders_container.clear()
        docs = db.collection('orders').stream()
        async for doc in docs:
            order = doc.to_dict()
            with orders_container:
                with ui.card().classes('w-full mb-4'):
                    ui.label(f"Order ID: {doc.id}")
                    ui.label(f"Customer: {order.get('customer_name', 'N/A')}")
                    ui.label(f"Total: ${order.get('total', 0):.2f}")
                    ui.label(f"Status: {order.get('status', 'Pending')}")

    asyncio.create_task(refresh_orders())
