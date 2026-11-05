
# AI Customer Support Agent for E-Commerce

An intelligent, multilingual customer support system built for an electronic store, powered by **Retrieval-Augmented Generation (RAG), Google Gemini, Flask, and ChromaDB.**

The system enables customers to interact with an AI support agent that answers product-related questions, retrieves information from the store's knowledge base, assists with order management, and responds in multiple languages.

Unlike a basic chatbot that relies entirely on an LLM's internal knowledge, this system uses RAG to ground responses in relevant store information and live product data.

---

## 1. Project Overview

The AI Customer Support Agent is designed to automate customer interactions in an electronic store while maintaining access to accurate and relevant business information.

Customers can:
- Ask questions about products, pricing, availability, and store policies.
- Receive context-aware answers based on the store's knowledge base.
- Interact with the assistant in **English, Kiswahili, Dholuo, and Gĩkũyũ**.
- Create order drafts through natural language conversations.
- Cancel pending order drafts.
- Retrieve information about their existing orders.

The system also incorporates a confirmation-based ordering workflow, ensuring that the AI cannot independently finalize customer orders.

## 2. System Preview

### Customer Interface

<!-- Insert homepage screenshot here -->
<img width="1920" height="952" alt="homepageA" src="https://github.com/user-attachments/assets/3cccda5d-f475-4fe8-9801-10d83edf4b68" />




*Figure 1: Electronic store customer interface.*

### AI Customer Support Chatbot

<!-- Insert chatbot screenshot here -->
<img width="1920" height="948" alt="chatbot" src="https://github.com/user-attachments/assets/89f4c101-accd-4bad-a655-fdc92f7b580c" />






*Figure 2: AI-powered customer support interface.*

### Multilingual Conversation

<!-- Insert multilingual chatbot screenshot here -->

<img width="1920" height="946" alt="multilingual_system" src="https://github.com/user-attachments/assets/1107ea99-e68e-41b5-971c-23f00e22d0b5" />


### Order Management Through AI

<!-- Insert order confirmation screenshot here -->


<img width="1920" height="952" alt="conf" src="https://github.com/user-attachments/assets/b918deb6-acc8-4535-9d97-042c419065ab" />



*Figure 4: AI-assisted order drafting and customer confirmation.*

> Replace the image paths above with your actual screenshots. Store them inside `docs/images/` in your repository.

---

## 3. Key Features

### Retrieval-Augmented Generation (RAG)

The system implements a RAG pipeline to reduce unsupported responses and provide answers grounded in actual store information.

- Google Gemini embeddings for semantic representation.
- ChromaDB for persistent vector storage.
- Document chunking and embedding.
- Semantic similarity search.
- Retrieval of relevant knowledge-base information.
- Live product information retrieved from the database.
- Context injection into Gemini before response generation.

### Multilingual AI Support

The chatbot supports four languages:

| Language | Support |
|---|---|
| English | Native conversation |
| Kiswahili | Native conversation |
| Dholuo | Translation-assisted retrieval and response |
| Gĩkũyũ | Translation-assisted retrieval and response |

For Dholuo and Gĩkũyũ, incoming questions are first rendered in English to improve retrieval accuracy. Gemini then generates the response in the language selected by the customer.

The translation layer is modular, making it possible to integrate a dedicated translation model in the future.

### AI-Powered Order Management

The assistant uses Gemini tool calling to interact with order-related functionality.

Available tools:

- `draft_order` – Creates a pending order draft.
- `cancel_order_draft` – Cancels an existing order draft.
- `my_orders` – Retrieves the customer's orders.

**Human-in-the-loop confirmation:**

The AI is not allowed to independently finalize an order.

Instead, the workflow is:

1. Customer requests an order through chat.
2. Gemini invokes the `draft_order` tool.
3. The backend creates an order draft.
4. The customer reviews the order.
5. The customer explicitly clicks **Confirm**.
6. The frontend sends a request to `POST /api/chat/confirm-order`.

This ensures that important transactional actions remain under customer control.

---

## 4. Technical Architecture

### Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Backend | Python / Flask | REST API and application logic |
| Database | SQLAlchemy | Product and order management |
| LLM | Google Gemini | Response generation and tool calling |
| Embeddings | Gemini Embedding API | Semantic document representation |
| Vector Database | ChromaDB | Persistent vector storage |
| Frontend | HTML, CSS, JavaScript | Customer-facing interface |
| Testing | Pytest | Backend testing |
| Environment | Python dotenv | Environment configuration |

### RAG Architecture

The core RAG pipeline follows this process:

```text
       CUSTOMER QUESTION
               |
               v
       LANGUAGE PROCESSING
               |
               v
       GEMINI EMBEDDING
               |
               v
       CHROMADB SIMILARITY SEARCH
               |
               +----------------------+
               |                      |
               v                      v
       KNOWLEDGE BASE           LIVE PRODUCT DATA
               |                      |
               +----------+-----------+
                          |
                          v
                 CONTEXT ASSEMBLY
                          |
                          v
                  GEMINI LLM
                          |
                          v
                GENERATED RESPONSE
                          |
                          v
                 CUSTOMER CHAT UI
```

### How Retrieval Works

1. The customer submits a question.
2. The question is processed according to the selected language.
3. Gemini generates an embedding representing the question.
4. ChromaDB performs semantic similarity search against stored knowledge-base chunks.
5. Relevant live product information is retrieved from the application database.
6. The top 5 retrieved knowledge-base chunks, together with relevant product information, are supplied to Gemini as context.
7. Gemini generates a response grounded in the retrieved information.
8. The response is returned to the frontend.

The vector database is persistent and stored locally in:

`backend/chroma_db/`

This avoids rebuilding the vector index every time the application starts.

---

## 5. Project Structure

```text
AI-Customer-Support-Agent/
│
├── backend/
│   ├── app/
│   │   ├── rag/
│   │   │   ├── language.py
│   │   │   └── ...
│   │   │
│   │   ├── routes/
│   │   ├── models/
│   │   ├── ...
│   │
│   ├── knowledge_base/
│   │
│   ├── chroma_db/
│   │
│   ├── tests/
│   │
│   ├── .env
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── css/
│   ├── js/
│   │   └── chatbot.js
│   ├── images/
│   └── ...
│
├── docs/
│   └── images/
│
└── README.md
```

*Note: Adjust the folder tree to match your final repository structure.*

---

## 6. Getting Started

### Prerequisites

- Python 3.10+
- pip
- Google Gemini API key

### Installation

**Step 1: Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

cd YOUR_REPOSITORY
```

**Step 2: Install backend dependencies**

```bash
cd backend

pip install -r requirements.txt
```

**Step 3: Configure environment variables**

Create a `.env` file inside the `backend/` directory.

```env
GEMINI_API_KEY=your_gemini_api_key
```

Get your API key from:

https://aistudio.google.com/apikey

**Step 4: Start the application**

```bash
python run.py
```

**Step 5: Open the application**

Navigate to:

```text
http://localhost:5000
```

Flask serves the frontend directly, so there is no need to start a separate frontend development server.

### Reindexing the Knowledge Base

Whenever you modify the knowledge-base documents or product information, trigger the reindex endpoint:

```http
POST /api/chat/reindex
```

This updates the vector index with the latest information.

---

## 7. Testing

The backend includes automated tests using Pytest.

Gemini API calls are mocked during testing to avoid unnecessary external API requests.

Run the test suite:

```bash
cd backend

pytest
```

---

## 8. Engineering Considerations

Some important architectural decisions behind this project include:

**Persistent vector storage**

ChromaDB persists embeddings locally, allowing the system to reuse indexed knowledge without rebuilding the entire vector database on every application startup.

**Live product retrieval**

Product information is retrieved from the application database rather than relying exclusively on potentially outdated information stored in document embeddings.

**Language-aware retrieval**

Dholuo and Gĩkũyũ questions are translated into English before retrieval, creating a modular approach to multilingual semantic search.

**Controlled AI actions**

Gemini tool calling is used to connect the LLM to backend functionality. However, transactional operations such as order confirmation require explicit customer approval.

**Testability**

Gemini interactions are mocked during automated tests, allowing backend functionality to be tested independently of external model availability.

---

## 9. Future Improvements

Potential areas for further development:

- Voice-based customer support using speech-to-text and text-to-speech.
- Improved Dholuo and Gĩkũyũ translation using dedicated language models.
- RAG evaluation using retrieval precision, recall, and answer faithfulness.
- Conversation history and long-term customer context.
- M-Pesa payment integration.
- Admin dashboard for managing knowledge-base documents and products.
- Improved observability, logging, and retrieval debugging.
- Deployment using Docker and cloud infrastructure.

---

## 10. Why This Project?

This project explores the practical engineering challenges involved in building an AI-powered application beyond simply connecting an LLM to a chat interface.

It demonstrates the integration of:

- Large Language Models (LLMs).
- Retrieval-Augmented Generation (RAG).
- Vector databases and semantic search.
- Embedding generation.
- LLM tool calling and backend integration.
- Multilingual AI systems.
- REST API development.
- Human-in-the-loop transaction workflows.
- Automated backend testing.

The goal is to demonstrate how AI systems can be integrated into real-world business applications while maintaining structured data retrieval, controlled actions, and reliable backend workflows.

---

## Author

**Your Name**

Software Developer | AI & Backend Engineering

[GitHub](https://github.com/YOUR_USERNAME) · [LinkedIn](https://linkedin.com/in/YOUR_PROFILE)

---

*Built with Python, Flask, Google Gemini, ChromaDB, and JavaScript.*
