# Source: chapter-02-ai-boundaries.md
# Lines: 32-58
# Language: javascript

// AI生成的代码开始
const mongoose = require('mongoose');

// 用户模型
const userSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    roles: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Role' }],
    createdAt: { type: Date, default: Date.now }
});

// 角色模型
const roleSchema = new mongoose.Schema({
    name: { type: String, required: true, unique: true },
    permissions: [{ type: mongoose.Schema.Types.ObjectId, ref: 'Permission' }],
    parent: { type: mongoose.Schema.Types.ObjectId, ref: 'Role', default: null }
});

// 权限模型
const permissionSchema = new mongoose.Schema({
    name: { type: String, required: true },
    resource: { type: String, required: true },
    action: { type: String, required: true }  // create, read, update, delete
});
