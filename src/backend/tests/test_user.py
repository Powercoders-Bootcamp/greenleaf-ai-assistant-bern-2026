from core.security import hash_password
from models.user import user

user = user(
    email="test@company.com",
    password_hash=hash_password("123456"),
    role="Employee"
)