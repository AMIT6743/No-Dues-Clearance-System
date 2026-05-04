from backend.core.database import SessionLocal
from backend.models.user import User
from backend.core.security import get_password_hash

def create_student():
    db = SessionLocal()
    try:
        email = "student@test.com"
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"User {email} already exists.")
            return
        
        user = User(
            name="Test Student",
            email=email,
            password=get_password_hash("password"),
            role="STUDENT"
        )
        db.add(user)
        db.commit()
        print(f"User {email} created successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    create_student()
