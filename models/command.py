import os

try:
    os.remove("index.html")
    os.remove("buy.html")
except FileNotFoundError:
    pass 
