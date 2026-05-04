from backend.core.database import SessionLocal
from backend.models.user import User
from backend.models.department import Department
from backend.core.security import get_password_hash

def create_department_managers():
    db = SessionLocal()
    try:
        departments = db.query(Department).all()
        created_users = []
        
        for dept in departments:
            # Create a clean email from department name
            clean_name = "".join(e for e in dept.name.lower() if e.isalnum())
            email = f"{clean_name}@college.edu"
            
            existing = db.query(User).filter(User.email == email).first()
            if existing:
                # Update existing user to be department manager for this department
                existing.role = "DEPARTMENT"
                existing.department_id = dept.id
                db.commit()
                created_users.append((dept.name, email, "password123"))
                continue
            
            user = User(
                name=f"{dept.name.title()} Manager",
                email=email,
                password=get_password_hash("password123"),
                role="DEPARTMENT",
                department_id=dept.id
            )
            db.add(user)
            db.commit()
            created_users.append((dept.name, email, "password123"))
        
        print("Department Managers Created:")
        for dept_name, email, pw in created_users:
            print(f"Department: {dept_name} | Email: {email} | Password: {pw}")
            
    finally:
        db.close()

if __name__ == "__main__":
    create_department_managers()
