# src/nl2sql_assistant/prompts/sqlcoder_prompt.py

def build_sqlcoder_prompt(question: str, schema_ddl: str) -> str:
    """
    Build prompt for defog/sqlcoder-7b-2.
    
    Format based on model's training:
    - Question first
    - DDL statements with table schemas
    - Clear instruction
    """
    prompt = f"""### Task
Generate a SQL query to answer the following question: `{question}`

### Database Schema
The following are the CREATE TABLE statements for the database:

{schema_ddl}

### Instructions
- Return only the SQL query, nothing else
- Use standard SQL syntax
- Ensure the query is safe (SELECT only, no DROP/DELETE/UPDATE)
- Use proper JOIN conditions when accessing multiple tables

### SQL Query
"""
    return prompt


def extract_schema_ddl(schema: Dict) -> str:
    """
    Convert internal schema dict to DDL format.
    
    Example output:
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100)
    );
    """
    ddl_statements = []
    
    for table_name, columns in schema.items():
        col_defs = []
        for col in columns:
            col_def = f"    {col['name']} {col['type']}"
            if col.get('primary_key'):
                col_def += " PRIMARY KEY"
            col_defs.append(col_def)
        
        ddl = f"CREATE TABLE {table_name} (\n"
        ddl += ",\n".join(col_defs)
        ddl += "\n);"
        ddl_statements.append(ddl)
    
    return "\n\n".join(ddl_statements)