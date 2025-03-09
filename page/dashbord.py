from nicegui import ui

def dashboard():
    with ui.header().classes('items-center bg-black'):
        ui.label('E-commerce Dashboard').classes('text-h3 color-white')

    with ui.row().classes('w-full justify-center items-center'):
        ui.space()
        with ui.card().classes('cursor-pointer') as product_card:
            ui.label('Products').classes('text-center text-h6 m-4')
            ui.image('https://cdn-icons-png.flaticon.com/128/1186/1186286.png').classes('w-32 h-32')
        product_card.on('click', lambda: ui.open('/products'))

        with ui.card().classes('cursor-pointer') as orders_card:
            ui.label('Orders').classes('text-center text-h6 m-4')
            ui.image('https://cdn-icons-png.flaticon.com/128/9510/9510393.png').classes('w-32 h-32')
        orders_card.on('click', lambda: ui.open('/orders'))

        with ui.card().classes('cursor-pointer') as messages_card:
            ui.label('Messages').classes('text-center text-h6 m-4')
            ui.image('https://cdn-icons-png.flaticon.com/128/1827/1827295.png').classes('w-32 h-32')
        messages_card.on('click', lambda: ui.open('/messages'))

        ui.space()
