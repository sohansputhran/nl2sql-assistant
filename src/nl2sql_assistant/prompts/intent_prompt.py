from langchain_core.prompts import PromptTemplate

# We keep the output extremely constrained so parsing is reliable.
INTENT_PROMPT = PromptTemplate(
    input_variables=["user_prompt"],
    template=(
        "Classify the user's request into one of: read, write, unknown.\n"
        "Return ONLY one token: read OR write OR unknown.\n\n"
        "User request:\n{user_prompt}\n\n"
        "Intent:"
    ),
)
