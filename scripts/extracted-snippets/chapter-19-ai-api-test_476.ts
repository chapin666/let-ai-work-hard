# Source: chapter-19-ai-api-test.md
# Lines: 476-492
# Language: typescript

// 基于契约的类型定义
interface Project {
  id: number;
  name: string;
  description?: string;
  visibility: 'public' | 'private' | 'internal';
  memberCount: number;
}

// API调用
const getProject = async (id: number): Promise<Project> => {
  const response = await fetch(`/api/projects/${id}`);
  if (!response.ok) throw new Error('Failed to fetch project');
  return response.json();
};
