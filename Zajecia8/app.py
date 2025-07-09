import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

CITIES = {
    "Warsaw": {"lat": 52.2297, "lon": 21.0122},
    "Krakow": {"lat": 50.0647, "lon": 19.9450},
    "Gdansk": {"lat": 54.3520, "lon": 18.6466},
    "Wroclaw": {"lat": 51.1079, "lon": 17.0385}
}

def get_connection():
    return sqlite3.connect('sales.db')

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL,
            latitude REAL,
            longitude REAL
        )
    ''')
    cursor.execute("PRAGMA table_info(sales)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'latitude' not in columns or 'longitude' not in columns:
        cursor.execute('ALTER TABLE sales ADD COLUMN latitude REAL')
        cursor.execute('ALTER TABLE sales ADD COLUMN longitude REAL')
    conn.commit()
    conn.close()

def fetch_sales():
    conn = get_connection()
    query = "SELECT id, product, quantity, price, date, latitude, longitude FROM sales"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def add_sale(product, quantity, price, date, latitude, longitude):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sales (product, quantity, price, date, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)", 
                   (product, quantity, price, date, latitude, longitude))
    conn.commit()
    conn.close()

st.title("Sales Dashboard")
init_db()

st.header("Add New Sale")
with st.form(key="add_sale_form"):
    product = st.text_input("Product", placeholder="Enter product name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    price = st.number_input("Price (PLN)", min_value=0.01, step=0.01)
    date = st.date_input("Date", value=datetime.today())
    city = st.selectbox("Store Location", options=list(CITIES.keys()))
    submit_button = st.form_submit_button("Add Sale")

    if submit_button:
        if product and city:
            latitude = CITIES[city]["lat"]
            longitude = CITIES[city]["lon"]
            add_sale(product, quantity, price, date.strftime('%Y-%m-DD'), latitude, longitude)
            st.success("Sale added successfully!")
            st.balloons()
        else:
            st.error("Product name and location are required!")

st.header("Sales Data")
df = fetch_sales()

st.subheader("Filter Data")
col1, col2 = st.columns(2)
with col1:
    products = ['All'] + sorted(df['product'].unique().tolist())
    selected_product = st.selectbox("Filter by Product", products)
with col2:
    dates = ['All'] + sorted(df['date'].unique().tolist())
    selected_date = st.selectbox("Filter by Date", dates)

filtered_df = df
if selected_product != 'All':
    filtered_df = filtered_df[filtered_df['product'] == selected_product]
if selected_date != 'All':
    filtered_df = filtered_df[filtered_df['date'] == selected_date]

st.dataframe(filtered_df, use_container_width=True)

st.header("Sales Locations")
if not filtered_df.empty and 'latitude' in filtered_df and 'longitude' in filtered_df:
    map_data = filtered_df[['latitude', 'longitude']].dropna()
    if not map_data.empty:
        st.map(map_data, use_container_width=True)
    else:
        st.warning("No valid location data available for the selected filters.")
else:
    st.warning("No data available to display on the map.")

st.header("Sales Analysis")
show_charts = st.checkbox("Show Sales Charts", value=True)

if show_charts:
    df['total_value'] = df['quantity'] * df['price']
    daily_sales = df.groupby('date')['total_value'].sum().reset_index()
    fig1 = px.line(daily_sales, x='date', y='total_value', 
                   title="Daily Sales Value (Quantity × Price)",
                   labels={'total_value': 'Total Value (PLN)', 'date': 'Date'})
    st.plotly_chart(fig1, use_container_width=True)

    product_sales = df.groupby('product')['quantity'].sum().reset_index()
    fig2 = px.bar(product_sales, x='product', y='quantity', 
                  title="Total Quantity Sold by Product",
                  labels={'quantity': 'Total Quantity', 'product': 'Product'})
    st.plotly_chart(fig2, use_container_width=True)