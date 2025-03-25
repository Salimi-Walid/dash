from datetime import datetime, timedelta
from collections import defaultdict
import plotly.graph_objects as go
from nicegui import ui
from firebase.service import db

def monthly_orders_chart(content):
    content.clear()

    async def fetch_monthly_data():
        """Fetch and process orders from Firestore for the current month."""
        try:
            now = datetime.now()
            start_of_month = datetime(now.year, now.month, 1)
            end_of_month = start_of_month + timedelta(days=31)

            orders_ref = db.collection('orders')
            orders_docs = await orders_ref.where('order_date', '>=', start_of_month).where('order_date', '<', end_of_month).get()

            daily_orders = defaultdict(int)
            daily_profit = defaultdict(float)

            for doc in orders_docs:
                order_data = doc.to_dict()
                order_date = order_data.get('order_date').date()
                total = float(order_data.get('total', 0))
                cost = float(order_data.get('cost', 0))
                profit = total - cost

                daily_orders[order_date] += 1
                daily_profit[order_date] += profit

            return daily_orders, daily_profit

        except Exception as e:
            ui.notify(f"Error fetching data: {e}", color='negative')
            return {}, {}

    async def load_chart():
        """Load data and update the Plotly chart."""
        daily_orders, daily_profit = await fetch_monthly_data()

        if not daily_orders:
            ui.notify("No data available for the current month.", color='warning')
            return
        days = sorted(daily_orders.keys())
        order_counts = [daily_orders[day] for day in days]
        profits = [daily_profit[day] for day in days]
        order_trace = go.Scatter(x=days, y=order_counts, mode='lines+markers', name='Number of Orders')
        profit_trace = go.Scatter(x=days, y=profits, mode='lines+markers', name='Profit')

        # Define the layout
        layout = go.Layout(
            title='Daily Orders and Profit for the Current Month',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Count / Profit'),
            legend=dict(x=0, y=1)
        )

        # Create the figure
        fig = go.Figure(data=[order_trace, profit_trace], layout=layout)

        # Update the Plotly chart
        plotly_chart.figure = fig
        plotly_chart.update()

    with content:
        ui.label('📈 Monthly Orders and Profit').classes('text-h4')

        plotly_chart = ui.plotly()
        ui.button('🔄 Refresh Chart', icon='refresh', on_click=load_chart).props('color=primary')

        ui.timer(1, load_chart, once=True)
