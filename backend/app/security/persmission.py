ROLE_PERMISSIONS = {
    "admin": {
        "user:read",
        "user:update",
        "user:delete",
        "user:list",
    },
    "user": {
        "user:read_self",
        "user:update_self"
    }
}