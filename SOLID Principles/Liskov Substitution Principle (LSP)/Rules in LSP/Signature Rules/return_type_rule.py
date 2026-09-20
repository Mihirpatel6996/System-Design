'''
Child can return same type or more specific type
(this is covariance)

'''

# return type rule --> child must return at least what parent promised to return. If parent returns a base class, child can return a derived class. This is called covariance.

# covariant --> child can return a more detailed version of the same thing. For example, if parent returns a base class, child can return a derived class.


# parent contract : returns a dictionary with a "content" key

class FileService:
    def read(self):
        return {"content": "data"}


# caller code 

def process(service: FileService):
    data = service.read()
    print(data["content"])

## this is important because the caller expects a dictionary with a "content" key. If the child class returns a different type, it will break the caller code.

# child - correct implementation : returns a derived class of dictionary
class LocalFileService(FileService):
    def read(self):
        return {
            "content": "file data",
            "size": 123   # extra info
        }

# run it 
process(LocalFileService())  # works fine, returns a dictionary with "content" key

'''
why it works :
Because parent promised to return a dictionary with a "content" key.
and child returned a dictionary with a "content" key and an extra "size" key. This is allowed because the child returned a more specific type (a dictionary with extra information) while still fulfilling the contract of the parent class.
'''

## Violation Example (Returning a Different Type)

class BadFileService(FileService):
    def read(self):
        return "file data"   #  changed type

# run 
process(BadFileService())  #  breaks, returns a string instead of a dictionary

'''
Final intuition (this is the one I have to remember)

Parent defines the minimum guarantee
Child can give more, but never less or different

Covariance --> “Return something more detailed, not something unrelated”
'''