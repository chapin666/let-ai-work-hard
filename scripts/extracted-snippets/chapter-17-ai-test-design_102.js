# Source: chapter-17-ai-test-design.md
# Lines: 102-174
# Language: javascript

describe('applyCoupon', () => {
  // 基础功能测试
  describe('basic functionality', () => {
    test('should return original price when no coupon', () => {
      expect(applyCoupon(100, null)).toBe(100);
      expect(applyCoupon(100, undefined)).toBe(100);
    });
    
    test('should return original price when coupon is invalid', () => {
      expect(applyCoupon(100, { valid: false })).toBe(100);
      expect(applyCoupon(100, { valid: false, type: 'percentage', value: 10 })).toBe(100);
    });
    
    test('should return original price when coupon has no type', () => {
      expect(applyCoupon(100, { valid: true })).toBe(100);
    });
  });
  
  // 百分比优惠券测试
  describe('percentage coupon', () => {
    test('should apply percentage discount correctly', () => {
      expect(applyCoupon(100, { valid: true, type: 'percentage', value: 10 })).toBe(90);
      expect(applyCoupon(100, { valid: true, type: 'percentage', value: 50 })).toBe(50);
      expect(applyCoupon(100, { valid: true, type: 'percentage', value: 100 })).toBe(0);
    });
    
    test('should handle edge cases for percentage', () => {
      expect(applyCoupon(0, { valid: true, type: 'percentage', value: 10 })).toBe(0);
      expect(applyCoupon(100, { valid: true, type: 'percentage', value: 0 })).toBe(100);
      expect(applyCoupon(100, { valid: true, type: 'percentage', value: 200 })).toBe(-100);
    });
    
    test('should handle decimal percentage', () => {
      expect(applyCoupon(100, { valid: true, type: 'percentage', value: 33.33 })).toBeCloseTo(66.67, 2);
    });
  });
  
  // 固定金额优惠券测试
  describe('fixed amount coupon', () => {
    test('should apply fixed discount correctly', () => {
      expect(applyCoupon(100, { valid: true, type: 'fixed', value: 20 })).toBe(80);
      expect(applyCoupon(100, { valid: true, type: 'fixed', value: 100 })).toBe(0);
    });
    
    test('should not return negative price', () => {
      expect(applyCoupon(50, { valid: true, type: 'fixed', value: 100 })).toBe(0);
      expect(applyCoupon(0, { valid: true, type: 'fixed', value: 10 })).toBe(0);
    });
    
    test('should handle zero discount', () => {
      expect(applyCoupon(100, { valid: true, type: 'fixed', value: 0 })).toBe(100);
    });
  });
  
  // 边界情况和异常输入
  describe('edge cases and invalid inputs', () => {
    test('should handle negative price', () => {
      expect(applyCoupon(-100, { valid: true, type: 'fixed', value: 50 })).toBe(0);
    });
    
    test('should handle very large numbers', () => {
      expect(applyCoupon(1e10, { valid: true, type: 'percentage', value: 10 })).toBe(9e9);
    });
    
    test('should handle malformed coupon objects', () => {
      expect(applyCoupon(100, {})).toBe(100);
      expect(applyCoupon(100, { type: 'percentage' })).toBe(100);
      expect(applyCoupon(100, { value: 10 })).toBe(100);
    });
  });
});
