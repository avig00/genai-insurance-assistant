import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load token from .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize HF-compatible OpenAI client
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

# Load schema from project root regardless of working directory
def load_schema(schema_path: str = None) -> dict:
    if schema_path is None:
        base_dir = Path(__file__).resolve().parent.parent
        schema_path = base_dir / "schema" / "db_schema.json"
    with open(schema_path, "r") as f:
        return json.load(f)

# Format schema for LLM prompt
def format_schema_for_prompt(schema: dict) -> str:
    lines = ["You are a data assistant. Here's the schema:"]
    for table, meta in schema.items():
        columns = ", ".join(meta["columns"])
        lines.append(f"Table `{table}` with columns: {columns}")
    return "\n".join(lines)

# Build system + user prompt for the chat model
def build_messages(question: str, schema: dict) -> list:
    schema_prompt = format_schema_for_prompt(schema)
    return [
        {"role": "system", "content": schema_prompt},
        {"role": "user", "content": f"Write an SQL query to answer: {question}"},
    ]

# Call LLM via OpenAI-compatible HF router
# def generate_sql(question: str, schema_path: str = None, context_sql: str = None) -> str:
#     schema = load_schema(schema_path)

#     # Adjust the prompt if this is a follow-up query
#     if context_sql:
#         followup_prompt = f"""The user previously ran this SQL:

# {context_sql}

# Now they asked: "{question}"

# Generate SQL based on the previous context and the current question.
# """
#         messages = build_messages(followup_prompt, schema)
#     else:
#         messages = build_messages(question, schema)

#     response = client.chat.completions.create(
#         model="defog/llama-3-sqlcoder-8b:featherless-ai",
#         messages=messages,
#     )
#     return response.choices[0].message.content.strip()

def generate_sql(question: str, schema_path: str = None, context_sql: str = None) -> str:
    schema = load_schema(schema_path)

    if context_sql:
        prompt = f"""The user previously ran this SQL:

{context_sql}

Now they asked: "{question}"

Generate follow-up SQL based on the previous context and the current question."""
    else:
        prompt = question

    messages = build_messages(prompt, schema)

    response = client.chat.completions.create(
        model="defog/llama-3-sqlcoder-8b:featherless-ai",
        messages=messages,
    )
    return response.choices[0].message.content.strip()


# Example usage
if __name__ == "__main__":
    question = "What is the average claim amount by line of business for closed claims?"
    sql = generate_sql(question)
    print("Generated SQL:\n", sql)
