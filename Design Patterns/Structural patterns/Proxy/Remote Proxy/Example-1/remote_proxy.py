from abc import ABC, abstractmethod
import time


class IDataService(ABC):

    @abstractmethod
    def fetch_data(self):
        pass


class RealDataService(IDataService):

    def __init__(self):
        print("[RealDataService] Remote service initialized")

    def fetch_data(self):
        print("[RealDataService] Processing request on server...")
        time.sleep(2)
        return "[RealDataService] Data from server"

# Remote Proxy Layer

class DataServiceProxy(IDataService):

    def __init__(self):
        # could also be lazy (virtual + remote combo)
        self.real_service = RealDataService()

    def fetch_data(self):
        print("[Proxy] Opening network connection...")
        
        # simulate network latency
        time.sleep(1)

        print("[Proxy] Sending request to remote server...")

        response = self.real_service.fetch_data()

        print("[Proxy] Received response")

        return response


if __name__ == "__main__":

    service: IDataService = DataServiceProxy()

    result = service.fetch_data()

    print(result)

    




