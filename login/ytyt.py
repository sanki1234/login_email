a=5

def g():
    global a
    a=6
    print(a)

g()
print(a)