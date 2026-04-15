# Source: chapter-01-first-ai-experience.md
# Lines: 251-264
# Language: javascript

app.post('/api/register', async (req, res) => {
    const { username, email, password } = req.body;
    // 检查用户是否存在
    const existingUser = await User.findOne({ $or: [{ username }, { email }] });
    if (existingUser) {
        return res.status(400).json({ error: '用户已存在' });
    }
    // 创建新用户
    const user = new User({ username, email, password });
    await user.save();
    res.json({ message: '注册成功' });
});
