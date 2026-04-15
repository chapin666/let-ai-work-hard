# Source: chapter-20-ai-security-test.md
# Lines: 842-863
# Language: javascript

// SQL注入 ❌
db.query(`SELECT * FROM users WHERE id = ${userId}`);
// ✅ 修复
db.query('SELECT * FROM users WHERE id = ?', [userId]);

// XSS ❌
element.innerHTML = userInput;
// ✅ 修复
element.textContent = userInput;

// 越权 ❌
const data = await db.findById(id);
// ✅ 修复
const data = await db.findOne({ id, userId: currentUser.id });

// 敏感信息泄露 ❌
res.json({ user, password: hashedPassword });
// ✅ 修复
const { password, ...safeUser } = user;
res.json({ user: safeUser });
