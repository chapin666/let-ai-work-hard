# Source: chapter-20-ai-security-test.md
# Lines: 52-61
# Language: javascript

// 存在SQL注入的代码
app.get('/api/users', async (req, res) => {
  const { keyword } = req.query;
  // 危险！直接拼接SQL
  const sql = `SELECT * FROM users WHERE name LIKE '%${keyword}%'`;
  const users = await db.query(sql);
  res.json(users);
});
