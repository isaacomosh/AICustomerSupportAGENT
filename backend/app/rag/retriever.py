from .embeddings import embed
from . import vector_store as vs, knowledge_base

def retrieve(query, k=5):
    if vs.state["stale"]:
        knowledge_base.build_index()
    return vs.search(embed([query], "RETRIEVAL_QUERY")[0], k)
