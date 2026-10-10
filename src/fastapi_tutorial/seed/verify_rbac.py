from sqlalchemy import select, text

from fastapi_tutorial.core.rbac import sync_permissions
from fastapi_tutorial.db import SessionLocal
from fastapi_tutorial.models import Role


def verify_rbac() -> bool:
    db = SessionLocal()

    try:
        # Discover the permissions registered by our models.
        expected_permissions = set(sync_permissions(db))

        # Load the admin role and its assigned permissions.
        admin_role = db.scalar(
            select(Role).where(Role.name == "admin")
        )

        if admin_role is None:
            print("ERROR: Admin role not found.")
            return False

        actual_permissions = {
            permission.name
            for permission in admin_role.permissions
        }

        missing = expected_permissions - actual_permissions
        extra = actual_permissions - expected_permissions

        print("=== RBAC Permission Verification ===")
        print(f"Discovered permissions: {len(expected_permissions)}")
        print(f"Admin permissions:      {len(actual_permissions)}")

        print("\nMissing permissions:")
        print(*(sorted(missing) or ["None"]), sep="\n")

        print("\nExtra permissions:")
        print(*(sorted(extra) or ["None"]), sep="\n")

        # Inspect the actual association-table rows.
        rows = db.execute(
            text("""
                SELECT p.name
                FROM role_permissions AS rp
                JOIN roles AS r ON r.id = rp.role_id
                JOIN permissions AS p ON p.id = rp.permission_id
                WHERE r.name = :role_name
                ORDER BY p.name
            """),
            {"role_name": "admin"},
        ).scalars().all()

        print(f"\nrole_permissions rows for admin: {len(rows)}")
        print(*(rows or ["None"]), sep="\n")

        success = not missing and not extra and (
            len(rows) == len(actual_permissions)
        )

        print(
            "\nRESULT:",
            "PASS" if success else "FAIL",
        )

        return success

    finally:
        # sync_permissions() may add missing Permission records.
        # This script verifies state without persisting changes.
        db.rollback()
        db.close()


if __name__ == "__main__":
    success = verify_rbac()
    raise SystemExit(0 if success else 1)