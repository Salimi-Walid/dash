from nicegui import ui
from firebase.service import db
import asyncio


async def my_products(my_prods):
    my_prods.clear()
    def edit_product():
        with ui.dialog() as edit_dialog, ui.card():
            ui.label('Edit Product').classes('text-h5')
            name = ui.input('Product Name', value=product.get('name', '')).props('filled')
            price = ui.number('Price', value=product.get('price', 0)).props('filled')
            description = ui.textarea('Description', value=product.get('description', '')).props('filled')
            image_url = ui.input('Image URL', value=product.get('image_url', '')).props('filled')
            quantity = ui.number('Quantity', value=product.get('quntiter', 0)).props('filled')
            price_city = ui.number('Price Delivery (City)', value=product.get('prix_levrisent_ville', 0)).props('filled')
            price_non_city = ui.number('Price Delivery (Non-city)', value=product.get('prix_levrisent_Nonville', 0)).props('filled')

            async def update_product():
                try:
                    updated_product = {
                        'name': name.value,
                        'price': float(price.value),
                        'description': description.value,
                        'image_url': image_url.value,
                        'quntiter': quantity.value,
                        'prix_levrisent_ville': price_city.value,
                        'prix_levrisent_Nonville': price_non_city.value,
                    }
                    await asyncio.to_thread(
                        db.collection('products').document(doc.id).update,
                        updated_product
                    )
                    ui.notify('Product updated successfully!')
                    edit_dialog.close()
                    await my_products(my_prods)  # Refresh UI
                except Exception as e:
                    ui.notify(f"Update failed: {str(e)}", color='negative')

            ui.button('Save Changes', on_click=update_product).props('color=primary')
            ui.button('Cancel', on_click=edit_dialog.close).props('color=secondary')
        edit_dialog.open()
    with my_prods:
        ui.label('My Products').classes('text-gray-500')
    
    try:
        docs = await asyncio.to_thread(db.collection('products').get)
        if not docs:
            with my_prods:
                ui.label('No products found').classes('text-gray-500')
            return
        
        for doc in docs:
            product = doc.to_dict()

            with my_prods:
                with ui.row():
                    with ui.card().classes('mb-4 p-4'):
                        if 'image_url' in product:
                            ui.image(product['image_url']).classes('w-48 h-48 object-contain')
                        ui.label(f"Name: {product.get('name', 'N/A')}")
                        ui.label(f"ID: {doc.id}")
                        ui.label(f"Price: ${product.get('price', 0):.2f} DH")
                        ui.label(f"Description: {product.get('description', 'N/A')}")
                        ui.label(f"Quantity: {product.get('quntiter', 0):.2f}")
                        ui.label(f"Price Delivery (City): ${product.get('prix_levrisent_ville', 0):.2f} DH")
                        ui.label(f"Price Delivery (Non-city): ${product.get('prix_levrisent_Nonville', 0):.2f} DH")
                        async def delete_product(doc_id=doc.id):
                            try:
                                await asyncio.to_thread(
                                    db.collection('products').document(doc_id).delete
                                )
                                ui.notify('Product deleted!')
                                await my_products(my_prods)
                            except Exception as e:
                                ui.notify(f"Delete failed: {str(e)}", color='negative')

                        with ui.row():
                            ui.button('Edit', on_click=lambda: edit_product()).props('color=warning')
                            ui.button('Delete', on_click=lambda: delete_product(doc.id)).props('color=negative')

    except Exception as e:
        with my_prods:
            ui.label(f"Error loading products: {str(e)}").classes('text-red-500')

    