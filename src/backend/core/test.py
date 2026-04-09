# test.py
from security import create_access_token

print(create_access_token({"sub": "123"}))