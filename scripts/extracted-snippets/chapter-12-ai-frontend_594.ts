# Source: chapter-12-ai-frontend.md
# Lines: 594-612
# Language: typescript

// 模板（写一次）
export function createListPage<T, Q, F>(config: ListPageConfig<T, Q, F>) {
  return function ListPage() {
    // 通用逻辑：搜索、分页、弹窗
    // 通用UI：搜索栏、表格、操作按钮
    // 个性化部分通过config传入
  };
}

// 使用（每个页面只要5行配置）
export default createListPage({
  title: '用户管理',
  api: userApi,
  columns: [...],
  searchFields: [...],
  formFields: [...],
});
