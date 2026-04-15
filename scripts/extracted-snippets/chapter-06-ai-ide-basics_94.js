# Source: chapter-06-ai-ide-basics.md
# Lines: 94-117
# Language: javascript

const checkPermission = (requiredPermission) => {
  return async (req, res, next) => {
    try {
      const user = await User.findById(req.userId).populate({
        path: 'roles',
        populate: { path: 'permissions' }
      });
      
      const hasPermission = user.roles.some(role =>
        role.permissions.some(perm => perm.code === requiredPermission)
      );
      
      if (!hasPermission) {
        return res.status(403).json({ error: '没有权限' });
      }
      
      next();
    } catch (error) {
      res.status(500).json({ error: '权限检查失败' });
    }
  };
};
