# Source: chapter-01-first-ai-experience.md
# Lines: 302-306
# Language: javascript

const existingUser = await User.findOne({ 
    $or: [{ username }, { email }] 
});
