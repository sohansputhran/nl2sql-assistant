from nl2sql_assistant.rag.corpus import RagCorpus
from nl2sql_assistant.rag.retriever_bm25 import build_index, retrieve


def test_retrieve_returns_relevant_chunk():
    corpus = RagCorpus(
        chunks=[
            "TABLE customers:\n  - customer_id\n  - name\n  - email\n",
            "TABLE orders:\n  - order_id\n  - status\n",
        ]
    )
    idx = build_index(corpus)
    ctx = retrieve(idx, "update order status", k=1)
    assert "orders" in ctx.lower()
