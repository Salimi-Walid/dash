from nicegui import ui, app
from page.dashbord import dashboard
from page.product_page import products_page
from page.order_page import orders_page
from page.commant_page import messages_page

# Register Pages
ui.page('/')(dashboard)
ui.page('/products')(products_page)
ui.page('/orders')(orders_page)
ui.page('/messages')(messages_page)

# Static Files
app.add_static_files('/static', 'static')

# Run the App
ui.run(title='E-commerce Dashboard')