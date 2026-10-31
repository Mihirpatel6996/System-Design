import time

class IImage:
    def display(self):
        raise NotImplementedError


class RealImage(IImage):
    def __init__(self, filename: str):
        self.filename = filename
        self._load_from_disk()

    def _load_from_disk(self):
        print(f"[RealImage] Loading image from disk: {self.filename}")
        time.sleep(2)  # simulate heavy IO

    def display(self):
        print(f"[RealImage] Displaying {self.filename}")


# ---- Client Code ----
if __name__ == "__main__":
    print("Creating images...")

    image1 = RealImage("scan1.jpg")
    image2 = RealImage("scan2.jpg")
    image3 = RealImage("scan3.jpg")

    print("Images created.\n")

    # user only views one image
    image1.display()


"""
Exectuion Output:

Creating images...

[RealImage] Loading scan1.jpg  (2 sec)
[RealImage] Loading scan2.jpg  (2 sec)
[RealImage] Loading scan3.jpg  (2 sec)

Images created.

then :  [RealImage] Displaying scan1.jpg


"""

"""
Problems Identified :


users only used or called display for 1 image but all 3 images were loaded from disk which is a waste of time and resources.
slow startup time for the application because of loading all images at once.
memory pressure because of loading all images at once and never using it really
no control over when cost happens 


"""