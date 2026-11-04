import time
import numpy as np
from flask import current_app
from google import genai
from google.genai import types, errors

_client = None
def client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=current_app.config["GEMINI_API_KEY"])
    return _client

def with_retry(fn, tries=3):
    """Retry temporary Gemini failures (503 overloaded, 429 rate limit) with 1s, 2s, 4s backoff."""
    for n in range(tries):
        try:
            return fn()
        except (errors.ServerError, errors.ClientError) as e:
            if (e.code not in (429, 500, 503)) or n == tries - 1:
                raise
            time.sleep(2 ** n)

def embed(texts, task="RETRIEVAL_DOCUMENT"):
    out = []
    for i in range(0, len(texts), 90):  # batch limit
        batch = texts[i:i + 90]
        r = with_retry(lambda: client().models.embed_content(
            model=current_app.config["EMBED_MODEL"], contents=batch,
            config=types.EmbedContentConfig(task_type=task)))
        out += [e.values for e in r.embeddings]
    return np.array(out, dtype="float32")
