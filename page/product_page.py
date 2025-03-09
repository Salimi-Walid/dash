import asyncio
from nicegui import ui
from firebase.service import db

def products_page():
    with ui.header().classes('bg-black'):
        ui.icon('arrow_back').classes('text-h4 color-white cursor-pointer').on('click', lambda: ui.run_javascript('window.history.back()'))
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
                            await asyncio.to_thread(db.collection('products').document(doc_id).delete)
                            ui.notify('Product deleted!')
                            await refresh_products()

                        with ui.row():
                            ui.button('Delete', on_click=delete_product).props('color=negative')
        except Exception as e:
            ui.label(f"Error loading products: {str(e)}").classes('text-red-500')

    asyncio.create_task(refresh_products())
