"""
In-memory SQLite database for the Text-to-SQL prototype.

Creates a small sample schema (users, products, orders) and seeds it with a few
rows so that generated SQL queries return meaningful results.

A single shared in-memory connection is used. The `check_same_thread=False`
flag lets FastAPI's worker threads reuse it during local development.
"""

import sqlite3
from typing import List

# A single shared in-memory connection. `:memory:` databases live only as long
# as the connection is open, so we keep one connection alive for the app.
_conn = sqlite3.connect(":memory:", check_same_thread=False)


def init_db() -> None:
    """Create the sample schema and seed it with data. Safe to call once."""
    cur = _conn.cursor()

    cur.executescript(
        """
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS orders;

        CREATE TABLE users (
            id    INTEGER PRIMARY KEY,
            name  TEXT NOT NULL,
            email TEXT NOT NULL,
            age   INTEGER NOT NULL
        );

        CREATE TABLE products (
            id    INTEGER PRIMARY KEY,
            name  TEXT NOT NULL,
            price REAL NOT NULL
        );

        CREATE TABLE orders (
            id       INTEGER PRIMARY KEY,
            user_id  INTEGER NOT NULL,
            product  TEXT NOT NULL,
            quantity INTEGER NOT NULL
        );
        """
    )

    cur.executemany(
        "INSERT INTO users (id, name, email, age) VALUES (?, ?, ?, ?);",
        [
            (1, "Alice", "alice@example.com", 30),
            (2, "Bob", "bob@example.com", 25),
            (3, "Charlie", "charlie@example.com", 35),
            (4, "Diana", "diana@example.com", 28),
        ],
    )

    cur.executemany(
        "INSERT INTO products (id, name, price) VALUES (?, ?, ?);",
        [
            (1, "Keyboard", 49.99),
            (2, "Monitor", 199.99),
            (3, "Mouse", 19.99),
        ],
    )

    cur.executemany(
        "INSERT INTO orders (id, user_id, product, quantity) VALUES (?, ?, ?, ?);",
        [
            (1, 1, "Keyboard", 2),
            (2, 2, "Monitor", 1),
            (3, 3, "Mouse", 4),
        ],
    )

    _conn.commit()


def run_query(sql: str) -> List[list]:
    """
    Execute a SQL string and return all rows as a list of lists.

    Any database error is caught and returned as a single-row error message so
    the API never crashes on a bad generated query.
    """
    try:
        cur = _conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return [list(row) for row in rows]
    except sqlite3.Error as exc:
        return [[f"SQL execution error: {exc}"]]
