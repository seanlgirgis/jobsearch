# CarMax Interview Prep — Backend AI/ML Serving Scalability

Role context:
- CarMax — Sr Software Engineer - Backend
- Plano, TX / DFW
- Framing: senior Python backend/data engineer with APIs, distributed systems, AWS, databases, production support, reliability, and AI/ML data workflow exposure.

## Q1: Is horizontal scaling and load balancing the least relevant concern when deploying a model that must handle 500 requests per second with p99 latency under 100 ms?

Answer:
No. Horizontal scaling and load balancing are not the least relevant concern. For 500 RPS with p99 latency under 100 ms, they are core deployment concerns.

Key points:
- One model-serving instance may not handle 500 requests/sec.
- Horizontal scaling lets us add warm replicas.
- Load balancing prevents one overloaded instance from ruining p99 latency.
- p99 latency is tail latency, so uneven traffic distribution matters.
- Scaling and load balancing must be combined with model optimization, efficient serving, batching/caching when appropriate, CPU/GPU sizing, queue management, and monitoring.

Interview answer:
"For 500 RPS with p99 under 100 ms, horizontal scaling and load balancing are highly relevant, not least relevant. They help distribute traffic, protect tail latency, and provide availability. But they must be combined with model optimization, efficient serving, warm replicas, batching or caching where appropriate, and careful p50/p95/p99 monitoring."

## Q2: Is loading a 4GB model into memory on every API request a sound approach?

Answer:
No. Loading a 4GB model on every request is a bad serving design.

Key points:
- It would add huge startup latency to every request.
- It would waste CPU/GPU, disk I/O, and memory.
- It would destroy throughput and p99 latency.
- It could cause memory pressure, crashes, and unstable production behavior.
- The model should be loaded once per worker or serving process and kept warm.

Interview answer:
"No. A large model should be loaded once when the worker or model-serving process starts, then reused for incoming requests. Loading a 4GB model per request would destroy latency and throughput, especially with a p99 target under 100 ms. In production I would use warm model replicas behind a load balancer, monitor p50/p95/p99 latency, and consider batching, caching, quantization, or GPU acceleration depending on the workload."
