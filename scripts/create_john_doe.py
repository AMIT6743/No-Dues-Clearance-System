from backend.core.database import SessionLocal
from backend.models.user import User
from backend.core.security import get_password_hash

def create_fresh_student():
    db = SessionLocal()
    try:
        email = "john_doe@test.com"
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"User {email} already exists.")
            return
        
        user = User(
            name="John Doe",
            email=email,
            password=get_password_hash("password123"),
            role="STUDENT"
        )
        db.add(user)
        db.commit()
        print(f"User {email} created successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    create_fresh_student()
