# Source: chapter-02-ai-boundaries.md
# Lines: 169-177
# Language: javascript

// 增加资源归属检查
if (resource === 'order') {
    const order = await Order.findById(req.params.id);
    if (order.userId.toString() !== req.userId && !user.isAdmin) {
        return res.status(403).json({ error: '无权访问此资源' });
    }
}
