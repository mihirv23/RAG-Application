def build_prompt(
    question: str,
    retrieved_chunks: list[str]
):

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You must answer ONLY from the provided context.

If the answer is present in the context,
quote and summarize it.

If the answer is not present,
say:
'I could not find the answer in the document.'


Context:
{context}

Question:
{question}

Answer:
"""

    return prompt