from __future__ import annotations

from langchain_core.prompts import PromptTemplate

# Few-shot examples are intentionally small and realistic.
# We'll expand these later as the project grows.
FEW_SHOT_EXAMPLES = """
Example 1:
Schema:
TABLE customers:
  - customer_id : INTEGER (PK, NOT NULL)
  - name : TEXT (NOT NULL)

TABLE orders:
  - order_id : INTEGER (PK, NOT NULL)
  - customer_id : INTEGER (NOT NULL)
  - order_date : TEXT (NOT NULL)
  - status : TEXT (NOT NULL)

Question: List completed orders with customer name.
SQL:
SELECT c.name, o.order_id, o.order_date
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.status = 'completed'
ORDER BY o.order_date DESC;

Example 2:
Schema:
TABLE products:
  - product_id : INTEGER (PK, NOT NULL)
  - name : TEXT (NOT NULL)
  - category : TEXT
  - price : REAL (NOT NULL)

Question: Show all products in Electronics ordered by price descending.
SQL:
SELECT name, price
FROM products
WHERE category = 'Electronics'
ORDER BY price DESC;
""".strip()


SQL_PROMPT = PromptTemplate(
    input_variables=["schema_text", "question"],
    template=(
        "You are an expert data analyst. Generate a single SQLite SELECT query.\n"
        "Rules:\n"
        "1) Output ONLY SQL (no markdown, no backticks).\n"
        "2) Use ONLY SELECT queries. No INSERT/UPDATE/DELETE/DROP/ALTER.\n"
        "3) Use the provided schema exactly. Do not invent columns.\n"
        "4) If the question is ambiguous, choose the safest reasonable interpretation.\n"
        "5) Prefer explicit JOIN conditions.\n\n"
        "Few-shot examples:\n"
        "{few_shot}\n\n"
        "Schema:\n"
        "{schema_text}\n\n"
        "Question: {question}\n"
        "SQL:"
    ),
    partial_variables={"few_shot": FEW_SHOT_EXAMPLES},
)
