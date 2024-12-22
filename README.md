# yeshiva  Bot 🤖

Welcome to the **yeshiva  Bot**, your friendly guide to all things yeshiva! This chatbot is designed to assist yeshiva students, faculty, and prospective students with any questions they may have about yeshiva. The  Bot leverages a combination of RAG (Retrieval-Augmented Generation) and fine-tuned LLM (Large Language Model) technology to provide accurate and up-to-date information directly from yeshiva's website.

## How It Works 🛠️

The yeshiva  Bot is powered by an LLM trained on data scraped from various sections of the yeshiva website, creating a knowledge base that enables the bot to respond intelligently to queries. The process of data gathering and embedding is outlined below.

### 1. Data Scraping with BeautifulSoup 🥣

To build the bot's knowledge base, we used BeautifulSoup to scrape content from the yeshiva website. This content serves as the foundation of the bot’s responses, allowing it to provide answers that are accurate and relevant.

The script collects text from specified URLs, focusing on paragraph elements that contain the core information about yeshiva. This collected text is then processed for further steps.

### 2. Creating Vector Embeddings with FAISS 🧬

Once the text is scraped, we use a Sentence Transformer model (`all-MiniLM-L6-v2`) to generate embeddings for each piece of content. These embeddings are vector representations of the textual data, allowing the bot to perform efficient similarity searches.

To enable quick and scalable querying, we store the embeddings in a FAISS (Facebook AI Similarity Search) vector database. FAISS allows the bot to find the most relevant information for user queries by searching through the embedding vectors, resulting in accurate and contextually appropriate responses.

### 3. Integrating the First LLM with NVIDIA's Llama Model 🦙

To create an intelligent RAG-based chatbot, we leveraged **`nvidia/llama-3.1-nemotron-70b-instruct`**, a powerful language model from NVIDIA's suite. This model allowed us to process and understand complex queries by retrieving relevant information from our FAISS-powered vector database. The combination of Llama’s robust language understanding and our vector embeddings enabled the bot to deliver precise and contextually accurate responses.

### 4. Fine-Tuning with BERT for Custom Data 🧠

In addition to the initial LLM, we implemented **BERT** from the `transformers` library and fine-tuned it on custom yeshiva data. To generate this fine-tuning dataset, we used **`nvidia/nemotron-4-340b`**, another advanced language model from NVIDIA, which produced synthetic data closely aligned with the types of queries and responses relevant to yeshiva.

The integration of BERT, fine-tuned with this custom dataset, added a layer of specificity, enabling the  Bot to better address nuanced questions and provide more personalized assistance to yeshiva users. This approach, combining both a large-scale LLM and a fine-tuned BERT model, helped us achieve a balanced chatbot capable of accurate retrieval and context-aware responses.


# yeshiva  Bot Architecture Flow

```plaintext
                         # yeshiva  Bot Architecture Flow

The yeshiva  Bot architecture is designed to provide quick, accurate, and contextually relevant responses by combining predefined responses, a large language model (LLM), and a fine-tuned fallback model. Here’s a detailed step-by-step explanation of the flow:

---

## Architecture Flow Diagram

```plaintext
                            +----------------+
                            |   User Query   |
                            +----------------+
                                   |
                                   v
                      +------------------------+
                      | Check for Stop Words   |
                      +------------------------+
                                   |
                                   v
                      +---------------------------------+
                      | Check Predefined Q&A from FAQs  |
                      +---------------------------------+
                                   |
                                   v
                     +--------------------------+
                     |  Check Conversation Log  |
                     +--------------------------+
                                   |
                        +----------+-----------+
                        |                      |
                        v                      v
               +------------------+    +-------------------------+
               | Predefined       |    |  NVIDIA LLM Processes   |
               | Response         |    |      Query              |
               +------------------+    +-------------------------+
                                              |
                                              v
                                   +-----------------------+
                                   |   Search Vector DB    |
                                   +-----------------------+
                                              |
                                       +------+------+
                                       |             |
                                       v             v
                            +------------------+  +-----------------+
                            |  Context Found   |  |  No Context    |
                            |                  |  |  Scrape Web    |
                            +------------------+  |  for Solution  |
                                       |         +-----------------+
                                       |
                              +--------+--------+
                              | Generate Output |
                              +--------+--------+
                                       |
                                       v
                             +-------------------+
                             | Store in          |
                             | Conversation Log  |
                             +-------------------+
                                       |
                                       v
                              +----------------------+
                              | Timeout Handling     |
                              | Fine-tuned BERT      |
                              | Generates Response   |
                              +----------------------+
                                       |
                                       v
                             +-------------------+
                             | Store in          |
                             | Conversation Log  |
                             +-------------------+


```

# yeshiva  Bot Architecture Flow

The yeshiva  Bot architecture is designed to provide quick, accurate, and contextually relevant responses by combining predefined responses, a large language model (LLM), and a fine-tuned fallback model. Here’s a detailed step-by-step explanation of the flow:

---

# Architecture Flow Explained

The yeshiva  Bot follows a structured flow to ensure fast, accurate, and contextually relevant responses. Here’s a breakdown of each step in the architecture:

1. **User Query** 💬  
   - The process begins when a user submits a query to the chatbot.

2. **Check for Stop Words** 🔍  
   - The bot initially checks if the query contains any stop words or irrelevant words that might indicate a simple or unimportant query. This helps to filter out unnecessary queries that do not require complex processing.

3. **Check Predefined Q&A** 📖  
   - Before proceeding further, the bot checks a set of hardcoded, predefined questions and answers. This Q&A set handles frequently asked questions and common queries, providing an immediate response when there’s a match.
   - **Predefined Response**: If a match is found in the predefined Q&A set, the bot provides the corresponding answer without further processing.

4. **Check Conversation Log** 📜  
   - If the query isn’t found in the predefined Q&A set, the bot searches its conversation log file to check if the query has been previously asked and answered. This log helps in quickly responding to repeated queries.
   - **Stored Response**: If a match is found in the conversation log, the bot retrieves and provides the saved response.
   - **NVIDIA LLM Processes Query**: If the query is not found in the log, the bot proceeds to the next stage, where the NVIDIA LLM handles the query.

5. **NVIDIA LLM and Vector Database Search** 🧠  
   - For complex queries, the **NVIDIA Large Language Model (LLM)** is activated. The LLM processes the query and searches a **FAISS-powered Vector Database** for relevant information:
     - **Context Found**: If relevant context is found in the vector database, the bot generates a response based on this context.
     - **No Context Found**: If no context is available, the LLM initiates a **web scraping** process to gather information that could help answer the query.
   - After generating the response (whether from context in the vector database or web scraping), the bot **stores the output in the conversation log** for future reference.

6. **Timeout Handling and Fine-Tuned BERT** ⏱️  
   - If the NVIDIA LLM takes too long to generate a response, the bot activates a **fine-tuned BERT model** as a fallback. This BERT model, fine-tuned on yeshiva-specific data, quickly generates a response to ensure the user isn’t kept waiting.
   - The response from the BERT model is also **stored in the conversation log**, allowing for quick retrieval in future queries.

7. **Store in Conversation Log** 🗂️  
   - Regardless of the response source (predefined Q&A, NVIDIA LLM, web scraping, or BERT), the final output is stored in the conversation log. This log is continuously updated, allowing the bot to improve its efficiency and response accuracy over time.

---

## Summary

This architecture flow allows the yeshiva  Bot to:

- **Quickly handle common queries** with predefined responses.
- **Leverage the power of NVIDIA LLM** for complex, context-dependent questions.
- **Fallback on fine-tuned BERT** for timely responses when needed.
- **Continuously update** its conversation log for improved efficiency and accuracy.

This structured approach ensures a fast, accurate, and user-friendly experience tailored to the needs of yeshiva students, faculty, and prospective students.


=

