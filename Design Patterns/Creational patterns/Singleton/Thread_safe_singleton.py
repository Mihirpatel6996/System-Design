import threading


class Singleton:
    _instance = None
    _lock = threading.Lock()  # equivalent to C++ mutex -> static mutex mtx;

    def __init__(self):
        print("Constructor called")

    @classmethod
    def get_instance(cls):
        with cls._lock:  # lock_guard equivalent ->  lock_guard<mutex> lock(mtx); 
            if cls._instance is None:
                cls._instance = cls()
        return cls._instance


# Simulating usage
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
Output: 
    Constructor called
    Instance ID: 1967948391216
    Instance ID: 1967948391216
    Instance ID: 1967948391216
    Instance ID: 1967948391216
    Instance ID: 1967948391216

'''

'''
What is happening :

1. lets say we have 2 threads t1 and t2 trying to access the get_instance method at the same time.
2. t1 acquires the lock and checks if _instance is None. Since it is None, t1 proceeds to create a new instance of Singleton.
3. Meanwhile, t2 is waiting for the lock to be released. Once t1 finishes creating the instance and releases the lock, t2 acquires the lock and checks if _instance is None.
4. Since t1 has already created the instance, _instance is no longer None, and t2 simply returns the existing instance.
'''

'''
Problem we introduced with this approach is that we are locking the entire method, which can lead to performance issues if the get_instance method is called frequently. every time a thread wants to access the get_instance method, it has to acquire the lock, even if the instance has already been created. This can lead to contention and slow down the performance of the application.
'''

## solution is Double locking.