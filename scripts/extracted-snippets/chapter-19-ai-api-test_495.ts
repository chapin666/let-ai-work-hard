# Source: chapter-19-ai-api-test.md
# Lines: 495-510
# Language: typescript

// 基于契约的接口实现
app.get('/api/projects/:id', async (req, res) => {
  const project = await db.project.findById(req.params.id);
  if (!project) return res.status(404).json({ error: 'Not found' });
  
  // 确保返回格式符合契约
  res.json({
    id: project.id,
    name: project.name,
    description: project.description,
    visibility: project.visibility,
    memberCount: project.members.length,
  });
});
