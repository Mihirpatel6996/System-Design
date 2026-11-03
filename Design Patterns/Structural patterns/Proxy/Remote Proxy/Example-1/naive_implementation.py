import time


class RealDataService:
    def __init__(self):
        print("[RealDataService] Connecting to remote server...")
        time.sleep(2)

    def fetch_data(self):
        print("[RealDataService] Fetching data from server...")
        time.sleep(2)
        return "DATA_FROM_SERVER"


# client code 

if __name__ == "__main__":
    print("Creating RealDataService object...\n")
    service = RealDataService()

    print("\nFetching data from server...\n")
    data = service.fetch_data()
    print(f"Received: {data}")

"""
problem here:

1. Client knows too much
    - It knows it's calling a remote service
2. No control layer
    You cannot:
        - retry
        - cache
        - log
        - handle failures
3. No abstraction
    If tomorrow service becomes HTTP-based, everything breaks
"""

