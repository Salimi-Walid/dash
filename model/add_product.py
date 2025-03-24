from nicegui import ui
from Supabase.service import SUPABASE_KEY,SUPABASE_URL
import supabase
from firebase.service import db
import asyncio
from supabase import create_client, Client
import uuid
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Categories
categores = ['Chaise', 'Table', 'Étagères', 'Décorations']

def product_content(contentscren):
    contentscren.clear()
    with contentscren:
        with ui.card().classes('w-full h-25 justify-center items-center'):
            with ui.row():
                ui.icon('warning', color='Red').classes('text-h6 ')
                ui.label('Veuillez saisir toutes les informations sur le produit avant de l\'ajouter.').classes('text-center')

        with ui.row().classes('w-full'):
            ui.label('Product Name:')
            ui.space()
            name = ui.input('Product Name').props('filled')

        with ui.row().classes('w-full'):
            ui.label('Product Description:')
            ui.space()
            description = ui.textarea('Description').props('filled')

        with ui.row().classes('w-full'):
            ui.label('Product Image:')
            ui.space()
            image_upload = ui.upload(on_upload=lambda e: handle_image_upload(e)).classes('max-w-full').props('filled')

        with ui.row().classes('w-full'):
            ui.label('Quantity in Stock:')
            ui.space()
            quantity = ui.number('Quantity').props('filled')

        with ui.row().classes('w-full'):
            ui.label('Product Price:')
            ui.space()
            price = ui.number('Price').props('filled')

        with ui.row().classes('w-full'):
            ui.label('Prix de livraison en ville:')
            ui.space()
            prix_livraison_ville = ui.number('Prix en ville').props('filled')

        with ui.row().classes('w-full'):
            ui.label('Prix de livraison hors ville:')
            ui.space()
            prix_livraison_hors_ville = ui.number('Prix hors ville').props('filled')

        with ui.row().classes('w-full'):
            ui.label('Category:')
            ui.space()
            category = ui.select(categores, multiple=True, value=categores[:1], label='Categories').classes('w-50').props('use-chips filled')

        # Hidden input to store image URL
        hidden_image_url = ui.input('', visible=False)

        # Status label for errors
        status_label = ui.label('').classes('text-red-500')

        # Handle Image Upload
        async def handle_image_upload(e):
            try:
                # Generate unique filename
                file_ext = e.name.split('.')[-1]
                file_name = f"{uuid.uuid4()}.{file_ext}"

                # Upload to Supabase Storage (Bucket: image_products)
                await asyncio.to_thread(
                    supabase.storage.from_("image_prpduct").upload,
                    file_name,
                    e.content.read(),
                    {"content-type": e.type}
                )

                # Get public URL
                image_url = f"{SUPABASE_URL}/storage/v1/object/public/image_prpduct/{file_name}"

                # Store the URL in hidden input
                hidden_image_url.set_value(image_url)

                ui.notify(f'Image {e.name} téléchargée avec succès!')

            except Exception as ex:
                ui.notify(f"Erreur de téléchargement: {str(ex)}", color='negative')

        # Add Product to Firestore
        async def add_product():
            try:
                # Retrieve the stored image URL
                image_url = hidden_image_url.value

                if not image_url:
                    ui.notify("Veuillez télécharger une image.", color='negative')
                    return

                product_data = {
                    'name': name.value,
                    'price': float(price.value),
                    'description': description.value,
                    'image': image_url,
                    'quantity': int(quantity.value),
                    'prix_livraison_ville': prix_livraison_ville.value,
                    'prix_livraison_hors_ville': prix_livraison_hors_ville.value,
                    'category': category.value
                }

                # Store product details in Firestore
                await asyncio.to_thread(db.collection('products').add, product_data)

                ui.notify('Produit ajouté avec succès!')

            except Exception as e:
                status_label.set_text(f"Erreur: {str(e)}")

        # Button to add product
        ui.button('Add Product', icon='add', on_click=lambda:add_product()).props('color=primary')
