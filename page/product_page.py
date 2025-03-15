import asyncio
from nicegui import ui
from firebase.service import db
def products_page():
    with ui.header().classes('bg-black'):
        ui.icon('arrow_back').classes('text-h4 color-white cursor-pointer').on('click', lambda: ui.run_javascript('window.history.back()'))
        ui.label('Add New Product').classes('text-h5 color-white')
    def product_content():
        content.clear()
        with content:
            name = ui.input('Product Name').props('filled')
            description = ui.textarea('Description').props('filled')
            #image=ui.upload(on_upload=lambda e: ui.notify(f'Uploaded {e.name}')).classes('max-w-full').props('filled')
            quntiter= ui.number('Quntiter').props('filled')
            price = ui.number('Price').props('filled')
            prix_levrisent_ville= ui.number('Quntiter').props('filled')
            prix_levrisent_Nonville= ui.number('Quntiter').props('filled')
            
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
            ui.button('Add Product', on_click=add_product).props('color=primary')
    with ui.row().classes('w-full '):
        with ui.column().classes('w-30 text-center'):
            with ui.card().classes('justify-center items-center cursor-pointer h-16 w-30') as add_product:
                with ui.row():
                    ui.icon('conveyor_belt').classes('text-h6 m-4')
                    ui.label('Add Product').classes('text-h6 m-4 text-center')
            add_product.on('click', lambda: product_content())
            with ui.card().classes('justify-center items-center cursor-pointer h-16 w-30') as my_product:
                with ui.row():
                    ui.icon('inventory_2').classes('text-h6 m-4')
                    ui.label('My Product').classes('text-h6 m-4')
            my_product.on('click', lambda: print('caming soon'))
            with ui.card().classes('justify-center items-center cursor-pointer h-16 w-30 ') as best_product:
                with ui.row():
                    ui.icon('star').classes('text-h6 m-4')
                    ui.label('Best Product').classes('text-h6 m-4')
            best_product.on('click', lambda: print('caming soon'))
        ui.separator().classes('h-full w-1 bg-black mx-4')
        with ui.column().classes('w-65 ') as content:
            pass
        
