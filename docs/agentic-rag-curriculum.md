# Agentic RAG & AI Agent Systems — Full Curriculum
*Built from 2026 job market analysis: Kyndryl, Hitachi, Microsoft, Slalom, Motion Recruitment, Apex Systems*

---

## How to Use This

1. Pick one topic below (start from top, they build on each other)
2. Copy the prompt into Claude.ai web (claude.ai)
3. Study the output (~45–60 min), run the code examples
4. Come back and say: **"Quiz me on [topic] and simulate a technical interview"**
5. Check off the topic when done
6. Build the Flagship Project at the end using everything learned

**Target: one topic per day, ~2 hours total per topic.**
**Stack: Python + AWS (primary) + Google Cloud / Azure as needed (free tier)**

---

## TRACK 1 — LLM API FOUNDATIONS

### 1.1 — Anthropic Claude API
- [ ] Studied

**Prompt:**
```
I am a Senior Data/AI Engineer with 20 years of Python experience. I already use the Claude API in production for a job search automation system. I want to go deeper.

Give me a focused 2-hour study session on the Anthropic Claude API covering:
1. API authentication, client setup, model selection (claude-sonnet-4-6, opus, haiku — when to use each)
2. Messages API structure: system, user, assistant roles, multi-turn conversations
3. Streaming responses — how to implement and when it matters
4. Tool use / function calling: defining tools, handling tool_use blocks, tool_result, multi-turn tool loops
5. Structured output patterns: JSON mode, Pydantic validation, schema enforcement
6. Token counting, context window management, caching (prompt caching for cost reduction)
7. Error handling: rate limits, retries, exponential backoff
8. Cost optimization: choosing models by task, batching, caching
9. 8 real interview questions about LLM API integration with strong answers

Format as a structured tutorial with working Python code examples throughout.
My background: Python expert, AWS, currently using Claude for agents and RAG.
End with a 5-minute cheat sheet.
```

---

### 1.2 — OpenAI API (GPT-4o, o3)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer expert in the Anthropic Claude API. I now need to learn the OpenAI API because many enterprise jobs require it, and frameworks like LangChain abstract over it.

Give me a focused 2-hour study session on the OpenAI Python API covering:
1. Client setup, authentication, model selection (gpt-4o, gpt-4o-mini, o3 — when to use each)
2. Chat completions API: messages structure, system prompts, temperature, max_tokens
3. Function calling / tool use: defining functions, parallel tool calls, tool_choice
4. Structured outputs: response_format with JSON schema, Pydantic integration
5. Streaming with the OpenAI SDK
6. Embeddings API: text-embedding-3-small vs large, dimensions, use cases
7. Assistants API vs raw completions — when to use each
8. Differences between OpenAI and Anthropic APIs — how to swap between them
9. Cost management: tiktoken, context window costs, batching

Python code examples throughout. End with a side-by-side comparison cheat sheet vs Anthropic.
```

---

### 1.3 — AWS Bedrock (Deep Dive)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AWS Engineer. I have used AWS Bedrock at a basic level at Citi (Fortune 500 financial services). I need to go deep for senior AI engineering interviews.

Give me a focused 2-hour study session on AWS Bedrock covering:
1. Bedrock architecture: what it is, which models are available (Claude, Titan, Llama, Mistral, Cohere)
2. InvokeModel vs Converse API — differences, when to use each
3. Bedrock Agents: creating agents, action groups, knowledge bases, session state
4. Bedrock Knowledge Bases: ingestion pipeline, S3 → chunking → embeddings → OpenSearch Serverless
5. Bedrock Guardrails: content filtering, topic denial, PII redaction, grounding checks
6. Bedrock Flows: visual agent workflow builder — how it compares to LangGraph
7. IAM permissions for Bedrock: least-privilege patterns
8. Cost management: on-demand vs provisioned throughput
9. boto3 Python integration patterns for all of the above
10. 8 interview questions about production Bedrock deployments with strong answers

Code examples in Python/boto3 throughout. My background: Python expert, AWS certified-level knowledge, financial services context.
```

---

### 1.4 — Azure OpenAI Service
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AWS Engineer learning Azure for AI engineering roles that require Azure. I have no Azure background.

Give me a focused 2-hour study session on Azure OpenAI Service covering:
1. What Azure OpenAI is vs OpenAI API directly — why enterprises choose Azure (compliance, VNet, SLA)
2. Setting up: creating a resource, deploying a model, getting endpoints and keys
3. Python SDK: openai library with Azure config, AzureOpenAI client
4. Available models on Azure: GPT-4o, GPT-4 Turbo, text-embedding-ada-002, DALL-E
5. Azure AI Studio: playground, fine-tuning UI, evaluation tools
6. Private endpoints and VNet integration (why regulated industries need this)
7. Content filtering and responsible AI controls
8. Azure AI Search integration for RAG (this is Azure's vector DB)
9. Cost and quota management
10. How this compares to AWS Bedrock — switching between them in LangChain

Python code examples throughout. Bridge every concept to AWS equivalents.
Sign-up uses free credits — no billing required for this session.
```

---

### 1.5 — Google Gemini API & Vertex AI
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AWS Engineer learning Google Cloud for AI engineering roles. I have no GCP background.

Give me a focused 2-hour study session on Google Gemini and Vertex AI covering:
1. Google AI ecosystem: Gemini API (direct) vs Vertex AI (enterprise) — when to use which
2. Setting up Google AI Studio and getting a free Gemini API key
3. Python SDK (google-generativeai): chat, streaming, function calling, embeddings
4. Gemini model family: Gemini 2.0 Flash, Pro, Ultra — capability and cost differences
5. Multimodal inputs: sending images, PDFs, audio to Gemini
6. Vertex AI basics: what it adds over direct API (managed endpoints, MLOps, Pipelines)
7. Vertex AI Search (enterprise RAG service) — equivalent to Bedrock Knowledge Bases
8. LangChain integration with Gemini: ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
9. Cost: Gemini API has a generous free tier — how to use it for learning
10. Comparison table: AWS Bedrock vs Azure OpenAI vs Google Vertex AI

Python code throughout. Start from free tier sign-up. No prior GCP knowledge assumed.
```

---

## TRACK 2 — EMBEDDINGS & VECTOR SEARCH

### 2.1 — Embeddings: Concepts & Models
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. I use embeddings in RAG pipelines but want to go deep on the theory and model selection.

Give me a focused 2-hour study session on embeddings for AI systems covering:
1. What embeddings are: vector space, semantic similarity, cosine similarity explained simply
2. Embedding model families: OpenAI text-embedding-3, Cohere embed-v3, BGE, E5, sentence-transformers
3. Dimensions: 384 vs 768 vs 1536 vs 3072 — trade-offs between size, quality, speed, cost
4. Local vs API embeddings: when to use HuggingFace sentence-transformers locally vs API
5. Matryoshka embeddings: what they are, why they matter for flexible retrieval
6. Evaluating embedding quality: MTEB benchmark, semantic textual similarity tasks
7. Embedding for different content: short queries vs long documents — asymmetric embeddings
8. Multi-lingual embeddings: when you need them
9. Python code: how to generate, store, and compare embeddings end-to-end
10. Choosing the right embedding model for a given use case — decision framework

Working Python code with sentence-transformers and OpenAI. Cost vs quality comparison table.
```

---

### 2.2 — Text Chunking Strategies
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer building RAG pipelines. I want to master chunking strategies because this is where most RAG systems fail.

Give me a focused 2-hour study session on text chunking for RAG covering:
1. Why chunking matters: the chunk size vs retrieval quality trade-off
2. Fixed-size chunking: character splitting, token splitting, overlap — when to use
3. Recursive character splitting (LangChain RecursiveCharacterTextSplitter) — how it works
4. Semantic chunking: splitting on meaning boundaries, not character count
5. Document-aware chunking: Markdown headers, HTML tags, code blocks, tables
6. Sentence-level and paragraph-level chunking
7. Hierarchical chunking: parent-child document retrieval
8. LlamaIndex node parsers: SentenceSplitter, SemanticSplitterNodeParser
9. How to evaluate chunk quality: retrieval hit rate, answer faithfulness
10. Practical rules of thumb: chunk sizes for different document types (PDFs, code, emails, contracts)

Python code examples using LangChain and LlamaIndex text splitters.
Show how different chunking strategies affect retrieval quality with the same test documents.
```

---

### 2.3 — FAISS (Facebook AI Similarity Search)
- [ ] Studied

**Prompt:**
```
I am a Senior Python Engineer. I have used FAISS for vector similarity search. I want to go deep for technical interviews.

Give me a focused 2-hour study session on FAISS covering:
1. What FAISS is: approximate nearest neighbor (ANN) search, why it beats brute force
2. Index types: Flat (exact), IVF (inverted file), HNSW, PQ (product quantization) — when to use each
3. IndexFlatL2 vs IndexFlatIP (L2 distance vs inner product / cosine)
4. IVFFlat: nlist, nprobe — how to tune for speed vs recall trade-off
5. HNSW: how the graph index works, M parameter, ef_construction vs ef_search
6. Saving and loading FAISS indexes to disk
7. FAISS + metadata: why FAISS doesn't store metadata and how to handle it (parallel arrays, SQLite)
8. GPU FAISS: when and how to use it
9. LangChain FAISS integration: from_documents, similarity_search, as_retriever
10. FAISS vs managed vector databases: when to use FAISS (local, no cost) vs Pinecone/pgvector

Python code examples throughout. Real benchmarks showing index type trade-offs.
```

---

### 2.4 — ChromaDB
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer familiar with FAISS. I want to learn ChromaDB because it appears in many LangChain and LlamaIndex tutorials and is common in interviews.

Give me a focused 2-hour study session on ChromaDB covering:
1. What ChromaDB is: embedded vs client-server mode, SQLite + HNSW under the hood
2. Collections: creating, adding documents, metadata, IDs
3. Querying: query_texts, query_embeddings, where filters on metadata, n_results
4. Persistent storage: ChromaDB on disk vs in-memory
5. ChromaDB server mode: running as a standalone service, connecting from Python
6. Custom embedding functions: using your own embeddings vs built-in
7. LangChain integration: Chroma as a vectorstore, from_documents, as_retriever
8. LlamaIndex integration: ChromaVectorStore
9. When to use ChromaDB vs FAISS vs Pinecone — decision matrix
10. Production considerations: limitations, scaling, alternatives when you outgrow it

Python code examples for every concept. Show a complete end-to-end RAG pipeline with Chroma.
```

---

### 2.5 — Pinecone
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. Pinecone appears in nearly every senior AI job description. I have not used it but need to learn it for interviews.

Give me a focused 2-hour study session on Pinecone covering:
1. What Pinecone is: managed vector database, serverless vs pod-based
2. Setting up a free Pinecone account and creating an index (serverless, free tier)
3. Index configuration: dimensions, metric (cosine, dotproduct, euclidean), namespaces
4. Upsert: inserting vectors with IDs and metadata
5. Query: top-k search, metadata filtering, namespace isolation
6. Sparse-dense hybrid search: combining BM25 sparse vectors with dense embeddings
7. Pinecone Assistant (managed RAG product) — what it is, when to use vs build your own
8. LangChain integration: PineconeVectorStore, from_documents, similarity_search_with_score
9. Production patterns: batch upsert, index namespacing for multi-tenant RAG
10. Cost model: serverless pricing, how to estimate costs for enterprise scale
11. Pinecone vs pgvector vs ChromaDB vs Weaviate — honest comparison

Working Python code with the Pinecone SDK. Uses free tier — no billing needed.
```

---

### 2.6 — pgvector (PostgreSQL Vector Extension)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/Data Engineer with strong PostgreSQL experience. pgvector appears in Kyndryl, Hitachi, and other job postings. I need to learn it for interviews.

Give me a focused 2-hour study session on pgvector covering:
1. What pgvector is: PostgreSQL extension adding vector column type and ANN operators
2. Installation: enabling the extension in PostgreSQL (local Docker, AWS RDS, Supabase)
3. Creating tables with vector columns: CREATE TABLE with vector(1536) type
4. Inserting vectors: Python psycopg2 / asyncpg, SQLAlchemy ORM patterns
5. Querying: L2 distance (<->), cosine distance (<=>), inner product (<#>) operators
6. Indexing: IVFFlat vs HNSW indexes for pgvector — CREATE INDEX patterns
7. Hybrid search with pgvector: combining full-text search (tsvector/tsquery) with vector similarity
8. LangChain PGVector integration: connection strings, collection names, from_documents
9. LlamaIndex PGVectorStore
10. pgvector in AWS RDS / Aurora: how to enable, limits
11. When to choose pgvector over Pinecone: the "keep it in Postgres" argument

Python code examples using psycopg2, SQLAlchemy, and LangChain PGVector.
Docker compose setup for local PostgreSQL + pgvector development.
```

---

### 2.7 — Weaviate
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. I need to learn Weaviate as it appears in enterprise AI job descriptions as an alternative vector database.

Give me a focused 2-hour study session on Weaviate covering:
1. What Weaviate is: open-source vector database with built-in ML models
2. Weaviate Cloud (managed) vs local Docker — free tier setup
3. Schema / Collections: defining data classes, properties, vectorizer configuration
4. Importing data: batch import, automatic vectorization vs bring-your-own vectors
5. Querying: nearText, nearVector, hybrid, BM25 — how each works
6. Filters: where clause filtering on metadata during vector search
7. Weaviate modules: text2vec-openai, text2vec-cohere, generative-openai (RAG built-in)
8. GraphQL API: how Weaviate exposes queries (understand the pattern, not master it)
9. LangChain Weaviate integration
10. Weaviate vs Pinecone vs pgvector vs ChromaDB — honest enterprise comparison

Python code examples using the Weaviate Python client v4.
Uses Weaviate Cloud free tier. End with a decision framework for which vector DB to pick.
```

---

### 2.8 — Hybrid Search (BM25 + Vector)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer building RAG systems. Hybrid search is mentioned in Hitachi, Kyndryl, and other senior AI job descriptions. I need to understand it deeply.

Give me a focused 2-hour study session on hybrid search for RAG covering:
1. Why pure vector search fails: keyword mismatch, exact term requirements, named entities
2. BM25 explained: TF-IDF evolution, why it works for keyword search
3. Sparse vectors: how BM25 scores become sparse vectors for combination with dense vectors
4. Reciprocal Rank Fusion (RRF): how to merge ranked lists from BM25 and vector search
5. Weighted hybrid scoring: alpha parameter to tune keyword vs semantic weight
6. Implementation in Pinecone: sparse-dense index, BM25Encoder
7. Implementation in Weaviate: hybrid query, alpha parameter
8. Implementation in Elasticsearch / OpenSearch: KNN + BM25 combo
9. Implementation in LangChain: EnsembleRetriever combining BM25Retriever + vector retriever
10. When hybrid outperforms pure vector: benchmarks, real examples
11. Evaluation: how to measure if hybrid is actually better for your data

Python code for LangChain EnsembleRetriever and Pinecone hybrid.
Include a test harness to compare pure vector vs hybrid on the same query set.
```

---

### 2.9 — Reranking
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. Reranking is mentioned in Hitachi's job description and is a key step in production RAG pipelines. I need to understand it deeply.

Give me a focused 2-hour study session on reranking for RAG covering:
1. Why first-stage retrieval is imprecise: ANN trade-offs, why top-k isn't always best-k
2. What reranking is: second-stage scoring with a cross-encoder model
3. Bi-encoders (retrieval) vs cross-encoders (reranking) — fundamental difference
4. Cohere Rerank API: how to use it, models available (rerank-english-v3.0), cost
5. Local reranking with sentence-transformers: cross-encoder/ms-marco-MiniLM-L-6-v2
6. FlashRank: lightweight local reranker, good for AWS Lambda
7. LangChain CohereRerank integration: ContextualCompressionRetriever pattern
8. LlamaIndex reranking: SentenceTransformerRerank, CohereRerank
9. ColBERT: late interaction reranking, what makes it different
10. When reranking matters most vs when it's overkill
11. Performance impact: latency cost of reranking, how to minimize it

Python code examples for Cohere Rerank API and local cross-encoder reranking.
Build a complete retrieval pipeline: embed → ANN search → rerank → generate.
```

---

## TRACK 3 — RAG PIPELINE ARCHITECTURE

### 3.1 — Naive RAG (Baseline Pattern)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. I want to master RAG from first principles, starting with the naive baseline before advanced patterns.

Give me a focused 2-hour study session on Naive RAG (baseline pattern) covering:
1. The RAG pipeline end-to-end: load → chunk → embed → store → retrieve → augment → generate
2. Document loaders: PDF (PyPDF2, pdfplumber), TXT, DOCX, HTML, JSON
3. The retrieval-augmented prompt: how to construct the context window correctly
4. Top-k retrieval: how many chunks to retrieve, how context length affects quality
5. Answer generation: system prompt design for grounded, cited responses
6. Why naive RAG fails: lost-in-the-middle problem, stale retrieval, context overflow
7. Building naive RAG from scratch in Python (no framework): step by step
8. Building naive RAG with LangChain: RetrievalQA vs LCEL chain
9. Building naive RAG with LlamaIndex: VectorStoreIndex, QueryEngine
10. Evaluation baseline: faithfulness, answer relevancy, context precision — using RAGAS

Complete Python implementation of naive RAG end-to-end.
Use a real dataset (e.g., Wikipedia articles or financial reports) as test documents.
```

---

### 3.2 — Advanced RAG Patterns
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer who knows naive RAG. I need to learn advanced RAG patterns for senior AI engineer interviews (Hitachi, Kyndryl, Microsoft-level roles).

Give me a focused 2-hour study session on Advanced RAG patterns covering:
1. HyDE (Hypothetical Document Embeddings): generate a fake answer, embed it, retrieve with it
2. Multi-query retrieval: generate N paraphrased queries, retrieve for each, deduplicate
3. RAG fusion: multi-query + RRF merging of results
4. Parent-child retrieval: store small chunks, retrieve full parent document on match
5. Step-back prompting: abstract the question before retrieval
6. Self-RAG: LLM decides whether to retrieve, evaluates its own answer
7. CRAG (Corrective RAG): retrieval quality grading, web search fallback
8. Contextual compression: extract only relevant sentences from retrieved chunks
9. Sentence window retrieval: retrieve surrounding context around matched sentence
10. Agentic RAG: let an agent decide retrieval strategy dynamically

Python code for each pattern using LangChain and/or LlamaIndex.
Benchmark each against naive RAG on the same questions.
End with a decision framework: which pattern to use when.
```

---

### 3.3 — RAGAS (RAG Evaluation Framework)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer building RAG systems. Evaluation frameworks like RAGAS are mentioned in senior job descriptions (Hitachi explicitly). I need to understand RAG evaluation deeply.

Give me a focused 2-hour study session on RAG evaluation with RAGAS covering:
1. Why RAG evaluation is hard: no ground truth, LLM-as-judge, hallucination detection
2. RAGAS metrics explained:
   - Faithfulness: is the answer grounded in the retrieved context?
   - Answer Relevancy: does the answer address the question?
   - Context Precision: are the retrieved chunks relevant?
   - Context Recall: did we retrieve all necessary information?
3. Setting up RAGAS: installation, dataset format (question, answer, contexts, ground_truth)
4. Running RAGAS evaluation: evaluate() function, interpreting scores
5. RAGAS with LangChain pipelines
6. RAGAS with LlamaIndex pipelines
7. Building a test dataset: how to generate question-answer pairs from documents
8. LLM-as-judge patterns beyond RAGAS: G-Eval, custom rubrics
9. Online vs offline evaluation: production monitoring vs test suite
10. Statistical testing: are two RAG pipelines actually different?

Python code for a complete RAGAS evaluation pipeline.
Include a comparison of naive RAG vs advanced RAG on the same test dataset using RAGAS scores.
```

---

### 3.4 — Document Parsing & Ingestion (Unstructured, LlamaParse)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. Document ingestion quality is often the hidden failure point in RAG systems. I need to master production document parsing.

Give me a focused 2-hour study session on document parsing for RAG covering:
1. Why document parsing matters: garbage in → garbage retrieval → garbage answers
2. PDF challenges: text vs scanned, multi-column, tables, footnotes, headers/footers
3. PyPDF2 and pdfplumber: basic extraction, limitations
4. Unstructured.io library: how it works, element types (Title, NarrativeText, Table)
5. LlamaParse (LlamaIndex cloud parser): superior PDF/DOCX parsing, table extraction
6. Docling (IBM): open-source document converter, good for enterprise docs
7. Table extraction: converting tables to markdown for LLM consumption
8. Image extraction and description: using vision models to describe embedded images
9. Web scraping for RAG: BeautifulSoup, Playwright, Firecrawl API
10. Email ingestion patterns
11. Code file ingestion: treating code as a special document type
12. Metadata extraction: file name, page number, section, date — building the metadata schema

Python code examples for each approach.
Build a document ingestion pipeline that handles PDF, DOCX, HTML, and plain text.
```

---

## TRACK 4 — AGENT FRAMEWORKS

### 4.1 — LangChain (Deep Dive)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer with some LangChain experience (Text-to-SQL agents). I need to go deep for senior interviews.

Give me a focused 2-hour study session on LangChain covering:
1. LangChain architecture: chains, runnables, LCEL (LangChain Expression Language)
2. LCEL syntax: pipe operator, RunnablePassthrough, RunnableLambda, RunnableParallel
3. Chat models: ChatOpenAI, ChatAnthropic, ChatBedrockConverse — unified interface
4. Prompt templates: ChatPromptTemplate, MessagesPlaceholder, few-shot templates
5. Memory: ConversationBufferMemory, ConversationSummaryMemory, RunnableWithMessageHistory
6. Document loaders and text splitters in LangChain
7. Vector stores as retrievers: as_retriever(), search_type, search_kwargs
8. Agents in LangChain: create_react_agent, AgentExecutor, custom tools with @tool
9. LangChain callbacks: how to log, trace, and debug chains
10. LangSmith integration: tracing, evaluation, prompt management
11. LangChain v0.3 changes: what changed from v0.1/v0.2, migration patterns

Python code for every concept.
Build a complete conversational RAG agent with memory, tools, and LangSmith tracing.
```

---

### 4.2 — LangGraph (Stateful Multi-Agent)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer with LangChain experience. LangGraph is now the dominant framework for production agentic systems and appears in multiple job descriptions. I need to learn it.

Give me a focused 2-hour study session on LangGraph covering:
1. Why LangGraph exists: LangChain agents vs stateful graphs — what problem it solves
2. Core concepts: StateGraph, nodes, edges, state schema (TypedDict)
3. Building a simple graph: add_node, add_edge, add_conditional_edges, compile
4. State management: how state flows through nodes, state reducers (Annotated with operator.add)
5. Tool nodes: ToolNode, how tools integrate into the graph
6. Conditional routing: routing based on state, END node
7. Persistence: MemorySaver, checkpointing, resuming interrupted graphs
8. Human-in-the-loop: interrupt_before, interrupt_after, updating state mid-run
9. Multi-agent patterns in LangGraph: supervisor agent, subgraph pattern
10. Streaming: how to stream tokens and graph events
11. LangGraph Platform / LangGraph Cloud: deployment options

Python code building progressively: simple chain → tool-using agent → multi-agent supervisor.
Final example: a ReAct agent that uses web search + code execution + RAG retrieval.
```

---

### 4.3 — LlamaIndex (RAG-Focused Framework)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer familiar with LangChain. LlamaIndex is a competing framework that appears frequently in RAG-focused roles.

Give me a focused 2-hour study session on LlamaIndex covering:
1. LlamaIndex vs LangChain: philosophy, strengths, when to choose each
2. Core objects: Document, Node, VectorStoreIndex, QueryEngine, RetrieverQueryEngine
3. Data ingestion: SimpleDirectoryReader, custom readers
4. Node parsers and transformations: SentenceSplitter, metadata extraction
5. Index types: VectorStoreIndex, SummaryIndex, KnowledgeGraphIndex
6. Query engines: how to build them, response synthesizers, node postprocessors
7. Retrievers: VectorIndexRetriever, BM25Retriever, custom retrievers
8. LlamaIndex agents: ReActAgent, function calling agents, AgentRunner
9. Workflows (new in 2024): event-driven agentic orchestration, Steps and Events pattern
10. LlamaIndex + Pinecone / ChromaDB / pgvector integration
11. LlamaIndex + AWS Bedrock

Python code for a complete RAG pipeline in LlamaIndex.
Build the same pipeline in LangChain and compare code complexity side-by-side.
```

---

### 4.4 — Agent Patterns: ReAct, Plan-and-Execute, Reflection
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer building agentic AI systems. I need to understand the fundamental agent design patterns that underlie all frameworks.

Give me a focused 2-hour study session on agent design patterns covering:
1. ReAct (Reasoning + Acting): Thought → Action → Observation loop, original paper explained
2. Implementing ReAct from scratch in Python (no framework) — understand what frameworks hide
3. Plan-and-Execute: planner LLM creates a plan, executor LLM carries it out
4. Reflection and self-critique: agent evaluates its own output and retries
5. Tool use patterns: when to call tools, parallel tool calling, tool output handling
6. Memory patterns:
   - Short-term: conversation history in context window
   - Long-term: external memory in vector store or database
   - Episodic: storing and retrieving past task experiences
7. Agent state machines: representing agent progress as state
8. Guardrails patterns: input validation, output validation, tool call validation
9. Failure recovery: what to do when tools fail, retry logic, fallback strategies
10. Agent evaluation: what makes an agent "good" — task completion, faithfulness, efficiency

Python code implementing ReAct from scratch.
Then show the same agent in LangGraph, demonstrating what the framework gives you.
```

---

### 4.5 — Multi-Agent Systems & Orchestration
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. Multi-agent architectures appear across nearly every senior AI job description in 2026. I need to understand them deeply.

Give me a focused 2-hour study session on multi-agent systems covering:
1. Why multi-agent: specialization, parallelism, overcoming context limits
2. Orchestrator-worker pattern: one agent dispatches tasks to specialized agents
3. Supervisor pattern (LangGraph): how the supervisor routes between agents
4. Swarm pattern: peer agents, handoffs, no central orchestrator
5. Agent communication: shared state, message passing, event queues
6. Tool isolation: each agent has different tool permissions — security model
7. AutoGen (Microsoft): ConversableAgent, GroupChat, code execution sandboxing
8. CrewAI: Role-based agents, tasks, crews — when to use over LangGraph
9. Parallel execution: running multiple agents simultaneously, gathering results
10. Coordination patterns: voting, consensus, critic-reviser
11. Real production example: a code review multi-agent system (planner, coder, reviewer, tester)

Python code implementing the supervisor pattern in LangGraph.
Also implement a CrewAI crew for the same task. Compare code and architecture.
```

---

### 4.6 — Tool Design & Function Calling
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. Tool design is one of the most important — and underestimated — skills in agentic AI systems.

Give me a focused 2-hour study session on tool design for AI agents covering:
1. What tools are: functions exposed to LLMs, how they map to API/function calls
2. Tool schema design: name, description, parameters — why description quality matters enormously
3. Anthropic tool_use format: tool definitions, tool_use blocks, tool_result blocks
4. OpenAI function calling format: function definitions, tool_calls, parallel tool calls
5. LangChain @tool decorator: how to define tools, type hints, docstrings as descriptions
6. LangGraph ToolNode: automatic tool execution in graphs
7. Tool categories: read tools, write tools, search tools, compute tools — permission design
8. Sandboxing tool execution: E2B (remote code execution), Docker containers
9. Tool error handling: tool failures, partial results, retry logic
10. Stateful tools: tools that maintain state across calls
11. MCP (Model Context Protocol): Anthropic's standard for tool/resource exposure
12. 10 real-world tools every production agent needs (web search, code runner, file reader, SQL query...)

Python code: implement 5 production-quality tools with proper schemas and error handling.
Build an agent that uses these tools and show how tool descriptions affect behavior.
```

---

### 4.7 — Memory Systems for Agents
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. Memory is a key differentiator between toy agents and production agents. It's listed in Microsoft, Hitachi, and other job descriptions.

Give me a focused 2-hour study session on agent memory systems covering:
1. Four types of memory: sensory (context window), short-term (conversation), long-term (external), episodic (experiences)
2. In-context memory: conversation history management, summarization when context fills up
3. External memory with vector stores: storing and retrieving past conversations
4. Semantic memory: facts about the user/domain stored as embeddings
5. Episodic memory: storing task traces for future reference
6. Procedural memory: storing learned behaviors / instructions
7. LangChain memory: ConversationBufferMemory, ConversationSummaryMemory, VectorStoreRetrieverMemory
8. LangGraph checkpointer memory: MemorySaver, SQLiteSaver, persistent state
9. Mem0 (memory layer library): open-source agent memory system
10. Memory in production: user isolation, TTL, privacy, GDPR considerations
11. Building a personalized agent: one that remembers user preferences across sessions

Python code: build a conversational agent with full memory (short-term + long-term + episodic).
Show how memory retrieval affects answer quality over multi-session conversations.
```

---

### 4.8 — Guardrails & Safety for AI Agents
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer building agents for regulated enterprise environments (financial services, compliance). Guardrails are critical and mentioned in Slalom, Hitachi, and other job descriptions.

Give me a focused 2-hour study session on AI guardrails covering:
1. Why guardrails matter in enterprise: compliance, liability, hallucination costs
2. Input guardrails: prompt injection detection, jailbreak detection, off-topic filtering
3. Output guardrails: hallucination detection, PII detection and redaction, toxicity filtering
4. AWS Bedrock Guardrails: content filters, denied topics, word filters, sensitive info, grounding
5. Guardrails AI (open-source library): validators, guards, on_fail actions
6. NeMo Guardrails (NVIDIA): colang language, dialogue flow control
7. LlamaGuard (Meta): LLM-based safety classifier
8. Grounding checks: verifying LLM answers are supported by retrieved context
9. Rate limiting and budget controls: preventing runaway agent loops
10. Audit logging: capturing every LLM call for compliance review
11. Testing guardrails: red-teaming, adversarial prompts, evaluation datasets

Python code implementing a production guardrail stack using AWS Bedrock Guardrails + Guardrails AI.
Include a test suite of adversarial prompts that should be caught.
```

---

## TRACK 5 — OBSERVABILITY & MLOPS FOR AI

### 5.1 — LangSmith (LangChain Observability)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. LangSmith is mentioned in most LangChain-related job postings as the standard for LLM observability. I need to learn it.

Give me a focused 2-hour study session on LangSmith covering:
1. What LangSmith is: tracing, evaluation, dataset management, prompt hub
2. Setup: LANGCHAIN_TRACING_V2, LANGCHAIN_API_KEY environment variables
3. Automatic tracing: how LangChain automatically traces to LangSmith
4. Manual tracing: @traceable decorator, RunTree for non-LangChain code
5. Reading traces: understanding the trace tree (runs, spans, inputs, outputs, latency, cost)
6. Datasets: creating evaluation datasets from production traces
7. Evaluators: running RAGAS-style evals, custom evaluators, LLM-as-judge
8. Experiments: comparing two versions of a chain on the same dataset
9. Prompt management: LangSmith Hub, versioning prompts, pulling prompts in code
10. Cost tracking: monitoring token usage and cost per chain/agent
11. LangSmith for production monitoring: setting up alerts, dashboards

Python code: instrument a RAG chain and an agent with full LangSmith tracing.
Show how to identify a retrieval failure from a LangSmith trace.
```

---

### 5.2 — Weights & Biases (W&B) for LLMs
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer with Dynatrace and APM experience. I need to learn W&B (Weights & Biases) as it appears in MLOps and AI engineering job descriptions.

Give me a focused 2-hour study session on W&B for LLM/AI systems covering:
1. What W&B is: experiment tracking, model registry, artifact management, LLM tracing
2. Setup: wandb.init(), project/entity structure, free tier capabilities
3. Logging: wandb.log() for metrics, tables, charts, media
4. W&B Weave (LLM observability product): tracing LLM calls, evaluations
5. Weave tracing: @weave.op() decorator, automatic OpenAI/Anthropic instrumentation
6. Weave evaluations: Evaluation class, scorers, running evals across datasets
7. Weave datasets: managing test sets in W&B
8. Artifact management: versioning datasets, prompts, and model configs
9. Sweeps: hyperparameter optimization (for fine-tuning workflows)
10. W&B vs LangSmith vs Arize: when to use each
11. Integration with LangChain: WandbTracer callback

Python code using W&B Weave to trace and evaluate a RAG pipeline.
Use the free W&B cloud account — no billing required.
```

---

### 5.3 — Arize Phoenix (Open-Source LLM Observability)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. Arize Phoenix is an open-source LLM observability tool that I can run locally or self-host — important for regulated/compliance environments.

Give me a focused 2-hour study session on Arize Phoenix covering:
1. What Arize Phoenix is: open-source, runs locally, OpenTelemetry-based
2. Why it matters for enterprise: self-hosted, no data leaving your environment
3. Setup: pip install arize-phoenix, px.launch_app()
4. OpenTelemetry instrumentation: how it auto-instruments OpenAI, Anthropic, LangChain
5. Traces UI: reading spans, seeing prompt/response pairs, latency, token counts
6. Evals in Phoenix: hallucination, Q&A correctness, relevance — built-in evaluators
7. Datasets and experiments: running offline evaluation experiments
8. Phoenix in production: running as a container, persisting data
9. LangChain integration: OpenInference LangChain tracer
10. LlamaIndex integration
11. Comparing Phoenix vs LangSmith vs W&B Weave

Python code: instrument a RAG pipeline with Phoenix, then run hallucination evaluation.
Everything runs locally — no cloud accounts needed.
```

---

### 5.4 — MLflow for LLMs
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. MLflow is a widely deployed MLOps platform and is gaining LLM tracking capabilities. It appears in enterprise job descriptions including Kyndryl.

Give me a focused 2-hour study session on MLflow for LLM systems covering:
1. What MLflow is: experiment tracking, model registry, serving — the enterprise standard
2. MLflow tracking: mlflow.start_run(), logging params, metrics, artifacts
3. MLflow Models: logging LLM chains as models (mlflow.langchain.log_model)
4. MLflow Tracing: @mlflow.trace decorator, automatic LangChain/LlamaIndex tracing
5. MLflow Model Registry: registering, versioning, staging (Staging → Production)
6. MLflow serving: mlflow models serve — deploying a chain as a REST API
7. MLflow Evaluate: evaluating LLM outputs with built-in and custom metrics
8. Databricks + MLflow: how Databricks extends MLflow (relevant for enterprise interviews)
9. Self-hosting MLflow: running the tracking server on AWS EC2 / S3 backend
10. MLflow vs LangSmith vs W&B: which to use in which context

Python code: track a RAG pipeline experiment in MLflow, register the model, and serve it.
```

---

## TRACK 6 — CLOUD AI SERVICES

### 6.1 — AWS Lambda for AI Workloads
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AWS Engineer. I need to master deploying AI/agent code on AWS Lambda for production agentic systems.

Give me a focused 2-hour study session on AWS Lambda for AI workloads covering:
1. Lambda for AI: when it's appropriate (stateless inference, event-driven agent steps)
2. Container images for Lambda: packaging large dependencies (LangChain, torch)
3. Lambda function URLs: invoking agents via HTTP without API Gateway
4. API Gateway + Lambda: REST API pattern for agent endpoints
5. Lambda + Bedrock: invoking Bedrock from Lambda, IAM role patterns
6. Lambda + Bedrock Agents: triggering Bedrock Agents from Lambda
7. Lambda layers for shared dependencies
8. Cold start mitigation: provisioned concurrency, SnapStart (Java, now Python)
9. Timeout and memory limits: right-sizing for LLM workloads (3–15 minute timeouts)
10. Lambda + Step Functions: orchestrating multi-step agent workflows
11. Lambda + EventBridge: event-driven agent triggers
12. Observability: CloudWatch Logs, Lambda Powertools for structured logging and tracing

Python + SAM/CDK deployment examples.
Deploy a LangGraph agent to Lambda as a container image end-to-end.
```

---

### 6.2 — AWS Step Functions for Agent Orchestration
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AWS Engineer. Step Functions is a powerful alternative to LangGraph for orchestrating AI agent workflows in AWS-native environments.

Give me a focused 2-hour study session on AWS Step Functions for AI agent orchestration:
1. What Step Functions is: serverless workflow orchestration, state machine as code
2. When to use Step Functions vs LangGraph: AWS-native, long-running, built-in retry/error handling
3. State machine definition: Amazon States Language (ASL), JSON/YAML
4. Task states: Lambda invocations, Bedrock InvokeModel, DynamoDB operations
5. Choice states: conditional branching (routing agent decisions)
6. Parallel states: running multiple agent steps in parallel
7. Map states: processing arrays (batch document processing)
8. Wait states: human approval workflows, async coordination
9. Express vs Standard workflows: cost and execution model differences
10. SDK integrations: calling Bedrock, DynamoDB, S3 directly without Lambda
11. Error handling: Catch, Retry, fallback states
12. Building an agentic RAG pipeline in Step Functions: ingest → chunk → embed → query → respond

CDK Python code for deploying a multi-step agentic workflow in Step Functions.
```

---

### 6.3 — AWS SageMaker (ML Platform)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AWS Engineer. SageMaker appears in senior ML/AI engineering job descriptions. I need to understand it for interviews even if I won't use all features.

Give me a focused 2-hour study session on AWS SageMaker for LLM/AI systems covering:
1. SageMaker overview: what it covers (training, hosting, pipelines, experiments, feature store)
2. SageMaker JumpStart: deploying open-source LLMs (Llama, Mistral) as endpoints
3. SageMaker Endpoints: deploying custom model containers, real-time vs async
4. SageMaker Pipelines: ML pipeline orchestration (compare to Step Functions)
5. SageMaker Experiments: experiment tracking (compare to MLflow)
6. SageMaker Feature Store: storing and retrieving ML features
7. SageMaker Ground Truth: data labeling (for fine-tuning dataset creation)
8. HuggingFace on SageMaker: deploying HF models, training with SageMaker HF estimator
9. SageMaker vs Bedrock: when to use each — the key distinction
10. Cost management: instance types for LLM hosting, saving plans

Python boto3 code for deploying a HuggingFace LLM on SageMaker as a real-time endpoint.
```

---

## TRACK 7 — FINE-TUNING & MODEL CUSTOMIZATION

### 7.1 — Fine-Tuning Concepts (When & Why)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. Fine-tuning is mentioned in the Kyndryl and Cliff Services job descriptions. I need to understand when to fine-tune vs RAG vs prompt engineering.

Give me a focused 2-hour study session on fine-tuning concepts covering:
1. The decision framework: when to fine-tune vs RAG vs few-shot prompting
2. What fine-tuning actually does to a model: weights, gradient updates, catastrophic forgetting
3. Full fine-tuning vs parameter-efficient fine-tuning (PEFT)
4. LoRA explained: low-rank adaptation, rank parameter, what changes in the model
5. QLoRA: quantized LoRA, how it enables fine-tuning on consumer hardware
6. Dataset requirements: format, size, quality — what makes a good fine-tuning dataset
7. Generating synthetic training data with LLMs: the self-instruct pattern
8. Evaluation: train/val/test split, loss curves, task-specific metrics
9. Fine-tuning APIs: OpenAI fine-tuning, AWS Bedrock fine-tuning, Google Vertex fine-tuning
10. Serving fine-tuned models: merging adapters, serving with vLLM
11. When fine-tuning fails: overfitting, data contamination, format issues

Focus on concepts and decision-making. Python examples for dataset generation.
I need to understand this to discuss it intelligently in interviews, not necessarily implement it from scratch.
```

---

### 7.2 — Dataset Generation for Fine-Tuning
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. The Kyndryl job description mentions "fine-tuning pipeline including dataset generation." I need to learn how to generate training data with LLMs.

Give me a focused 2-hour study session on AI-generated dataset creation for fine-tuning:
1. Why synthetic data: real data is scarce, expensive, and may contain PII
2. Self-instruct method: using a strong LLM to generate instruction-response pairs
3. Generating instruction datasets: prompts that produce diverse question-answer pairs
4. Alpaca format: the standard fine-tuning data format (instruction, input, output)
5. ShareGPT format: multi-turn conversation format
6. Domain-specific dataset generation: generating data from your company's documents
7. Quality filtering: deduplication, length filtering, quality scoring with LLM judges
8. Distillation: using GPT-4 / Claude to teach a smaller model
9. Preference data (for RLHF/DPO): chosen vs rejected responses
10. Data contamination risks: accidentally including test data
11. Tools: Argilla, LabelStudio for human review and annotation

Python code: build a dataset generation pipeline that takes a document corpus and produces
an instruction-following dataset for fine-tuning. Target: 1000+ examples from a knowledge base.
```

---

## TRACK 8 — ADVANCED & SPECIALIZED TOPICS

### 8.1 — Model Context Protocol (MCP)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. MCP (Model Context Protocol) is Anthropic's new open standard for connecting AI agents to tools and data. It's appearing in cutting-edge job descriptions and is important for the future of agentic AI.

Give me a focused 2-hour study session on MCP covering:
1. What MCP is: open protocol, client-server architecture, what problem it solves
2. MCP vs traditional tool use: how MCP standardizes tool exposure across clients
3. MCP architecture: MCP hosts (Claude Desktop, IDEs), MCP clients, MCP servers
4. MCP servers: resources (data), tools (actions), prompts (templates)
5. Building an MCP server in Python: mcp library, @server.tool(), @server.resource()
6. Transports: stdio (local), HTTP+SSE (remote)
7. Built-in MCP servers: filesystem, browser, Slack, GitHub — what's available
8. Connecting to Claude Desktop: configuring claude_desktop_config.json
9. MCP for enterprise: authentication, authorization, deployment patterns
10. MCP vs LangChain tools vs Bedrock action groups — comparison
11. Future of MCP: why this is becoming the standard for agent tool integration

Python code: build an MCP server exposing database query + document search tools.
Connect it to Claude Desktop and test tool invocation.
```

---

### 8.2 — GraphRAG & Knowledge Graphs for AI
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. GraphRAG and knowledge graphs appear in specialized job descriptions (Cliff Services, Microsoft research). I need a solid understanding even if not a specialist.

Give me a focused 2-hour study session on GraphRAG and knowledge graphs for AI covering:
1. Limitations of vector RAG: why it misses multi-hop reasoning and relationship queries
2. What knowledge graphs are: entities, relationships, triples (subject-predicate-object)
3. Property graphs vs RDF: Neo4j (property) vs SPARQL/RDF (semantic web)
4. GraphRAG (Microsoft): the paper, community detection, global vs local search
5. LlamaIndex KnowledgeGraphIndex: building a graph from documents
6. Neo4j + LangChain: LangChain Neo4jGraph, GraphCypherQAChain
7. Entity extraction for graph construction: using LLMs to extract entities and relationships
8. Hybrid graph-vector retrieval: combining graph traversal with vector similarity
9. When GraphRAG beats vector RAG: multi-hop questions, relationship queries, summarization
10. Ontology basics: classes, properties, hierarchy — enough to discuss in an interview
11. AWS Neptune as a managed graph database alternative to Neo4j

Python code: build a simple knowledge graph from text using LlamaIndex and query it.
Compare answers to the same question using vector RAG vs GraphRAG.
```

---

### 8.3 — Semantic Kernel (Microsoft)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. Semantic Kernel is Microsoft's AI orchestration framework and appears in Azure/Microsoft-focused job descriptions. I need to understand it for interviews.

Give me a focused 2-hour study session on Semantic Kernel (Python SDK) covering:
1. What Semantic Kernel is: Microsoft's LLM orchestration framework, open-source
2. Core concepts: Kernel, plugins, functions (semantic + native), memory
3. Kernel setup: connecting to Azure OpenAI vs OpenAI vs other models
4. Plugins: grouping related functions, KernelPlugin, @kernel_function decorator
5. Semantic functions: prompts as functions, prompt templates, PromptTemplateConfig
6. Native functions: Python functions exposed as AI-callable functions
7. Auto function calling: SK automatically invokes functions when LLM requests
8. Memory / Vector stores in SK: VolatileMemoryStore, AzureAISearchMemoryStore
9. Planner: automatic plan creation from a goal (compare to LangGraph planner)
10. SK Process Framework: new workflow orchestration (compete to LangGraph)
11. SK vs LangChain vs LangGraph: honest comparison, when Microsoft shops use SK

Python code examples for every concept.
Build a simple agent in Semantic Kernel that uses plugins and auto function calling.
```

---

### 8.4 — AutoGen (Microsoft Multi-Agent)
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. AutoGen is Microsoft's multi-agent framework and appears in AI engineering job descriptions alongside LangGraph and CrewAI.

Give me a focused 2-hour study session on AutoGen v0.4+ covering:
1. What AutoGen is: multi-agent conversation framework, ConversableAgent pattern
2. AutoGen v0.4 architecture: AgentChat, Core (async actor model) — new design
3. Basic agents: AssistantAgent, UserProxyAgent, ConversableAgent
4. Conversations: two-agent chat, group chat, nested chat
5. Code execution: LocalCommandLineCodeExecutor, DockerCommandLineCodeExecutor (sandboxed)
6. Group chat: GroupChat, GroupChatManager, speaker selection strategies
7. Tool use in AutoGen: registering functions as tools, automatic execution
8. AutoGen Studio: no-code UI for building multi-agent workflows
9. Termination conditions: how to end agent conversations appropriately
10. AutoGen vs LangGraph vs CrewAI: honest comparison, when to use each
11. Human-in-the-loop: incorporating human feedback in agent conversations

Python code: build a software development team (product manager, coder, reviewer, tester) using AutoGen.
Show code execution sandboxing in action.
```

---

### 8.5 — CrewAI
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. CrewAI is a popular multi-agent framework that often appears in job descriptions alongside LangGraph and AutoGen.

Give me a focused 2-hour study session on CrewAI covering:
1. What CrewAI is: role-based agents, task-focused, opinionated framework
2. Core concepts: Agent, Task, Crew, Process (sequential vs hierarchical)
3. Defining agents: role, goal, backstory, tools, llm, memory
4. Defining tasks: description, expected_output, agent assignment, context (task dependencies)
5. Defining crews: assembling agents and tasks, kicking off
6. Tools in CrewAI: SerperDevTool, FileReadTool, custom tools with @tool
7. Memory in CrewAI: short-term, long-term, entity memory — how it stores between runs
8. Hierarchical process: manager agent distributing tasks to worker agents
9. CrewAI Flows: event-driven orchestration (new feature)
10. CrewAI vs LangGraph vs AutoGen: when CrewAI is the right choice (rapid prototyping, role clarity)
11. Deploying CrewAI in production: async execution, callback patterns

Python code: build a market research crew (researcher, analyst, writer) that researches a company
and produces a report. Compare the code length and clarity vs the same system in LangGraph.
```

---

### 8.6 — vLLM & Local LLM Hosting
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. Some enterprise jobs require understanding how to host open-source LLMs (Llama, Mistral) rather than always calling APIs.

Give me a focused 2-hour study session on local/self-hosted LLM serving covering:
1. Why self-host: cost at scale, data privacy, latency, fine-tuned models
2. vLLM: what it is, PagedAttention, why it's the production standard for LLM serving
3. Setting up vLLM: pip install, launching a server, OpenAI-compatible API endpoint
4. GPU requirements: what hardware you need for different model sizes
5. Model quantization: GGUF, GPTQ, AWQ — serving quantized models on smaller GPUs
6. Ollama: local LLM runner, simple setup for development (runs on CPU/laptop)
7. Using Ollama in LangChain and LlamaIndex: drop-in replacement for OpenAI
8. AWS EC2 for LLM hosting: g4dn (T4 GPU) vs g5 (A10G) — cost vs capability
9. AWS SageMaker for LLM hosting: managed alternative
10. Batching and throughput optimization in vLLM
11. When to use self-hosted vs Bedrock vs OpenAI API

Python code: deploy Llama 3.2 locally with Ollama and connect it to a LangChain RAG pipeline.
Replace the OpenAI client with the Ollama client — show the swap is 3 lines of code.
```

---

### 8.7 — Streaming Responses & Real-Time UI Patterns
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. Streaming LLM responses is expected in production applications and appears in full-stack AI roles.

Give me a focused 2-hour study session on streaming in AI applications covering:
1. Why streaming: perceived latency, UX, time-to-first-token
2. Streaming with Anthropic API: stream=True, MessageStreamEvent types
3. Streaming with OpenAI API: stream=True, delta content
4. Streaming with LangChain: .stream() vs .astream(), StreamingStdOutCallbackHandler
5. Streaming with LangGraph: astream_events() — streaming tokens and graph events
6. Server-Sent Events (SSE): how streaming works over HTTP
7. FastAPI streaming responses: StreamingResponse, async generators
8. WebSockets for streaming: when to use WS vs SSE
9. Gradio for streaming AI UIs: gr.ChatInterface with streaming
10. Streamlit streaming: st.write_stream
11. Token counting during streaming: tracking usage without waiting for final response

Python code: build a streaming RAG chatbot with FastAPI (SSE backend) + Streamlit frontend.
Show the difference in perceived responsiveness vs non-streaming.
```

---

### 8.8 — CI/CD for AI Systems
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. CI/CD for AI/ML pipelines appears in Hitachi, Kyndryl, and other job descriptions. This is different from regular software CI/CD.

Give me a focused 2-hour study session on CI/CD for AI systems covering:
1. Why AI CI/CD is different: non-determinism, data dependencies, model drift
2. Testing strategies for LLM applications:
   - Unit tests for tools and chains (mock LLM calls)
   - Integration tests with real LLM calls (expensive, run less often)
   - Regression tests: comparing outputs before and after a change
3. GitHub Actions for AI pipelines: automated testing, deployment workflows
4. Testing RAG pipelines: automated RAGAS evaluation on every PR
5. Prompt versioning: how to version and test prompt changes
6. Model versioning: tracking which model version is in production
7. Feature flags for AI: gradual rollout of new models/prompts
8. Blue-green deployment for AI services
9. Automated evaluation gates: blocking deploys when eval scores drop
10. AWS CodePipeline + SageMaker Pipelines for ML-specific CI/CD
11. LangSmith datasets as regression test suites

Python + GitHub Actions YAML: build a CI/CD pipeline that runs RAGAS evaluation on every PR
and blocks merge if faithfulness score drops below threshold.
```

---

### 8.9 — Vector Database Selection & Architecture
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. I want a comprehensive decision framework for choosing vector databases in enterprise production systems — this is a common senior interview question.

Give me a focused 2-hour study session on vector database architecture and selection covering:
1. The vector database landscape in 2026: who the players are, market position
2. Comparison matrix: FAISS, ChromaDB, Pinecone, Weaviate, Qdrant, pgvector, Milvus, OpenSearch
3. Evaluation criteria: scale, latency, filtering, hybrid search, cost, managed vs self-hosted, compliance
4. FAISS: when to use (local dev, research, <10M vectors, no metadata filtering needs)
5. ChromaDB: when to use (prototyping, small teams, simple metadata)
6. Pinecone: when to use (managed, scalable, enterprise, pay-as-you-go)
7. pgvector: when to use (already have PostgreSQL, regulated env, operational simplicity)
8. Weaviate: when to use (complex schema, built-in ML, open-source self-hosted)
9. Qdrant: when to use (performance, Rust-based, strong filtering)
10. OpenSearch / Elasticsearch with vector: when to use (already have it, hybrid search)
11. AWS-native options: OpenSearch Serverless, Bedrock Knowledge Bases default store
12. Multi-tenant RAG architecture: namespace isolation, per-tenant indexes

Architecture diagram descriptions and a decision tree.
Python code connecting to 3 different vector stores from the same LangChain chain.
```

---

## TRACK 9 — PRODUCTION PATTERNS

### 9.1 — Cost Optimization for LLM Applications
- [ ] Studied

**Prompt:**
```
I am a Senior Python/AI Engineer. LLM API costs can spiral in production. Cost management is a real concern in enterprise AI engineering.

Give me a focused 2-hour study session on LLM cost optimization covering:
1. Understanding token costs: input vs output tokens, why output is more expensive
2. Model selection for cost: Claude Haiku vs Sonnet vs Opus — routing by task complexity
3. LLM routing: using a cheap model for classification, expensive for generation
4. Caching strategies:
   - Exact match caching: same query → cached response (Redis)
   - Semantic caching: similar query → cached response (GPTCache, LangChain cache)
   - Prompt caching: Anthropic prompt caching for repeated system prompts (90% cost reduction)
5. Context window management: only sending relevant chunks, not whole documents
6. Batching API calls: Anthropic Batch API (50% discount), OpenAI batch endpoint
7. Output length control: constraining output tokens with max_tokens, structured outputs
8. Self-hosted models for high-volume: break-even analysis vs API
9. Monitoring costs: tracking spend by user, feature, model
10. Budget alerts and rate limiting to prevent runaway costs

Python code: implement semantic caching with Redis and show cost reduction on a real RAG pipeline.
Build a model router that selects cheap vs expensive model based on query complexity.
```

---

### 9.2 — Async & High-Throughput AI Pipelines
- [ ] Studied

**Prompt:**
```
I am a Senior Python Engineer. Production AI systems need to handle concurrent requests efficiently. I need to master async patterns for AI pipelines.

Give me a focused 2-hour study session on async AI pipelines covering:
1. Why async matters for AI: I/O-bound LLM calls, concurrent user requests
2. Python asyncio fundamentals: async/await, event loop, coroutines
3. Async LLM clients: AsyncAnthropic, AsyncOpenAI — how to use them
4. Parallel LLM calls with asyncio.gather(): processing multiple documents simultaneously
5. Semaphore for rate limiting: preventing API rate limit errors under load
6. Async LangChain: ainvoke, astream, async chains
7. Async LangGraph: astream_events, async nodes
8. FastAPI for async AI endpoints: async def handlers, background tasks
9. Celery + Redis for background AI jobs: when async isn't enough
10. AWS SQS + Lambda: event-driven async AI processing at scale
11. Benchmarks: sync vs async for 10/100/1000 concurrent RAG queries

Python code: build an async RAG pipeline that processes 100 documents in parallel
vs sequentially — measure the throughput difference.
```

---

## TRACK 10 — FLAGSHIP PROJECT

### 10.1 — Cornerstone Project: Enterprise AI Analyst Agent

**Project Title:** `ARIA — Agentic Retrieval & Intelligence Analyst`

**What it demonstrates to employers:**
Every skill from this curriculum, production-quality, in a single deployable system.

---

**Project Description:**

ARIA is a multi-agent system that ingests enterprise documents (PDFs, reports, code, web pages),
builds a hybrid RAG knowledge base, and answers complex multi-hop questions using an
orchestrated team of specialized agents — with full observability, guardrails, and CI/CD.

---

**Architecture:**

```
                    ┌─────────────────────────────────────┐
                    │          ARIA System                │
                    │                                     │
  Documents ──────► │  Ingestion Pipeline                 │
  (PDF/DOCX/HTML)   │  ├─ Document Parser (Unstructured)  │
                    │  ├─ Chunking (semantic + hierarchical│
                    │  ├─ Embeddings (Bedrock Titan /      │
                    │  │    text-embedding-3-small)        │
                    │  └─ Vector Store (pgvector on RDS)   │
                    │       + Keyword Index (BM25)         │
                    │                                     │
  User Query ──────►│  Orchestrator Agent (LangGraph)     │
                    │  ├─ Query Classifier                 │
                    │  ├─ Retriever Agent                  │
                    │  │   └─ Hybrid search + Reranking    │
                    │  ├─ Analyst Agent                    │
                    │  │   └─ Multi-hop reasoning          │
                    │  ├─ Code Agent (if code questions)   │
                    │  └─ Response Synthesizer             │
                    │       └─ Citations + Grounding check │
                    │                                     │
                    │  Guardrails (Bedrock Guardrails)    │
                    │  Observability (Arize Phoenix)      │
                    │  API (FastAPI + Streaming)          │
                    │  UI (Streamlit)                     │
                    └─────────────────────────────────────┘
```

---

**Tech Stack:**

| Component | Technology | Why |
|-----------|-----------|-----|
| LLM | Claude Sonnet (Bedrock) | Your existing expertise |
| Embeddings | Amazon Titan Embeddings v2 | Free on Bedrock |
| Vector DB | pgvector (AWS RDS free tier) | Covers pgvector interview requirement |
| Chunking | LangChain RecursiveCharacterTextSplitter + SemanticChunker | Shows chunking depth |
| Document parsing | Unstructured.io (local) | Production-quality ingestion |
| Hybrid search | pgvector + BM25 via LangChain EnsembleRetriever | Shows hybrid search |
| Reranking | Cohere Rerank API (free tier) | Shows reranking knowledge |
| Agent framework | LangGraph | Shows stateful multi-agent |
| Guardrails | AWS Bedrock Guardrails | Shows enterprise safety |
| Observability | Arize Phoenix (local) | Shows MLOps thinking |
| API | FastAPI (async, streaming) | Production-grade API |
| UI | Streamlit | Demo-ready |
| Evaluation | RAGAS | Shows eval framework |
| CI/CD | GitHub Actions | Automated eval on PR |
| Deployment | AWS Lambda (container) or EC2 | AWS production deploy |

**Estimated cloud cost:** ~$5–15/month on free tiers + minimal pay-as-you-go

---

**Phases:**

**Phase 1 — Foundation (Week 1)**
- [ ] Set up pgvector on local Docker + RDS free tier
- [ ] Build document ingestion pipeline (PDF, DOCX, HTML → chunks → embeddings → pgvector)
- [ ] Naive RAG working end-to-end with LangChain
- [ ] RAGAS evaluation baseline established

**Phase 2 — Advanced Retrieval (Week 2)**
- [ ] Hybrid search (BM25 + vector with EnsembleRetriever)
- [ ] Reranking with Cohere
- [ ] Parent-child document retrieval
- [ ] Retrieval quality improved vs baseline (measured with RAGAS)

**Phase 3 — Multi-Agent (Week 3)**
- [ ] LangGraph orchestrator with query classification
- [ ] Specialist agents: retrieval agent, analyst agent, code agent
- [ ] Agent memory (LangGraph MemorySaver for session, pgvector for long-term)
- [ ] Human-in-the-loop for low-confidence answers

**Phase 4 — Production (Week 4)**
- [ ] AWS Bedrock Guardrails integration
- [ ] Arize Phoenix observability (full tracing)
- [ ] FastAPI async streaming API
- [ ] Streamlit UI with streaming, citation display, conversation history
- [ ] CI/CD with GitHub Actions (RAGAS eval gate)
- [ ] Deploy to AWS Lambda (container image)

---

**Prompt to start Phase 1:**
```
I am a Senior Python/AWS Engineer. I want to build a production-quality multi-agent RAG system
called ARIA (Agentic Retrieval & Intelligence Analyst) as a portfolio project.

Help me build Phase 1 — Foundation:

1. Docker compose file for local PostgreSQL with pgvector extension
2. Python document ingestion pipeline using:
   - Unstructured.io for PDF/DOCX parsing
   - LangChain RecursiveCharacterTextSplitter
   - Amazon Titan Embeddings v2 via AWS Bedrock (boto3)
   - pgvector storage using LangChain PGVector
3. Naive RAG query engine:
   - Hybrid search: pgvector similarity + BM25 keyword search via EnsembleRetriever
   - Claude Sonnet via Bedrock for generation
   - Grounded prompt that cites source documents
4. RAGAS evaluation harness:
   - 10 test questions over the ingested documents
   - Measure faithfulness, answer_relevancy, context_precision baseline

Tech stack: Python, LangChain, AWS Bedrock, pgvector, Docker.
My AWS credentials are configured. I have Docker Desktop.
Produce working, runnable code for every component.
```

---

**Interview talking points this project enables:**

When asked about any of these topics, you can say:
> "In my ARIA project, I implemented [topic] and specifically found that [concrete observation].
> Here's the GitHub link: github.com/sgirgis/aria-agent"

Topics covered: RAG, hybrid search, reranking, multi-agent, LangGraph, pgvector, guardrails,
observability, evaluation, CI/CD, FastAPI, Streamlit, AWS Bedrock, async, streaming.

---

*Last updated: 2026-03-11*
*Built for: Kyndryl, Hitachi, Microsoft, Slalom, Motion Recruitment, and similar 2026 job targets*
