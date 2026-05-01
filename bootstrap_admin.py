from flask import Flask
from db import Base, engine, SessionLocal
from models import User, Role, UserRole

app = Flask(__name__)

@app.route("/bootstrap-admin")
def bootstrap_admin():
    db = SessionLocal()

    # 1. Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # 2. Check if admin role exists
    admin_role = db.query(Role).filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(name="admin")
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

    # 3. Check if admin user exists
    admin_email = "admin@hegay.ai"
    admin_user = db.query(User).filter_by(email=admin_email).first()

    if not admin_user:
        admin_user = User(email=admin_email)
        admin_user.set_password("Admin@162000@")
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

    # 4. Link admin user to admin role
    link = db.query(UserRole).filter_by(user_id=admin_user.id, role_id=admin_role.id).first()
    if not link:
        link = UserRole(user_id=admin_user.id, role_id=admin_role.id)
        db.add(link)
        db.commit()

    db.close()

    return "Admin user and role created successfully. REMOVE THIS ROUTE NOW."
