# defining a common interface for both file and folder classes. This interface will define the methods that both classes must implement, such as get_size() and get_structure().


from abc import ABC, abstractmethod


class FileSystemItem(ABC):

    @abstractmethod
    def ls(self, indent):
        pass

    @abstractmethod
    def open_all(self, indent):
        pass

    @abstractmethod
    def get_size(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

# File class that implements the FileSystemItem interface. It has name and size as attributes, and implements the methods defined in the interface.

class File(FileSystemItem):

    def __init__(self, name, size):
        self.name = name
        self.size = size

    def ls(self, indent): # here Indent is used to represent the level of nesting in the file system hierarchy. 
        print(" " * indent + self.name)

    def open_all(self, indent):
        print(" " * indent + self.name)

    def get_size(self):
        return self.size

    def get_name(self):
        return self.name

# Composite class that implements the FileSystemItem interface. It has a name and a list of children, which can be either files or folders. It implements the methods defined in the interface, and uses recursion to traverse the file system hierarchy.

class Folder(FileSystemItem):

    def __init__(self, name):
        self.name = name
        self.children : 'File | Folder' = []

    def add(self, item: FileSystemItem):
        self.children.append(item)

    def ls(self, indent):
        print(" " * indent + "+ " + self.name)
        for child in self.children:
            child.ls(indent + 4)

    def open_all(self, indent):
        print(" " * indent + "+ " + self.name)
        for child in self.children:
            child.open_all(indent + 4)

    def get_size(self):
        total = 0
        for child in self.children:
            # ✅ No type checking
            total += child.get_size()
        return total

    def get_name(self):
        return self.name



root = Folder("root")

root.add(File("file1.txt", 10))
root.add(File("file2.txt", 20))

docs = Folder("docs")
docs.add(File("resume.pdf", 30))
docs.add(File("notes.txt", 40))

images = Folder("images")
images.add(File("photo.jpg", 50))

root.add(docs)
root.add(images)

root.ls(0)

print("\nOpen All:\n")
root.open_all(0)

print("\nTotal Size:", root.get_size())