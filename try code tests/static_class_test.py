class C1():
    # it is not static field, it is just class field
    static_field = 10

o = C1()
o.static_field += 1

print(o.static_field)
print(C1.static_field)

