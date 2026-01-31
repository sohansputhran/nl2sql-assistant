# Data Dictionary

customers
- customer_id: primary key
- name: customer full name
- email: unique email
- country: customer country

orders
- order_id: primary key
- customer_id: FK -> customers.customer_id
- order_date: ISO date (YYYY-MM-DD)
- status: one of: completed, processing

order_items
- order_item_id: primary key
- order_id: FK -> orders.order_id
- product_id: FK -> products.product_id
- quantity: integer units purchased
- unit_price: captured price at purchase time

products
- product_id: primary key
- name: product name
- category: category label
- price: current list price
