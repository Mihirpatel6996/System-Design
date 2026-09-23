1. What is Singleton? (practical definition)

A Singleton ensures:

Only one instance of a class exists in the entire system, and everyone uses that same instance.

Why does this even matter in real systems?

Think in terms of systems, not classes:

Database connection pool → you don’t want 1000 separate pools
Logger → all services should log to the same place
Cache (Redis client) → single shared client instance
Config manager → one source of truth

If you don’t control instance creation →
you silently create multiple objects → state fragmentation + resource waste