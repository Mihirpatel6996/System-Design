class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def get_size(self):
        return self.size

    def get_name(self):
        return self.name

    # A file class that has name and size as attributes, and a getter to return the file size and name of the file. 


class Folder:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add(self, item: 'File | Folder' ):
        self.children.append(item)

    def get_size(self):
        total = 0
        for item in self.children:
            #  Type checking everywhere
            if isinstance(item, File):
                total += item.get_size()
            elif isinstance(item, Folder):
                total += item.get_size()
        return total
    
    def get_structure(self, indent=0):
        structure = "  " * indent + f"Folder: {self.name}\n"
        for item in self.children:
            if isinstance(item, File):
                structure += "  " * (indent + 1) + f"File: {item.get_name()} (Size: {item.get_size()} bytes)\n"
            elif isinstance(item, Folder):
                structure += item.get_structure(indent + 1)
        return structure

#problems in the above code

"""
file and folder are 2 different classes and they are not related to each other.
code duplication everytime to check if it is a file or folder. --> type awarenedd everywhere
adding new type in the code breaks the existing code. --> open close principle is violated

"""

root = Folder("root")
root.add(File("a.txt", 10))
root.add(File("b.txt", 20))

sub_folder = Folder("subfolder")
sub_folder.add(File("c.txt", 30))
root.add(sub_folder)

print(root.get_size())  # 60
print(root.get_structure())

"""
That is why we need to use composite design pattern. Composite design pattern allows us to treat individual objects and compositions of objects uniformly. In this case, we can create a common interface for both File and Folder, allowing us to avoid type checking and code duplication. so we can create a common interface called "FileSystemItem" that both File and Folder will implement. This interface will define the methods that both classes must implement, such as get_size() and get_structure().
"""
