import firebase_admin
from firebase_admin import credentials, firestore
from nicegui import ui, app
import asyncio


cred = credentials.Certificate('full-stack-ecommerce.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


@ui.page('/products')
def products_page():
    with ui.header().classes('bg-black'):
        ui.label('Add New Product').classes('text-h5 color-white')
    with ui.column().classes('w-full'):
        name = ui.input('Product Name').props('filled')
        price = ui.number('Price').props('filled')
        description = ui.textarea('Description').props('filled')
        image_url = ui.input('Image URL').props('filled')
        status_label = ui.label('').classes('text-red-500')
        async def add_product():
            try:
                product_data = {
                    'name': name.value,
                    'price': float(price.value),
                    'description': description.value,
                    'image_url': image_url.value
                }
                await asyncio.to_thread(db.collection('products').add, product_data)
                ui.notify('Product added!')
                await refresh_products()
            except Exception as e:
                status_label.set_text(f"Error: {str(e)}") 
        ui.button('Add Product', on_click=add_product).props('color=primary')
        ui.label('Product List').classes('text-h5 mt-10')
        products_container = ui.column().classes('w-full')

    async def refresh_products():
        products_container.clear()
        try:
            docs = await asyncio.to_thread(db.collection('products').get)
            if not docs:
                with products_container:
                    ui.label('No products found').classes('text-gray-500')
                return
            for doc in docs:
                with products_container:
                    with ui.card().classes(' mb-4'):
                        product = doc.to_dict()
                        ui.label(f"ID: {doc.id}")
                        ui.label(f"Name: {product.get('name', 'N/A')}")
                        ui.label(f"Price: ${product.get('price', 0):.2f}")
                        ui.label(f"Description: {product.get('description', 'N/A')}")
                        if 'image_url' in product:
                            ui.image(product['image_url']).classes('w-48 h-48 object-contain')
                        async def delete_product(doc_id=doc.id):
                            try:
                                await asyncio.to_thread(
                                    db.collection('products').document(doc_id).delete
                                )
                                ui.notify('Product deleted!')
                                await refresh_products()
                            except Exception as e:
                                ui.notify(f"Delete failed: {str(e)}", color='negative')
                        async def edit_product(doc_id=doc.id):
                            try:
                                doc_ref = await asyncio.to_thread(
                                    db.collection('products').document(doc_id).get
                                )
                                product = doc_ref.to_dict()
                                name.value = product.get('name', '')
                                price.value = product.get('price', 0)
                                description.value = product.get('description', '')
                                image_url.value = product.get('image_url', '')
                                
                                async def save_changes():
                                    try:
                                        updated_data = {
                                            'name': name.value,
                                            'price': float(price.value),
                                            'description': description.value,
                                            'image_url': image_url.value
                                        }
                                        await asyncio.to_thread(
                                            db.collection('products').document(doc_id).update,
                                            updated_data
                                        )
                                        ui.notify('Product updated!')
                                        await refresh_products()
                                    except Exception as e:
                                        ui.notify(f"Update failed: {str(e)}", color='negative')
                                        
                                # Replace add button with update button
                                add_button.set_text('Update Product')
                                add_button.on('click', save_changes)
                                
                            except Exception as e:
                                ui.notify(f"Edit failed: {str(e)}", color='negative')
                                
                        with ui.row():
                            ui.button('Edit', on_click=edit_product).props('color=warning')
                            ui.button('Delete', on_click=delete_product).props('color=negative')
        except Exception as e:
            with products_container:
                ui.label(f"Error loading products: {str(e)}").classes('text-red-500')

    add_button = ui.button('Add Product', on_click=add_product).props('color=primary')
    asyncio.create_task(refresh_products())

# Orders Page
@ui.page('/orders')
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
                    
                    message_input = ui.input('Message to customer').props('filled')
                    async def send_message():
                        await db.collection('orders').document(doc.id).update({
                            'message': message_input.value
                        })
                        ui.notify('Message sent!')
                    ui.button('Send Message', on_click=send_message).props('color=primary')
                    
    asyncio.create_task(refresh_orders())

# Messaging Page
@ui.page('/messages')
def messages_page():
    with ui.column().classes('w-full'):
        ui.label('Customer Communication').classes('text-h5')
        messages_container = ui.column()
        
    async def refresh_messages():
        messages_container.clear()
        docs = db.collection('messages').stream()
        async for doc in docs:
            message = doc.to_dict()
            with messages_container:
                ui.label(f"From: {message.get('from', 'N/A')}")
                ui.label(f"Message: {message.get('text', '')}")
                ui.separator()
                
    message_input = ui.textarea('New Message').props('filled')
    async def send_message():
        await db.collection('messages').add({
            'from': 'Admin',
            'text': message_input.value,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        message_input.value = ''
        await refresh_messages()
        
    ui.button('Send', on_click=send_message).props('color=primary')
    asyncio.create_task(refresh_messages())

# Main Dashboard
@ui.page('/')
def dashboard():
    with ui.header().classes('items-center bg-black'):
        ui.label('E-commerce Dashboard').classes('text-h3 colors-white')
    with ui.row().classes('w-full justify-center items-center'):
        ui.space()
        with ui.card().classes('cursor-pointer') as productCard:
            ui.label('Products').classes('text-center text-h6 m-4')
            ui.image('https://cdn-icons-png.flaticon.com/128/1186/1186286.png').classes('w-32 h-32')
        productCard.on('click', lambda: ui.open('/products'))
        
        with ui.card().classes('cursor-pointer') as orders:
            ui.label('Orders').classes('text-center text-h6 m-4')
            ui.image('https://cdn-icons-png.flaticon.com/128/9510/9510393.png').classes('w-32 h-32')
        orders.on('click', lambda: ui.open('/orders'))
        
        with ui.card().classes('cursor-pointer') as notefucation:
            ui.label('messages').classes('text-center text-h6 m-4')
            ui.image('https://cdn-icons-png.flaticon.com/128/1827/1827295.png').classes('w-32 h-32')
        notefucation.on('click', lambda: ui.open('/messages'))
        ui.space() 
app.add_static_files('/static', 'static')
ui.run(title='E-commerce Dashboard')