
from nicegui import ui
from model.my_orders import myOrder
from model.my_stuts import mystuts
def orders_page():
    with ui.header().classes('bg-black'):
        ui.icon('arrow_back').classes('text-h4 color-white cursor-pointer').on('click', lambda: ui.run_javascript('window.history.back()'))
        ui.label('Oreder page').classes('text-h5 color-white')    
    with ui.row().classes('w-full '):
        with ui.column().classes('w-30 text-center'):
            with ui.card().classes('justify-center items-center cursor-pointer h-16 w-full') as my_order:
                with ui.row():
                    ui.icon('conveyor_belt').classes('text-h5 m-4')
                    ui.label('My Order').classes('text-h6 m-4 text-center')
            my_order.on('click', lambda: myOrder(content))
            with ui.card().classes('justify-center items-center cursor-pointer h-16 w-full') as my_stutes:
                with ui.row():
                    ui.icon('inventory_2').classes('text-h5 m-4')
                    ui.label('My Stutes').classes('text-h6 m-4')
            my_stutes.on('click', lambda: mystuts(content))
            with ui.card().classes('justify-center items-center cursor-pointer h-16 w-full ') as best_product:
                with ui.row():
                    ui.icon('star').classes('text-h5 m-4')
                    ui.label('client Revies').classes('text-h6 m-4')
            best_product.on('click', lambda: ui.notify('comming soon'))
        ui.separator().classes('h-full w-1 bg-black mx-4')
        with ui.column().classes('w-65 ') as content:
            pass


