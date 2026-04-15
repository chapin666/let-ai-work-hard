# Source: chapter-15-ai-code-review.md
# Lines: 86-94
# Language: javascript

// AI建议的改进
function calculateTotal(price, quantity) {
  if (typeof price !== 'number' || typeof quantity !== 'number') {
    throw new TypeError('price and quantity must be numbers');
  }
  return price * quantity;
}
