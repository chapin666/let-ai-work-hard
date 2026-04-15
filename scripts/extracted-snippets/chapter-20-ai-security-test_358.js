# Source: chapter-20-ai-security-test.md
# Lines: 358-369
# Language: javascript

app.get('/api/orders/:id', async (req, res) => {
  const { id } = req.params;
  const order = await db.orders.findById(id);
  
  if (!order) {
    return res.status(404).json({ error: 'Order not found' });
  }
  
  res.json(order);
});
