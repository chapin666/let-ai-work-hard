# Source: chapter-18-ai-automation-test.md
# Lines: 676-695
# Language: javascript

// scripts/fix-tests.js
const { fixTestFile } = require('./ai-helper');
const glob = require('glob');

async function main() {
  const files = glob.sync('**/*.test.{js,ts}');
  
  for (const file of files) {
    console.log(`处理: ${file}`);
    const content = fs.readFileSync(file, 'utf-8');
    const fixed = await fixTestFile(content, {
      fixSelectors: true,
      fixAsync: true,
      addComments: true,
    });
    fs.writeFileSync(file, fixed);
  }
}
