from fastapi_tutorial.core.security import get_password_hash

from fastapi_tutorial.core.permissions import PERMISSIONS
from fastapi_tutorial.db import SessionLocal
from fastapi_tutorial.models import Permission, Role, User

INITIAL_ROLES = {
    "user": "Regular application user",
    "admin": "System administrator",
}


ADMIN_USER = {
    "first_name": "Admin",
    "last_name": "User",
    "email": "admin@example.com",
    "password": "password",
}


def seed_permissions(db):
    """Create application permissions that don't exist yet."""

    permissions = {}

    for name, description in PERMISSIONS.items():
        permission = (
            db.query(Permission)
            .filter_by(name=name)
            .first()
        )

        if permission is None:
            permission = Permission(
                name=name,
                description=description,
            )
            db.add(permission)

        permissions[name] = permission

    db.flush()

    return permissions


def seed_roles(db):
    """Create the initial application roles."""

    roles = {}

    for name, description in INITIAL_ROLES.items():
        role = (
            db.query(Role)
            .filter_by(name=name)
            .first()
        )

        if role is None:
            role = Role(
                name=name,
                description=description,
            )
            db.add(role)

        roles[name] = role

    db.flush()

    return roles


def seed_admin_permissions(db, roles, permissions):
    """Give the initial admin role all known permissions."""

    admin_role = roles["admin"]

    for permission in permissions.values():
        if permission not in admin_role.permissions:
            admin_role.permissions.append(permission)

    db.flush()


def seed_admin_user(db, admin_role):
    """Create the initial admin account."""

    admin = (
        db.query(User)
        .filter_by(email=ADMIN_USER["email"])
        .first()
    )

    if admin is None:
        admin = User(
            first_name=ADMIN_USER["first_name"],
            last_name=ADMIN_USER["last_name"],
            email=ADMIN_USER["email"],
            password_hash=get_password_hash(
                ADMIN_USER["password"]
            ),
        )

        db.add(admin)
        db.flush()

    if admin_role not in admin.roles:
        admin.roles.append(admin_role)

    db.flush()

    return admin


def seed_rbac() -> None:
    db = SessionLocal()

    try:
        permissions = seed_permissions(db)

        roles = seed_roles(db)

        seed_admin_permissions(
            db,
            roles,
            permissions,
        )

        admin = seed_admin_user(
            db,
            roles["admin"],
        )

        db.commit()

        print("RBAC data seeded successfully.")
        print(f"Permissions: {len(permissions)}")
        print(f"Roles: {len(roles)}")
        print(f"Admin: {admin.email}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_rbac()