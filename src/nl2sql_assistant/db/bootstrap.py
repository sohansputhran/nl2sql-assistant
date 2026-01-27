from __future__ import annotations

import sqlite3
from pathlib import Path


def ensure_sample_db(db_path: Path) -> Path:
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")

        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS customers (
              customer_id INTEGER PRIMARY KEY,
              name TEXT NOT NULL,
              email TEXT UNIQUE,
              country TEXT
            );

            CREATE TABLE IF NOT EXISTS products (
              product_id INTEGER PRIMARY KEY,
              name TEXT NOT NULL,
              category TEXT,
              price REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS orders (
              order_id INTEGER PRIMARY KEY,
              customer_id INTEGER NOT NULL,
              order_date TEXT NOT NULL,
              status TEXT NOT NULL,
              FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
            );

            CREATE TABLE IF NOT EXISTS order_items (
              order_item_id INTEGER PRIMARY KEY,
              order_id INTEGER NOT NULL,
              product_id INTEGER NOT NULL,
              quantity INTEGER NOT NULL,
              unit_price REAL NOT NULL,
              FOREIGN KEY(order_id) REFERENCES orders(order_id),
              FOREIGN KEY(product_id) REFERENCES products(product_id)
            );
            """
        )

        # Seed data only if empty
        cur = conn.execute("SELECT COUNT(*) FROM customers;")
        if cur.fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO customers(name, email, country) VALUES (?, ?, ?);",
                [
                    ("Asha Rao", "asha@example.com", "India"),
                    ("Miguel Silva", "miguel@example.com", "Portugal"),
                    ("Emma Johnson", "emma@example.com", "USA"),
                    ("Liam Chen", "liam@example.com", "Canada"),
                ],
            )

        cur = conn.execute("SELECT COUNT(*) FROM products;")
        if cur.fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO products(name, category, price) VALUES (?, ?, ?);",
                [
                    ("Wireless Mouse", "Electronics", 25.0),
                    ("Mechanical Keyboard", "Electronics", 90.0),
                    ("Coffee Beans 1kg", "Grocery", 18.5),
                    ("Running Shoes", "Sports", 120.0),
                ],
            )

        cur = conn.execute("SELECT COUNT(*) FROM orders;")
        if cur.fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO orders(customer_id, order_date, status) VALUES (?, ?, ?);",
                [
                    (1, "2025-11-15", "completed"),
                    (2, "2025-12-02", "completed"),
                    (3, "2026-01-05", "processing"),
                    (1, "2026-01-18", "completed"),
                ],
            )

        cur = conn.execute("SELECT COUNT(*) FROM order_items;")
        if cur.fetchone()[0] == 0:
            conn.executemany(
                "INSERT INTO order_items(order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?);",
                [
                    (1, 1, 2, 25.0),
                    (1, 3, 1, 18.5),
                    (2, 2, 1, 90.0),
                    (3, 4, 1, 120.0),
                    (4, 1, 1, 25.0),
                    (4, 2, 1, 90.0),
                ],
            )

    return db_path
