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

---

## Step-by-step: how to run and access the app

Follow these steps in order. Commands are for macOS/Linux; Windows notes are
included where they differ.

### Step 1 — Open a terminal in the project folder

Navigate into the folder that contains `main.py`:

```bash
cd text_to_sql_app
```

### Step 2 — Create a virtual environment

```bash
python -m venv venv
```

### Step 3 — Activate the virtual environment

macOS / Linux:

```bash
source venv/bin/activate
```

Windows (PowerShell):

```bash
venv\Scripts\activate
```

You should now see `(venv)` at the start of your terminal prompt.

### Step 4 — Install the dependencies

```bash
pip install -r requirements.txt
```

This installs FastAPI, Uvicorn, and Pydantic. It should finish in a few seconds.

### Step 5 — Start the server

```bash
uvicorn main:app --reload
```

You should see output ending with:

```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

The app is now running. Leave this terminal open while you test.

---

## Step-by-step: how to test the endpoint

There are two endpoints:

| URL                                | Method | Purpose                                  |
|------------------------------------|--------|------------------------------------------|
| `http://127.0.0.1:8000/`           | GET    | Health check. Confirms the server is up. |
| `http://127.0.0.1:8000/text_to_sql`| POST   | The actual text-to-SQL endpoint.         |

> **Important:** The `/text_to_sql` endpoint is a **POST** endpoint, so it needs
> a request body. You **cannot** test it by typing its URL into a browser
> address bar, because browsers only send **GET** requests. To test it, use the
> interactive `/docs` page (Option A below) or curl (Option B below).
>
> Opening `http://127.0.0.1:8000/` in a browser will only show a short
> "prototype is running" message. That is expected. The query results come from
> `/text_to_sql`, not from the root URL.

### Option A — Test in the browser using the interactive docs (easiest)

1. Open this URL in your browser:

   ```
   http://127.0.0.1:8000/docs
   ```

2. You will see the auto-generated Swagger UI titled "Text-to-SQL Prototype".

3. Click on the green **POST `/text_to_sql`** row to expand it.

4. Click the **"Try it out"** button on the right.

5. In the **Request body** box, replace the placeholder with:

   ```json
   {
     "query": "show me users"
   }
   ```

6. Click the blue **Execute** button.

7. Scroll down to **Server response**. You should see:
   - **Code:** `200`
   - **Response body:** the generated SQL and the resulting rows, for example:

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

### Option B — Test using curl (command line)

Open a **second** terminal (leave the server running in the first one) and run:

```bash
curl -X POST "http://127.0.0.1:8000/text_to_sql" \
     -H "Content-Type: application/json" \
     -d '{"query": "show me users"}'
```

Expected response:

```json
{"natural_language_query":"show me users","generated_sql":"SELECT * FROM users;","result":[[1,"Alice","alice@example.com",30],[2,"Bob","bob@example.com",25],[3,"Charlie","charlie@example.com",35],[4,"Diana","diana@example.com",28]],"recognized":true}
```

### Step — Stop the server when done

In the terminal running the server, press:

```
CTRL + C
```

---

## Example queries to try

Send any of these as the `query` value in the request body:

| Natural language   | Generated SQL                       |
|--------------------|-------------------------------------|
| show me users      | SELECT * FROM users;                |
| list all users     | SELECT * FROM users;                |
| how many users     | SELECT COUNT(*) FROM users;         |
| names of users     | SELECT name FROM users;             |
| users above 30     | SELECT * FROM users WHERE age > 30; |
| show me products   | SELECT * FROM products;             |
| show me orders     | SELECT * FROM orders;               |

Queries that do not match a known pattern return a fallback message with
`recognized: false`, simulating where a real LLaMA 3 model would take over.

---

## How it works (brief)

1. The request hits the `/text_to_sql` POST endpoint in `main.py`.
2. `llama_mock.generate_sql()` simulates LLaMA 3 by matching keywords in the
   query to a known SQL statement.
3. If a statement is produced, `database.run_query()` executes it against the
   in-memory SQLite database (seeded with sample `users`, `products`, `orders`).
4. The endpoint returns the original query, the generated SQL, the result rows,
   and a `recognized` flag.