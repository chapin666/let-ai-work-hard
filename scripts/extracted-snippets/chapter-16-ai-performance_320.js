# Source: chapter-16-ai-performance.md
# Lines: 320-372
# Language: javascript

// dataProcessor.worker.js
self.onmessage = function(e) {
  const { type, payload, id } = e.data;
  
  if (type === 'PROCESS_DATA') {
    try {
      const result = processData(payload);
      self.postMessage({ type: 'SUCCESS', result, id });
    } catch (error) {
      self.postMessage({ type: 'ERROR', error: error.message, id });
    }
  }
};

function processData({ data, filters, sortConfig }) {
  let result = [...data];
  
  // 筛选
  if (filters) {
    result = result.filter(item => {
      return Object.entries(filters).every(([key, value]) => {
        if (!value) return true;
        return item[key]?.toString().toLowerCase().includes(value.toLowerCase());
      });
    });
  }
  
  // 排序
  if (sortConfig) {
    result.sort((a, b) => {
      for (const { key, direction } of sortConfig) {
        const comparison = a[key] > b[key] ? 1 : a[key] < b[key] ? -1 : 0;
        if (comparison !== 0) {
          return direction === 'desc' ? -comparison : comparison;
        }
      }
      return 0;
    });
  }
  
  // 计算聚合值
  const aggregates = {
    total: result.length,
    sum: result.reduce((acc, item) => acc + (item.amount || 0), 0),
    average: result.length > 0 
      ? result.reduce((acc, item) => acc + (item.amount || 0), 0) / result.length 
      : 0
  };
  
  return { data: result, aggregates };
}
