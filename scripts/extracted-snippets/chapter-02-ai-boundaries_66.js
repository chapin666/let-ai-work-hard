# Source: chapter-02-ai-boundaries.md
# Lines: 66-99
# Language: javascript

// 权限检查中间件
const checkPermission = (resource, action) => {
    return async (req, res, next) => {
        try {
            const user = await User.findById(req.userId).populate('roles');
            if (!user) {
                return res.status(401).json({ error: '用户未登录' });
            }
            
            // 检查用户是否有权限
            let hasPermission = false;
            for (const role of user.roles) {
                const roleData = await Role.findById(role).populate('permissions');
                for (const perm of roleData.permissions) {
                    if (perm.resource === resource && perm.action === action) {
                        hasPermission = true;
                        break;
                    }
                }
                if (hasPermission) break;
            }
            
            if (!hasPermission) {
                return res.status(403).json({ error: '没有权限' });
            }
            
            next();
        } catch (error) {
            res.status(500).json({ error: '权限检查失败' });
        }
    };
};
