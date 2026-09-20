# A child class must NOT throw broader or unexpected exceptions than the parent

# when a caller writes 

# try:
#     service.do_something()
# except SomeExpectedError:
#     handle()

'''
The caller is making an assumption:

“Only this type of failure will happen”

If the child breaks that assumption → system breaks.
'''

#Example:

# parent class
class FileService:
    def read(self):
        raise FileNotFoundError("File missing")

def process(service: FileService):
    try:
        service.read()
    except FileNotFoundError:
        print("Handled missing file")

# this works fine because the caller expects a FileNotFoundError and handles it.

process(FileService())  # works fine

# now child breaks the rule 
class BadFileService(FileService):
    def read(self):
        raise Exception("Something random")   #  broader exception

# this will crash 
process(BadFileService())  #  breaks, raises Exception instead of FileNotFoundError

# reason -> expecting file not found error, but got a generic exception. 

# this is violation -> parent said only file not found error will happen, but child said anything can happen. This breaks the caller's assumption and violates LSP.

    

