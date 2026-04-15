# Source: chapter-02-ai-boundaries.md
# Lines: 147-155
# Language: javascript

// AI生成的权限检查
for (const perm of roleData.permissions) {
    if (perm.resource === resource && perm.action === action) {
        hasPermission = true;
        break;
    }
}
