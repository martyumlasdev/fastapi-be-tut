from fastapi_tutorial.core.rbac import sync_permissions
from fastapi_tutorial.db import SessionLocal
from fastapi_tutorial.models import Permission, Role, User
from fastapi_tutorial.security import get_password_hash

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


def seed_roles(db):
    """Create the initial application roles if they don't exist."""

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


def seed_admin_user(db, admin_role):
    """Create the initial admin account if it doesn't exist."""

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

        admin.roles.append(admin_role)
        db.flush()

    return admin


def seed_rbac() -> None:
    db = SessionLocal()

    try:
        permissions = sync_permissions(db)

        roles = seed_roles(db)

        assign_admin_permissions(
            roles["admin"],
            permissions,
        )

        admin = seed_admin_user(db, roles["admin"])

        db.commit()

        print("RBAC data seeded successfully.")
        print(f"Permissions discovered: {len(permissions)}")
        print(f"Roles: {len(roles)}")
        print(f"Admin: {admin.email}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def assign_admin_permissions(
    admin_role: Role,
    permissions: dict[str, Permission],
) -> None:
    existing_permissions = {
        permission.name
        for permission in admin_role.permissions
    }

    for permission in permissions.values():
        if permission.name not in existing_permissions:
            admin_role.permissions.append(permission)

if __name__ == "__main__":
    seed_rbac()