"""
Mock LLaMA 3 text-to-SQL conversion.

In a production system this module would call a real LLaMA 3 model to translate
natural language into SQL. For this prototype, we simulate that behavior using
simple keyword matching against a set of known query patterns.

The function returns a tuple of (sql_string, recognized_flag) so the caller can
distinguish a confident match from a fallback.
"""

from typing import Tuple

# Ordered list of (keywords, sql) rules. The first rule whose keywords all
# appear in the lowercased query wins. Keep more specific rules before more
# general ones.
_RULES = [
    (["users", "above", "30"], "SELECT * FROM users WHERE age > 30;"),
    (["how many", "users"], "SELECT COUNT(*) FROM users;"),
    (["count", "users"], "SELECT COUNT(*) FROM users;"),
    (["names", "users"], "SELECT name FROM users;"),
    (["show", "users"], "SELECT * FROM users;"),
    (["list", "users"], "SELECT * FROM users;"),
    (["all", "users"], "SELECT * FROM users;"),
    (["products"], "SELECT * FROM products;"),
    (["orders"], "SELECT * FROM orders;"),
]

_FALLBACK_SQL = (
    "-- Could not confidently map this query to SQL. "
    "A real LLaMA 3 model would handle this case."
)


def generate_sql(natural_language_query: str) -> Tuple[str, bool]:
    """
    Simulate LLaMA 3's natural-language-to-SQL conversion.

    Args:
        natural_language_query: The user's plain-English request.

    Returns:
        A tuple (sql, recognized) where:
          - sql is the generated SQL string.
          - recognized is True if a known pattern matched, else False.
    """
    query = natural_language_query.lower().strip()

    for keywords, sql in _RULES:
        if all(keyword in query for keyword in keywords):
            return sql, True

    return _FALLBACK_SQL, False
