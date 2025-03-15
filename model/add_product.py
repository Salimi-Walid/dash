from nicegui import ui
from firebase.service import db
import asyncio
categores=['Chaise','table','étagères','décorations']
def product_content(contentscren):
        contentscren.clear()
        with contentscren:
            with ui.card().classes('w-full h-25 justify-center items-center'):
                with ui.row():
                    ui.icon('warning',color='Red').classes('text-h6 ')
                    ui.label('Veuillez saisir toutes les informations sur le produit avant de ajouter à lapplication').classes('text-center')
            with ui.row().classes('w-full'):
                ui.label('Product Name :')
                ui.space()
                name = ui.input('Product Name').props('filled')
                
            with ui.row().classes('w-full'):
                ui.label('Product Description :')
                ui.space()
                description = ui.textarea('Description').props('filled')
            with ui.row().classes('w-full'):
                ui.label('Product Image :')
                ui.space()
                image=ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full').props('filled')
            with ui.row().classes('w-full'):
                ui.label('Quntiter on stock :')
                ui.space()
                quntiter= ui.number('Quntiter').props('filled')
            with ui.row().classes('w-full'):
                ui.label('Product Price :')
                ui.space()
                price = ui.number('Price').props('filled')
            with ui.row().classes('w-full'):
                ui.label('Prix de livresent ville :')
                ui.space()
                prix_levrisent_ville= ui.number('Prix livresent ville').props('filled')
            with ui.row().classes('w-full'):
                ui.label('Prix livresent non ville :')
                ui.space()
                prix_levrisent_Nonville= ui.number('Prix livresent non ville').props('filled')
            with ui.row().classes('w-full'):
                ui.label('Categore')
                ui.space()
                categore=ui.select(categores, multiple=True, value=categores[:1], label='with chips').classes('w-50').props('use-chips filled')
            status_label = ui.label('').classes('text-red-500')
            async def add_product():
                try:
                    product_data = {
                        'name': name.value,
                        'price': float(price.value),
                        'description': description.value,
                        #'image': image.value,
                        'quntiter': quntiter.value,
                        'prix_levrisent_ville': prix_levrisent_ville.value,
                        'prix_levrisent_Nonville': prix_levrisent_Nonville.value,
                    }
                    await asyncio.to_thread(db.collection('products').add, product_data)
                    ui.notify('Product added!')
                except Exception as e:
                    status_label.set_text(f"Error: {str(e)}") 
            ui.button('Add Product',icon='add', on_click=add_product).props('color=primary')
        