Key Insight
A single event triggers multiple independent actions

That is Observer pattern.
Concrete RAG Events
Event 1: Query Received
Observers:
- Retriever
- Query Logger
- Rate Limiter
- Safety Filter
Event 2: Documents Retrieved
Observers:
- Reranker
- Context Builder
- Debug Logger
Event 3: LLM Response Generated
Observers:
- Response Logger
- Feedback Collector
- Metrics Tracker
So instead of this:
# BAD (tight coupling)retriever.retrieve()logger.log()analytics.track()


We want:
# GOOD (observer)event.notify_all()


Let’s Build a Simple RAG with Observer