'''
Problem we’re solving

Previous version:

        with lock:
            if instance is None:
                create()
Issue:
Lock happens every time
Even after object is already created

At scale:

1000 req/sec → 1000 lock acquisitions → unnecessary contention/waiting even though object is already created
'''

'''
Idea of double checking:

We reduce locking by 

Check 1 (no lock) → fast path
Check 2 (with lock) → safe creation

Flow -- if instance exists return it without locking, if not acquire lock and check again if instance exists, if not create it

'''

import threading


class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        print("Constructor called")

    @classmethod
    def get_instance(cls):
        # First check (NO LOCK)
        if cls._instance is None:
            with cls._lock:
                # Second check (WITH LOCK)
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance


# Simulate concurrency
def create_instance():
    obj = Singleton.get_instance()
    print(f"Instance ID: {id(obj)}")


threads = []

for _ in range(5):
    t = threading.Thread(target=create_instance)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

'''
Output :
    Constructor called
    Instance ID: 2523098211456
    Instance ID: 2523098211456
    Instance ID: 2523098211456
    Instance ID: 2523098211456
    Instance ID: 2523098211456
'''

'''
Execution Flow :

# very first call 
1. Thread 1: sees None → enters lock → creates instance
2. Thread 2: sees None → waits → enters lock → sees already created → skips

# After instance exists

1.Thread N: sees NOT None → returns immediately
    (no lock at all)
    
'''



