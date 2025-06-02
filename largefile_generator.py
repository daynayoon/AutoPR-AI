# largefile_generator.py
with open("largefile.py", "w") as f:
    for _ in range(10000):  
        f.write("print('Hello World')\n")
