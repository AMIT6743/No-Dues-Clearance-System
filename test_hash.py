from backend.core.security import verify_password
hash_str = "$2b$12$uPrNAhDeBKLp.9DoCvAdCeJfBjKH72qoDdDnXNuuAy4pyMO2QFBqq"
print("Is password?", verify_password("password", hash_str))
print("Is asmi123?", verify_password("asmi123", hash_str))
print("Is asmi?", verify_password("asmi", hash_str))
print("Is 123456?", verify_password("123456", hash_str))
