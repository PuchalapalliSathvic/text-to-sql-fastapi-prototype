"""
Text-to-SQL FastAPI Prototype with Mock LLaMA 3 Integration.

This application exposes a /text_to_sql endpoint that:
  1. Accepts a natural language query.
  2. Converts it to SQL using a placeholder function that simulates LLaMA 3.
  3. Executes the SQL against an in-memory SQLite database.
  4. Returns both the simulated SQL and the query result.

Run with:
    uvicorn main:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel

from llama_mock import generate_sql
from database import init_db, run_query

app = FastAPI(
    title="Text-to-SQL Prototype",
    description="Converts natural language to SQL using a mock LLaMA 3 model.",
    version="1.0.0",
)

# Initialize the in-memory SQLite database once at startup.
init_db()


class QueryRequest(BaseModel):
    """Request body for the /text_to_sql endpoint."""
    query: str


class QueryResponse(BaseModel):
    """Response body returned by the /text_to_sql endpoint."""
    natural_language_query: str
    generated_sql: str
    result: list
    recognized: bool


@app.get("/")
def root():
    """Simple health-check / landing endpoint."""
    return {
        "message": "Text-to-SQL prototype is running.",
        "usage": 'POST /text_to_sql with body {"query": "show me users"}',
    }


@app.post("/text_to_sql", response_model=QueryResponse)
def text_to_sql(request: QueryRequest):
    """
    Convert a natural language query to SQL and execute it.

    Example:
        Request:  {"query": "show me users"}
        Response: {
            "natural_language_query": "show me users",
            "generated_sql": "SELECT * FROM users;",
            "result": [[1, "Alice", "alice@example.com"], ...],
            "recognized": true
        }
    """
    sql, recognized = generate_sql(request.query)

    # Only execute against the DB if we produced a runnable SELECT statement.
    result = run_query(sql) if recognized else []

    return QueryResponse(
        natural_language_query=request.query,
        generated_sql=sql,
        result=result,
        recognized=recognized,
    )
