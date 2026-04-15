# Source: chapter-01-first-ai-experience.md
# Lines: 267-276
# Language: javascript

app.post('/api/login', async (req, res) => {
    const { username, password } = req.body;
    const user = await User.findOne({ username });
    if (!user || user.password !== password) {
        return res.status(401).json({ error: '用户名或密码错误' });
    }
    // 生成token...
});
