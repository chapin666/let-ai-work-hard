# Source: chapter-37-ai-harness-platform.md
# Lines: 284-292
# Language: typescript

function canViewOrder(user: User, order: Order): boolean {
  if (user.role === 'admin') return true;
  if (user.role === 'customer_service') {
    return order.assignedTo === user.id;
  }
  return order.userId === user.id;
}
