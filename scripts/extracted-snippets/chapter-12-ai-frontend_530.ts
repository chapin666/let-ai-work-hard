# Source: chapter-12-ai-frontend.md
# Lines: 530-540
# Language: typescript

// 你输入注释
// 创建一个带加载状态的按钮组件

// AI补全
const LoadingButton = ({ loading, children, ...props }: LoadingButtonProps) => (
  <Button disabled={loading} {...props}>
    {loading ? <Spinner size="sm" /> : children}
  </Button>
);
