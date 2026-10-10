from enum import StrEnum

from fastapi import HTTPException, status
from sqlalchemy.orm import DeclarativeBase, Session

from fastapi_tutorial.dependencies import CurrentUser
from fastapi_tutorial.models import Permission


class PermissionAction(StrEnum):
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


DEFAULT_ACTIONS = {
    PermissionAction.READ,
    PermissionAction.CREATE,
    PermissionAction.UPDATE,
    PermissionAction.DELETE,
}

RBAC_MANAGEMENT_PERMISSIONS = {
    "role_permission.assign",
    "user_role.assign",
}



def get_permission_names(
    resource: str,
    actions: set[PermissionAction] | None = None,
) -> list[str]:
    """
    Generate permission names for an RBAC resource.
    """
    actions = actions or DEFAULT_ACTIONS

    return [
        f"{resource}.{action.value}"
        for action in actions
    ]


def get_rbac_resources(
    base: type[DeclarativeBase],
) -> list[tuple[str, set[PermissionAction]]]:
    """
    Discover SQLAlchemy models that explicitly opt into RBAC.
    """
    resources = []

    for model in base.registry.mappers:
        cls = model.class_

        resource = getattr(
            cls,
            "__rbac_resource__",
            None,
        )

        if resource is None:
            continue

        actions = getattr(
            cls,
            "__rbac_actions__",
            DEFAULT_ACTIONS,
        )

        resources.append((resource, actions))

    return resources


def sync_permissions(db: Session) -> dict[str, Permission]:
    """
    Create missing permissions discovered from RBAC resources
    and RBAC management permissions.

    Existing permissions are never modified or deleted.
    Role-permission assignments are never changed.
    """
    from fastapi_tutorial import models
    from fastapi_tutorial.db import Base

    # Ensure all SQLAlchemy models have been imported.
    _ = models

    permission_names = {
        name
        for resource, actions in get_rbac_resources(Base)
        for name in get_permission_names(resource, actions)
    }

    permission_names.update(RBAC_MANAGEMENT_PERMISSIONS)

    permissions = {}

    for name in permission_names:
        permission = (
            db.query(Permission)
            .filter_by(name=name)
            .first()
        )

        if permission is None:
            permission = Permission(
                name=name,
                description=f"{name.replace('.', ' ').capitalize()}",
            )
            db.add(permission)

        permissions[name] = permission

    db.flush()

    return permissions


def require_permission(permission_name: str):
    def dependency(
        current_user: CurrentUser,
    ):
        for role in current_user.roles:
            for permission in role.permissions:
                if permission.name == permission_name:
                    return current_user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied",
        )

    return dependency