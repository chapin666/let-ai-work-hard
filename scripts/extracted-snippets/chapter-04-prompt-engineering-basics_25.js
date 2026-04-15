# Source: chapter-04-prompt-engineering-basics.md
# Lines: 25-44
# Language: javascript

// AI生成的代码
function exportData(data) {
  const csv = convertToCSV(data);
  downloadFile(csv, 'export.csv');
}

function convertToCSV(data) {
  // ... CSV转换逻辑
}

function downloadFile(content, filename) {
  const blob = new Blob([content], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
}
