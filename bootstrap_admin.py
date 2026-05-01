from flask import jsonify
from db import Base, engine, SessionLocal
from models import User, Role, UserRole
import bcrypt

# Create all tables
Base.metadata.create_all(bind=engine)

def create_admin():
    db = SessionLocal()

    # 1. Ensure admin role exists
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
        admin_role = Role(name="admin")
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

    # 2. Ensure admin user exists
    admin_user = db.query(User).filter(User.email == "admin@hegay.ai").first()
    if not admin_user:
        admin_user = User(
            email="admin@hegay.ai",
            password_hash=bcrypt.hashpw("Admin@162000@".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        # 3. Link admin user to admin role
        link = UserRole(user_id=admin_user.id, role_id=admin_role.id)
        db.add(link)
        db.commit()

    db.close()


def register_bootstrap_route(app):
    @app.route("/bootstrap-admin", methods=["GET"])
    def bootstrap_admin_route():
        create_admin()
        return jsonify({"status": "success", "message": "Admin bootstrap complete"})
