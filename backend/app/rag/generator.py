from flask import current_app
from google.genai import types, errors
from .embeddings import client, with_retry
from . import language

SYSTEM = """You are the customer assistant for an electronics store (smart-watches, VR headsets, controllers).
Answer questions ONLY from the CONTEXT provided: products, recommendations, orders, payments, delivery and store policies.
Quote prices and stock exactly as given. If the answer is not in the context, say you don't know and suggest
contacting store support. Be concise and friendly.
ORDERING: when the customer clearly asks to buy or order something, call draft_order. Never call it for hypothetical or
price questions. draft_order only prepares the order: tell the customer to review it and press the Confirm button; never say
the order is already placed. Use my_orders for order-status questions. If a tool reports the customer is not logged in, ask them to log in."""

def _ask(contents, config):
    models = [current_app.config["GEN_MODEL"]] + current_app.config["FALLBACK_MODELS"]
    for i, model in enumerate(models):  # if the main model stays overloaded, try the next one
        try:
            return with_retry(lambda: client().models.generate_content(model=model, contents=contents, config=config))
        except (errors.ServerError, errors.ClientError) as e:
            print(f"model {model} failed: {e}")
            if i == len(models) - 1: raise

def generate(question, contexts, history=(), lang="en", toolbox=None):
    ctx = "\n".join(f"- {c}" for c in contexts)
    contents = [types.Content(role=r, parts=[types.Part(text=t)]) for r, t in history]
    contents.append(types.Content(role="user", parts=[types.Part(text=f"CONTEXT:\n{ctx}\n\nQUESTION: {question}")]))
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM + "\n" + language.rule(lang),  # no temperature: Gemini 3.6+ deprecates sampling params
       
        tools=[types.Tool(function_declarations=toolbox.declarations)] if toolbox else None,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True))
    for _ in range(4):  # model -> tool call -> result -> model ...
        r = _ask(contents, config)
        calls = r.function_calls
        if not calls: return r.text
        contents.append(r.candidates[0].content)
        contents.append(types.Content(role="user", parts=[
            types.Part(function_response=types.FunctionResponse(
                id=c.id, name=c.name, response={"result": toolbox.run(c.name, dict(c.args or {}))})) for c in calls]))
    return r.text or "Sorry, I couldn't finish that. Please try again."
