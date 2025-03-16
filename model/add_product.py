from nicegui import ui
from firebase_admin import firestore  # Ensure Firebase is initialized elsewhere
import asyncio
import supabase
import uuid  # For unique filenames

# Supabase configuration
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_KEY"
supabase_client = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

# Firestore database reference
db = firestore.client()

categories = ['Chaise', 'table', 'étagères', 'décorations']

def product_content(contentscren):
    contentscren.clear()
    image_url = None  # To store the Supabase image URL

    with contentscren:
        # Warning banner
        with ui.card().classes('w-full h-25 justify-center items-center'):
            with ui.row():
                ui.icon('warning', color='Red').classes('text-h6')
                ui.label('Veuillez saisir toutes les informations').classes('text-center')
        
        # Product Name
        with ui.row().classes('w-full'):
            ui.label('Product Name :')
            ui.space()
            name = ui.input('Product Name').props('filled')
        
        # Description
        with ui.row().classes('w-full'):
            ui.label('Product Description :')
            ui.space()
            description = ui.textarea('Description').props('filled')
        
        # Image Upload
        with ui.row().classes('w-full'):
            ui.label('Product Image :')
            ui.space()
            
            async def handle_upload(e):
                nonlocal image_url
                try:
                    # Generate unique filename
                    file_ext = e.name.split('.')[-1]
                    file_name = f"{uuid.uuid4()}.{file_ext}"
                    
                    # Upload to Supabase [[8]]
                    await supabase_client.storage.from_('product_images').upload(
                        file_name,
                        e.content,
                        {"content-type": e.type}
                    )
                    
                    # Get public URL
                    image_url = supabase_client.storage.from_('product_images').get_public_url(file_name)
                    ui.notify(f'Uploaded {e.name}')
                except Exception as ex:
                    ui.notify(f'Upload failed: {str(ex)}')

            ui.upload(
                on_upload=lambda e: asyncio.create_task(handle_upload(e)),
                auto_upload=True
            ).classes('max-w-full').props('filled')
        
        # Quantity
        with ui.row().classes('w-full'):
            ui.label('Quantité en stock :')
            ui.space()
            quntiter = ui.number('Quantité').props('filled')
        
        # Pricing
        with ui.row().classes('w-full'):
            ui.label('Prix :')
            ui.space()
            price = ui.number('Prix').props('filled')
        
        # Delivery prices
        with ui.row().classes('w-full'):
            ui.label('Prix livraison ville :')
            ui.space()
            prix_levrisent_ville = ui.number('Prix ville').props('filled')
        
        with ui.row().classes('w-full'):
            ui.label('Prix livraison non-ville :')
            ui.space()
            prix_levrisent_Nonville = ui.number('Prix non-ville').props('filled')
        
        # Category selection
        with ui.row().classes('w-full'):
            ui.label('Catégorie')
            ui.space()
            categore = ui.select(
                categories,
                multiple=True,
                value=categories[:1],
                label='Avec chips'
            ).classes('w-50').props('use-chips filled')
        
        # Status indicator
        status_label = ui.label('').classes('text-red-500')
        
        # Add product button
        async def add_product():
            required_fields = [
                name.value,
                description.value,
                image_url,
                quntiter.value,
                price.value,
                prix_levrisent_ville.value,
                prix_levrisent_Nonville.value,
                categore.value
            ]
            
            if not all(required_fields):
                status_label.set_text("Erreur: Tous les champs sont requis")
                return
            
            try:
                product_data = {
                    'name': name.value,
                    'description': description.value,
                    'image_url': image_url,
                    'quantity': quntiter.value,
                    'price': float(price.value),
                    'delivery_price_city': float(prix_levrisent_ville.value),
                    'delivery_price_non_city': float(prix_levrisent_Nonville.value),
                    'categories': categore.value,
                    'created_at': firestore.SERVER_TIMESTAMP
                }
                
                # Add to Firestore
                await db.collection('products').add(product_data)
                ui.notify('Produit ajouté avec succès!')
                
                # Clear form
                name.set_value('')
                description.set_value('')
                quntiter.set_value(0)
                price.set_value(0)
                prix_levrisent_ville.set_value(0)
                prix_levrisent_Nonville.set_value(0)
                categore.set_value([])
                nonlocal image_url
                image_url = None
                
            except Exception as e:
                status_label.set_text(f"Erreur: {str(e)}")
        
        ui.button('Ajouter Produit', icon='add', on_click=add_product).props('color=primary')