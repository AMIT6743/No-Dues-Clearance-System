from backend.core.database import SessionLocal
from backend.models.user import User
from backend.models.clearance import ClearanceRequest, DepartmentApproval

def approve_all_for_john_doe():
    db = SessionLocal()
    try:
        email = "john_doe@test.com"
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"User {email} not found.")
            return
        
        request = db.query(ClearanceRequest).filter(ClearanceRequest.student_id == user.id).order_by(ClearanceRequest.id.desc()).first()
        if not request:
            print(f"No request found for {email}.")
            return
        
        # Approve all department approvals
        approvals = db.query(DepartmentApproval).filter(DepartmentApproval.request_id == request.id).all()
        for app in approvals:
            app.status = "APPROVED"
        
        # Update main request status
        request.status = "APPROVED"
        
        db.commit()
        print(f"All departments approved and request #{request.id} finalized for {email}.")
    finally:
        db.close()

if __name__ == "__main__":
    approve_all_for_john_doe()
