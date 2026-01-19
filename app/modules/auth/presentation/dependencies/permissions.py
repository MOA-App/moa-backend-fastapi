def require_permission(permission: str):
    async def dependency():
        _ = permission  # usado intencionalmente (stub)
        return None
    return dependency
