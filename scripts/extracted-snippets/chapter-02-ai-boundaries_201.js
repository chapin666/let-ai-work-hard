# Source: chapter-02-ai-boundaries.md
# Lines: 201-218
# Language: javascript

// AI生成的认证中间件
const authenticate = async (req, res, next) => {
    try {
        const token = req.headers.authorization?.split(' ')[1];
        if (!token) {
            return res.status(401).json({ error: '未提供token' });
        }
        
        // 致命问题在这里！
        const decoded = jwt.decode(token);  // 只用了decode，没有用verify！
        req.userId = decoded.userId;
        next();
    } catch (error) {
        res.status(401).json({ error: '认证失败' });
    }
};
