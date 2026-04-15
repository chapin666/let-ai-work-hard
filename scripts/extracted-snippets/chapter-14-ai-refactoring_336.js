# Source: chapter-14-ai-refactoring.md
# Lines: 336-363
# Language: javascript

// gateway.js - API网关
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

// 新系统已完成的模块
const newSystemModules = [
  '/api/v2/orders',      // 新订单模块
  '/api/v2/users',       // 新用户模块
];

// 路由中间件
app.use((req, res, next) => {
  const isNewModule = newSystemModules.some(prefix =>
    req.path.startsWith(prefix)
  );

  if (isNewModule) {
    // 路由到新系统（NestJS）
    proxyToNewSystem(req, res, next);
  } else {
    // 路由到旧系统（PHP）
    proxyToOldSystem(req, res, next);
  }
});
