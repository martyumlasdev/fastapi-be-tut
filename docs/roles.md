| Concern | Decision |
|---|---|
| User ↔ Role | Many-to-many |
| Role ↔ Permission | Many-to-many |
| Association tables | `user_roles`, `role_permissions` |
| Association PK | Composite primary key |
| Role name | Unique + NOT NULL |
| Permission name | Unique + NOT NULL |
| FK deletion | `ON DELETE CASCADE` |
| ORM entity deletion cascade | None |
| User deletion | Removes role associations only |
| Role deletion | Removes user/permission associations only |
| Permission deletion | Removes role associations only |
| Extra indexes | None initially |
| Loading strategy | Default for now |


                         ┌──────────────┐
                         │     User     │
                         └──────┬───────┘
                                │
                         user_roles
                                │
                                ▼
                         ┌──────────────┐
                         │     Role     │
                         └──────┬───────┘
                                │
                      role_permissions
                                │
                                ▼
                       ┌────────────────┐
                       │   Permission   │
                       └────────────────┘


                       Application Code
                            │
                            │ defines capabilities
                            ▼
                        Permissions
                            │
                            │ grouped by
                            ▼
                        Roles ←──── Admin API/UI
                            │
                            │ assigned to
                            ▼
                        Users