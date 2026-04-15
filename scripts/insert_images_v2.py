#!/usr/bin/env python3
"""
智能插入图片到各章节
在章节的故事部分之后、理论部分之前插入图片
"""
import re
from pathlib import Path

CHAPTERS_DIR = Path("/root/.openclaw/workspace/let-ai-work-hard/chapters")

# 章节图片配置：文件名 -> [(图片路径, 图片标题), ...]
CHAPTER_IMAGES = {
    "chapter-03-tool-selection.md": [
        ("../images/chapter-03-tool-selection-flow.svg", "AI工具选型决策流程"),
        ("../images/chapter-03-tools-compare.svg", "主流AI编程工具对比"),
    ],
    "chapter-04-prompt-engineering-basics.md": [
        ("../images/chapter-04-rpct-framework.svg", "RPCT提示框架"),
        ("../images/chapter-04-prompt-structure.svg", "高质量Prompt构建流程"),
    ],
    "chapter-05-cot-structured-output.md": [
        ("../images/chapter-05-cot-comparison.svg", "思维方式对比"),
        ("../images/chapter-05-structured-output.svg", "结构化输出工作流程"),
    ],
    "chapter-06-ai-ide-basics.md": [
        ("../images/chapter-06-agent-architecture.svg", "Cursor Agent模式架构"),
    ],
    "chapter-07-ai-ide-advanced.md": [
        ("../images/chapter-07-advanced-workflow.svg", "复杂项目AI协作流程"),
    ],
    "chapter-08-ai-writing-blog.md": [
        ("../images/chapter-08-blog-workflow.svg", "AI辅助博客写作流程"),
    ],
    "chapter-09-ai-writing-booklet.md": [
        ("../images/chapter-09-booklet-workflow.svg", "AI辅助小册出版流程"),
    ],
    "chapter-10-ai-speaking.md": [
        ("../images/chapter-10-speaking-workflow.svg", "AI辅助演讲准备流程"),
    ],
    "chapter-11-ai-learning.md": [
        ("../images/chapter-11-learning-system.svg", "AI辅助学习系统"),
    ],
    "chapter-12-ai-frontend.md": [
        ("../images/chapter-12-frontend-workflow.svg", "AI辅助前端开发流程"),
    ],
    "chapter-13-ai-backend.md": [
        ("../images/chapter-13-backend-workflow.svg", "AI辅助后端开发流程"),
    ],
    "chapter-14-ai-refactoring.md": [
        ("../images/chapter-14-refactoring-flow.svg", "代码重构决策流程"),
    ],
    "chapter-15-ai-code-review.md": [
        ("../images/chapter-15-review-dimensions.svg", "代码审查维度"),
    ],
    "chapter-16-ai-performance.md": [
        ("../images/chapter-16-performance-flow.svg", "AI辅助性能优化流程"),
    ],
    "chapter-17-ai-test-design.md": [
        ("../images/chapter-17-test-design.svg", "AI辅助测试设计流程"),
    ],
    "chapter-18-ai-automation-test.md": [
        ("../images/chapter-18-automation-arch.svg", "自动化测试架构"),
    ],
    "chapter-19-ai-api-test.md": [
        ("../images/chapter-19-api-test-flow.svg", "API测试流程"),
    ],
    "chapter-20-ai-security-test.md": [
        ("../images/chapter-20-security-flow.svg", "安全测试流程"),
    ],
    "chapter-21-ai-sql-optimization.md": [
        ("../images/chapter-21-sql-optimization.svg", "AI辅助SQL优化流程"),
    ],
    "chapter-22-ai-scripting.md": [
        ("../images/chapter-22-scripting-workflow.svg", "脚本自动化开发流程"),
    ],
    "chapter-23-ai-docker.md": [
        ("../images/chapter-23-docker-workflow.svg", "Docker容器化流程"),
    ],
    "chapter-24-ai-cicd.md": [
        ("../images/chapter-24-cicd-architecture.svg", "CI/CD流水线架构"),
    ],
    "chapter-25-ai-monitoring.md": [
        ("../images/chapter-25-observability.svg", "可观测性三大支柱"),
    ],
    "chapter-26-ai-data-analysis.md": [
        ("../images/chapter-26-data-analysis.svg", "数据分析工作流程"),
    ],
    "chapter-27-ai-requirements.md": [
        ("../images/chapter-27-requirements-flow.svg", "AI辅助需求分析流程"),
    ],
    "chapter-28-ai-tech-decision.md": [
        ("../images/chapter-28-tech-decision.svg", "技术选型评估维度"),
    ],
    "chapter-29-ai-project-management.md": [
        ("../images/chapter-29-project-management.svg", "项目管理流程优化"),
    ],
    "chapter-30-ai-team-collab.md": [
        ("../images/chapter-30-team-collab.svg", "团队协作架构"),
    ],
    "chapter-31-ai-knowledge.md": [
        ("../images/chapter-31-knowledge-workflow.svg", "知识库建设流程"),
    ],
    "chapter-32-ai-pm-workflow.md": [
        ("../images/chapter-32-priority-matrix.svg", "需求优先级矩阵"),
    ],
    "chapter-33-ai-personal-assistant.md": [
        ("../images/chapter-33-openclaw-arch.svg", "OpenClaw个人助手架构"),
        ("../images/chapter-33-assistant-workflow.svg", "个人助手工作流"),
    ],
    "chapter-34-ai-multi-agent.md": [
        ("../images/chapter-34-multi-agent.svg", "多Agent协作架构"),
    ],
    "chapter-35-ai-batch-processing.md": [
        ("../images/chapter-35-batch-processing.svg", "批量代码处理流程"),
    ],
    "chapter-36-ai-cowork-mode.md": [
        ("../images/chapter-36-cowork-comparison.svg", "Cowork模式对比"),
    ],
    "chapter-37-ai-harness-platform.md": [
        ("../images/chapter-37-harness-arch.svg", "Harness平台架构"),
    ],
    "chapter-38-ai-best-practices.md": [
        ("../images/chapter-38-maturity-model.svg", "AI工程成熟度模型"),
    ],
    "chapter-39-ai-builder.md": [
        ("../images/chapter-39-growth-path.svg", "AI时代程序员成长路线"),
    ],
}


def find_insert_position(content: str) -> int:
    """
    找到图片插入位置：
    1. 优先在"故事"部分结束后插入
    2. 或者在第一个二级标题后
    3. 或者在理论部分之前
    """
    lines = content.split('\n')
    
    # 策略1: 查找"故事"部分的结束（通常是"---"分隔线或下一个二级标题）
    in_story = False
    story_end = 0
    
    for i, line in enumerate(lines):
        if re.match(r'^## 故事[：:]', line):
            in_story = True
            continue
        
        if in_story:
            # 故事结束标志：另一个二级标题或分隔线
            if re.match(r'^## ', line) and not re.match(r'^## 故事', line):
                story_end = i
                break
            if line.strip() == '---':
                story_end = i + 1
                break
    
    if story_end > 0:
        return story_end
    
    # 策略2: 在第一个二级标题后插入
    for i, line in enumerate(lines):
        if re.match(r'^## ', line):
            # 找到这个标题段的结束位置
            for j in range(i + 1, len(lines)):
                if re.match(r'^(#{2,} |---|\n\n)', lines[j]):
                    return j
            return i + 3
    
    # 策略3: 在文档开头后
    return min(10, len(lines))


def insert_images_to_chapter(filepath: Path, images: list):
    """插入图片到章节"""
    content = filepath.read_text(encoding='utf-8')
    
    # 检查是否已有图片
    existing_images = re.findall(r'!\[.*?\]\(.*?\)', content)
    if len(existing_images) >= len(images):
        print(f"  ⏭️  已有 {len(existing_images)} 张图片，跳过")
        return False
    
    # 找到插入位置
    lines = content.split('\n')
    insert_pos = find_insert_position(content)
    
    # 构建图片 Markdown
    image_blocks = []
    for img_path, img_title in images:
        # 检查是否已存在
        if img_path in content:
            continue
        image_blocks.append(f"![{img_title}]({img_path})")
    
    if not image_blocks:
        print(f"  ⏭️  所有图片已存在")
        return False
    
    # 插入图片（在插入位置后空一行）
    insert_text = '\n\n' + '\n\n'.join(image_blocks) + '\n\n'
    lines.insert(insert_pos, insert_text)
    
    # 写回文件
    new_content = '\n'.join(lines)
    filepath.write_text(new_content, encoding='utf-8')
    
    print(f"  ✓ 插入了 {len(image_blocks)} 张图片")
    return True


def main():
    print("=" * 60)
    print("📝 智能插入图片到章节")
    print("=" * 60)
    
    modified_count = 0
    total_images = 0
    
    for filename, images in CHAPTER_IMAGES.items():
        filepath = CHAPTERS_DIR / filename
        
        if not filepath.exists():
            print(f"\n⚠️  文件不存在: {filename}")
            continue
        
        print(f"\n📄 {filename}")
        print(f"   计划插入: {len(images)} 张图片")
        
        modified = insert_images_to_chapter(filepath, images)
        if modified:
            modified_count += 1
            total_images += len(images)
    
    print("\n" + "=" * 60)
    print(f"✅ 完成! 修改了 {modified_count} 个文件")
    print(f"📊 共插入约 {total_images} 张图片")
    print("=" * 60)


if __name__ == '__main__':
    main()
