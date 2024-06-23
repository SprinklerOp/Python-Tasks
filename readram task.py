import psutil

def read_ram():
    memory = psutil.virtual_memory()
    print("Total RAM:", memory.total)
    print("Available RAM:", memory.available)

read_ram()
