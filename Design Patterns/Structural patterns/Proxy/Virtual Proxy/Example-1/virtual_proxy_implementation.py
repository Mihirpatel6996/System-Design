import time


class IImage:
    def display(self):
        raise NotImplementedError


# ----------------------------
# REAL OBJECT (heavy)
# ----------------------------
class RealImage(IImage):
    def __init__(self, filename: str):
        self.filename = filename
        self._load_from_disk()

    def _load_from_disk(self):
        print(f"[RealImage] Loading image from disk: {self.filename}")
        time.sleep(2)  # simulate heavy IO

    def display(self):
        print(f"[RealImage] Displaying {self.filename}")


# Virtual Proxy Layer

class ImageProxy(IImage):
    def __init__(self, filename: str):
        self.filename = filename
        self._real_image = None  # important: NOT created yet

    def display(self):
        # lazy initialization happens here
        if self._real_image is None:
            print("[Proxy] RealImage not created yet. Creating now...")
            self._real_image = RealImage(self.filename)

        self._real_image.display()

# ---- Client Code ----

if __name__ == "__main__":
    print("Creating proxy objects only...\n")

    image1 = ImageProxy("scan1.jpg")
    image2 = ImageProxy("scan2.jpg")
    image3 = ImageProxy("scan3.jpg")

    print("\nNo image loaded yet!\n")

    print("User opens only one image:\n")
    image1.display()