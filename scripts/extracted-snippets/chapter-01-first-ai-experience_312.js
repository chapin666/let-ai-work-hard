# Source: chapter-01-first-ai-experience.md
# Lines: 312-324
# Language: javascript

app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    const query = `SELECT * FROM users WHERE username='${username}' AND password='${password}'`;
    db.query(query, (err, results) => {
        if (results.length > 0) {
            res.json({ success: true });
        } else {
            res.status(401).json({ error: '登录失败' });
        }
    });
});
