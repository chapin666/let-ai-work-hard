# Source: chapter-18-ai-automation-test.md
# Lines: 442-463
# Language: javascript

// scripts/analyze-test-failures.js
const { analyzeTestFailure } = require('./ai-helper');

async function main() {
  const failures = await getRecentFailures();
  
  for (const failure of failures) {
    const analysis = await analyzeTestFailure({
      errorMessage: failure.message,
      stackTrace: failure.stack,
      testCode: failure.testCode,
      componentCode: failure.componentCode,
    });
    
    console.log(`\n失败测试: ${failure.testName}`);
    console.log(`可能原因: ${analysis.rootCause}`);
    console.log(`修复建议: ${analysis.suggestion}`);
    console.log(`置信度: ${analysis.confidence}%`);
  }
}
