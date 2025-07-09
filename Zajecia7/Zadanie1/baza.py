import sqlite3
from datetime import datetime

conn = sqlite3.connect('sales.db')
cursor = conn.cursor()

print("a) Sales of product 'Laptop':")
cursor.execute("SELECT * FROM sales WHERE product = 'Laptop'")
laptop_sales = cursor.fetchall()
for sale in laptop_sales:
    print(sale)

print("\nb) Sales on 2025-05-07 and 2025-05-08:")
cursor.execute("SELECT * FROM sales WHERE date IN ('2025-05-07', '2025-05-08')")
date_sales = cursor.fetchall()
for sale in date_sales:
    print(sale)

print("\nc) Transactions with price > 200:")
cursor.execute("SELECT * FROM sales WHERE price > 200")
high_price_sales = cursor.fetchall()
for sale in high_price_sales:
    print(sale)

print("\nd) Total sales value per product:")
cursor.execute("SELECT product, SUM(quantity * price) as total_value FROM sales GROUP BY product")
total_values = cursor.fetchall()
for product, total in total_values:
    print(f"Product: {product}, Total Value: {total:.2f}")

print("\ne) Day with the highest number of items sold:")
cursor.execute("SELECT date, SUM(quantity) as total_quantity FROM sales GROUP BY date ORDER BY total_quantity DESC LIMIT 1")
top_day = cursor.fetchone()
print(f"Date: {top_day[0]}, Total Items Sold: {top_day[1]}")

conn.close()