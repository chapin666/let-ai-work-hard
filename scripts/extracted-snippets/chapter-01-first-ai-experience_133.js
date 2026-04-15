# Source: chapter-01-first-ai-experience.md
# Lines: 133-135
# Language: javascript

const compose = (...fns) => fns.reduceRight((f, g) => (...args) => f(g(...args)));
