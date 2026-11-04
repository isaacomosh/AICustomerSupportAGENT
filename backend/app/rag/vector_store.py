import chromadb
from flask import current_app

_col = None
state = {"stale": True}  # set True whenever products change so the next question re-syncs

def collection():
    global _col
    if _col is None:
        client = chromadb.PersistentClient(path=current_app.config["CHROMA_PATH"])
        _col = client.get_or_create_collection("store_kb", metadata={"hnsw:space": "cosine"})
    return _col

def existing_ids():
    return set(collection().get(include=[])["ids"])

def upsert(ids, docs, vecs, metas):
    collection().upsert(ids=ids, documents=docs, embeddings=[v.tolist() for v in vecs], metadatas=metas)

def prune(keep_ids):
    stale = list(existing_ids() - set(keep_ids))
    if stale: collection().delete(ids=stale)

def search(qvec, k=5):
    if collection().count() == 0: return []
    return collection().query(query_embeddings=[qvec.tolist()], n_results=k)["documents"][0]
