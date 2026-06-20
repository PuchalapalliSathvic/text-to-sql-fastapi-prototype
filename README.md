# Text-to-SQL FastAPI Prototype (Mock LLaMA 3)

A basic prototype that converts natural language queries into SQL and executes
them against an in-memory SQLite database. The LLaMA 3 model is simulated with a
placeholder rule-based function.

## Project structure

```
text_to_sql_app/
├── main.py            # FastAPI app and /text_to_sql endpoint
├── llama_mock.py      # Mock LLaMA 3 natural-language-to-SQL conversion
├── database.py        # In-memory SQLite schema, seed data, query execution
├── requirements.txt   # Dependencies
└── README.md
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000
Interactive docs (Swagger UI): http://127.0.0.1:8000/docs

## Test the endpoint

Using curl:

```bash
curl -X POST "http://127.0.0.1:8000/text_to_sql" \
     -H "Content-Type: application/json" \
     -d '{"query": "show me users"}'
```

Expected response:

```json
{
  "natural_language_query": "show me users",
  "generated_sql": "SELECT * FROM users;",
  "result": [
    [1, "Alice", "alice@example.com", 30],
    [2, "Bob", "bob@example.com", 25],
    [3, "Charlie", "charlie@example.com", 35],
    [4, "Diana", "diana@example.com", 28]
  ],
  "recognized": true
}
```

## Example queries to try

| Natural language              | Generated SQL                              |
|-------------------------------|--------------------------------------------|
| show me users                 | SELECT * FROM users;                       |
| list all users                | SELECT * FROM users;                       |
| how many users                | SELECT COUNT(*) FROM users;                |
| names of users                | SELECT name FROM users;                    |
| users above 30                | SELECT * FROM users WHERE age > 30;        |
| show me products              | SELECT * FROM products;                    |
| show me orders                | SELECT * FROM orders;                      |

Queries that do not match a known pattern return a fallback message with
`recognized: false`, simulating where a real LLaMA 3 model would take over.
