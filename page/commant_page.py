import asyncio
from nicegui import ui
from firebase.service import db
from firebase_admin import  firestore
def messages_page():
    with ui.column().classes('w-full'):
        ui.label('Customer Communication').classes('text-h5')
        messages_container = ui.column()

    async def refresh_messages():
        messages_container.clear()
        docs = db.collection('messages').stream()
        async for doc in docs:
            message = doc.to_dict()
            with messages_container:
                ui.label(f"From: {message.get('from', 'N/A')}")
                ui.label(f"Message: {message.get('text', '')}")
                ui.separator()

    message_input = ui.textarea('New Message').props('filled')

    async def send_message():
        await db.collection('messages').add({
            'from': 'Admin',
            'text': message_input.value,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        message_input.value = ''
        await refresh_messages()

    ui.button('Send', on_click=send_message).props('color=primary')
    asyncio.create_task(refresh_messages())
