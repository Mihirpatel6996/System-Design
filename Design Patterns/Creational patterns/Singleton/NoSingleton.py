class NoSingleton:
    def __init__(self):
        print("Constructor called. New object created.")


# Simulating main()
s1 = NoSingleton()
s2 = NoSingleton()

print("Are both objects same?", s1 is s2)


'''
Output :

Constructor called. New object created.
Constructor called. New object created.
Are both objects same? False
'''