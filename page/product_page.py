import asyncio
from nicegui import ui
from firebase.service import db
from model.add_product import product_content
from model.my_product import my_products
def products_page():
    with ui.header().classes('bg-black'):
        ui.icon('arrow_back').classes('text-h4 color-white cursor-pointer').on('click', lambda: ui.run_javascript('window.history.back()'))
        ui.label('Add New Product').classes('text-h5 color-white')    
    with ui.row().classes('w-full '):
        with ui.column().classes('w-30 text-center'):
            with ui.card().classes('justify-center items-center cursor-pointer h-16 w-full') as tutorial:
                with ui.row():
                    ui.icon('school').classes('text-h5 m-4')
                    ui.label('Tutorial').classes('text-h6 m-4 text-center')
            tutorial.on('click', lambda: ui.notify('comming soon'))
            with ui.card().classes('justify-center items-center cursor-pointer h-16 w-full') as add_product:
                with ui.row():
                    ui.icon('conveyor_belt').classes('text-h5 m-4')
                    ui.label('Add Product').classes('text-h6 m-4 text-center')
            add_product.on('click', lambda: product_content(content))
            with ui.card().classes('justify-center items-center cursor-pointer h-16 w-full') as my_product:
                with ui.row():
                    ui.icon('inventory_2').classes('text-h5 m-4')
                    ui.label('My Product').classes('text-h6 m-4')
            my_product.on('click', lambda: my_products(content))
            with ui.card().classes('justify-center items-center cursor-pointer h-16 w-full ') as best_product:
                with ui.row():
                    ui.icon('star').classes('text-h5 m-4')
                    ui.label('Best Product').classes('text-h6 m-4')
            best_product.on('click', lambda: print('caming soon'))
        ui.separator().classes('h-full w-1 bg-black mx-4')
        with ui.column().classes('w-65 ') as content:
            with ui.card().classes('w-65 h-25 '):
                ui.label('If you have any problems adding the product to the application database, please watch the tutorial below.')
            ui.video('video/2025-02-24 21-41-57.mp4').classes('w-full h-60 object-contain')
            with ui.card().classes('w-65 h-25 '):
                ui.label('All information related to the products displayed in the application. Click here. Please watch the video to learn how to modify the displayed products.')  
            ui.video('video/2025-02-24 21-41-57.mp4').classes('w-full h-60 object-contain')
        
