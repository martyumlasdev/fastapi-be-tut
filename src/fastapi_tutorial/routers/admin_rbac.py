from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from fastapi_tutorial.core.rbac import require_permission
from fastapi_tutorial.dependencies import CurrentUser, DBSession
from fastapi_tutorial.models import Permission, Role, User

router = APIRouter(
    prefix="/admin/roles",
    tags=["Admin - RBAC"],
)


@router.post(
    "/{role_id}/permissions/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_permission("role_permission.assign"))
    ],
)
def assign_permission_to_role(
    role_id: int,
    permission_id: int,
    db: DBSession,
) -> None:
    role = db.get(Role, role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    permission = db.get(Permission, permission_id)
    if permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found",
        )

    if permission not in role.permissions:
        role.permissions.append(permission)
        db.commit()



@router.delete(
    "/{role_id}/permissions/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_permission("role_permission.assign"))
    ],
)
def remove_permission_from_role(
    role_id: int,
    permission_id: int,
    db: DBSession,
) -> None:
    role = db.get(Role, role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    permission = db.get(Permission, permission_id)
    if permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found",
        )

    if permission in role.permissions:
        role.permissions.remove(permission)
        db.commit()



@router.post(
    "/users/{user_id}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_permission("user_role.assign"))
    ],
)
def assign_role_to_user(
    user_id: int,
    role_id: int,
    db: DBSession,
) -> None:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    role = db.get(Role, role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    if role not in user.roles:
        user.roles.append(role)
        db.commit()


@router.delete(
    "/users/{user_id}/roles/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_permission("user_role.assign"))
    ],
)
def remove_role_from_user(
    user_id: int,
    role_id: int,
    db: DBSession,
) -> None:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    role = db.get(Role, role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    if role in user.roles:
        user.roles.remove(role)
        db.commit()

@router.get(
    "/",
    dependencies=[Depends(require_permission("role.read"))],
)
def list_roles(db: DBSession):
    roles = db.query(Role).order_by(Role.id).all()

    return [
        {
            "id": role.id,
            "name": role.name,
            "description": role.description,
            "permissions": [
                {
                    "id": permission.id,
                    "name": permission.name,
                    "description": permission.description,
                }
                for permission in role.permissions
            ],
        }
        for role in roles
    ]


@router.get(
    "/permissions",
    dependencies=[Depends(require_permission("permission.read"))],
)
def list_permissions(db: DBSession):
    permissions = (
        db.query(Permission)
        .order_by(Permission.name)
        .all()
    )

    return [
        {
            "id": permission.id,
            "name": permission.name,
            "description": permission.description,
        }
        for permission in permissions
    ]


@router.get(
    "/users",
    dependencies=[Depends(require_permission("user.read"))],
)
def list_users(db: DBSession):
    users = db.query(User).order_by(User.id).all()

    return [
        {
            "id": user.id,
            "email": user.email,
            "roles": [
                {
                    "id": role.id,
                    "name": role.name,
                }
                for role in user.roles
            ],
        }
        for user in users
    ]