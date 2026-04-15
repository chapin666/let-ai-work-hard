#!/usr/bin/env python3
"""
批量插入图片到各章节
"""
import re
from pathlib import Path

CHAPTERS_DIR = Path("/root/.openclaw/workspace/let-ai-work-hard/chapters")

# 章节图片映射
CHAPTER_IMAGES = {
    # Ch1-2 已有图片，只需补充
    "chapter-01-first-ai-experience.md": [],
    "chapter-02-ai-boundaries.md": [],
    
    # Ch3
    "chapter-03-tool-selection.md": [
        ("## 主流AI编程工具概览", "![AI工具选型决策流程](../images/chapter-03-tool-selection-flow.svg)"),
        ("## 代码编辑器：Cursor、Windsurf、Trae", "![主流AI编程工具对比](../images/chapter-03-tools-compare.svg)"),
    ],
    
    # Ch4
    "chapter-04-prompt-engineering-basics.md": [
        ("## 为什么提示词这么重要？", "![RPCT提示框架](../images/chapter-04-rpct-framework.svg)"),
        ("## RPCT框架详解", "![高质量Prompt构建流程](../images/chapter-04-prompt-structure.svg)"),
    ],
    
    # Ch5
    "chapter-05-cot-structured-output.md": [
        ("## 为什么AI会'偷懒'？", "![思维方式对比](../images/chapter-05-cot-comparison.svg)"),
        ("## 思维链（Chain of Thought）", "![结构化输出工作流程](../images/chapter-05-structured-output.svg)"),
    ],
    
    # Ch6
    "chapter-06-ai-ide-basics.md": [
        ("## Cursor入门：第一天的5个必会操作", "![Cursor Agent模式架构](../images/chapter-06-agent-architecture.svg)"),
    ],
    
    # Ch7
    "chapter-07-ai-ide-advanced.md": [
        ("## 处理复杂项目的策略", "![复杂项目AI协作流程](../images/chapter-07-advanced-workflow.svg)"),
    ],
    
    # Ch8
    "chapter-08-ai-writing-blog.md": [
        ("## 从选题到发布的完整流程", "![AI辅助博客写作流程](../images/chapter-08-blog-workflow.svg)"),
    ],
    
    # Ch9
    "chapter-09-ai-writing-booklet.md": [
        ("## 小册写作的独特挑战", "![AI辅助小册出版流程](../images/chapter-09-booklet-workflow.svg)"),
    ],
    
    # Ch10
    "chapter-10-ai-speaking.md": [
        ("## 演讲内容的结构化组织", "![AI辅助演讲准备流程](../images/chapter-10-speaking-workflow.svg)"),
    ],
    
    # Ch11
    "chapter-11-ai-learning.md": [
        ("## AI时代的学习方法变革", "![AI辅助学习系统](../images/chapter-11-learning-system.svg)"),
    ],
    
    # Ch12
    "chapter-12-ai-frontend.md": [
        ("## 组件开发的AI协作模式", "![AI辅助前端开发流程](../images/chapter-12-frontend-workflow.svg)"),
    ],
    
    # Ch13
    "chapter-13-ai-backend.md": [
        ("## API开发的AI辅助", "![AI辅助后端开发流程](../images/chapter-13-backend-workflow.svg)"),
    ],
    
    # Ch14
    "chapter-14-ai-refactoring.md": [
        ("## 何时应该重构？", "![代码重构决策流程](../images/chapter-14-refactoring-flow.svg)"),
    ],
    
    # Ch15
    "chapter-15-ai-code-review.md": [
        ("## AI代码审查的优势", "![代码审查维度](../images/chapter-15-review-dimensions.svg)"),
    ],
    
    # Ch16 - 性能优化
    "chapter-16-ai-performance.md": [
        ("## 性能瓶颈定位", "![AI辅助性能优化流程](../images/chapter-16-performance-flow.svg)"),
    ],
    
    # Ch17
    "chapter-17-ai-test-design.md": [
        ("## 测试用例设计基础", "![AI辅助测试设计流程](../images/chapter-17-test-design.svg)"),
    ],
    
    # Ch18
    "chapter-18-ai-automation-test.md": [
        ("## 自动化测试框架选型", "![自动化测试架构](../images/chapter-18-automation-arch.svg)"),
    ],
    
    # Ch19 - API测试
    "chapter-19-ai-api-test.md": [
        ("## API测试策略", "![API测试流程](../images/chapter-19-api-test-flow.svg)"),
    ],
    
    # Ch20 - 安全测试
    "chapter-20-ai-security-test.md": [
        ("## 安全测试基础", "![安全测试流程](../images/chapter-20-security-flow.svg)"),
    ],
    
    # Ch21
    "chapter-21-ai-sql-optimization.md": [
        ("## 慢查询分析与优化", "![AI辅助SQL优化流程](../images/chapter-21-sql-optimization.svg)"),
    ],
    
    # Ch22
    "chapter-22-ai-scripting.md": [
        ("## 脚本自动化的价值", "![脚本自动化开发流程](../images/chapter-22-scripting-workflow.svg)"),
    ],
    
    # Ch23
    "chapter-23-ai-docker.md": [
        ("## 容器化入门", "![Docker容器化流程](../images/chapter-23-docker-workflow.svg)"),
    ],
    
    # Ch24
    "chapter-24-ai-cicd.md": [
        ("## CI/CD流水线设计", "![CI/CD流水线架构](../images/chapter-24-cicd-architecture.svg)"),
    ],
    
    # Ch25
    "chapter-25-ai-monitoring.md": [
        ("## 可观测性基础", "![可观测性三大支柱](../images/chapter-25-observability.svg)"),
    ],
    
    # Ch26
    "chapter-26-ai-data-analysis.md": [
        ("## 数据分析的工作流程", "![数据分析工作流程](../images/chapter-26-data-analysis.svg)"),
    ],
    
    # Ch27
    "chapter-27-ai-requirements.md": [
        ("## 需求分析的挑战", "![AI辅助需求分析流程](../images/chapter-27-requirements-flow.svg)"),
    ],
    
    # Ch28
    "chapter-28-ai-tech-decision.md": [
        ("## 技术选型的复杂性", "![技术选型评估维度](../images/chapter-28-tech-decision.svg)"),
    ],
    
    # Ch29
    "chapter-29-ai-project-management.md": [
        ("## 项目规划与跟踪", "![项目管理流程优化](../images/chapter-29-project-management.svg)"),
    ],
    
    # Ch30
    "chapter-30-ai-team-collab.md": [
        ("## 跨职能协作的痛点", "![团队协作架构](../images/chapter-30-team-collab.svg)"),
    ],
    
    # Ch31
    "chapter-31-ai-knowledge.md": [
        ("## 知识管理的重要性", "![知识库建设流程](../images/chapter-31-knowledge-workflow.svg)"),
    ],
    
    # Ch32
    "chapter-32-ai-pm-workflow.md": [
        ("## 需求优先级管理", "![需求优先级矩阵](../images/chapter-32-priority-matrix.svg)"),
    ],
    
    # Ch33
    "chapter-33-ai-personal-assistant.md": [
        ("## OpenClaw简介", "![OpenClaw个人助手架构](../images/chapter-33-openclaw-arch.svg)"),
        ("## 个人助手的日常应用", "![个人助手工作流](../images/chapter-33-assistant-workflow.svg)"),
    ],
    
    # Ch34
    "chapter-34-ai-multi-agent.md": [
        ("## 从单Agent到多Agent", "![多Agent协作架构](../images/chapter-34-multi-agent.svg)"),
    ],
    
    # Ch35
    "chapter-35-ai-batch-processing.md": [
        ("## 批量处理的适用场景", "![批量代码处理流程](../images/chapter-35-batch-processing.svg)"),
    ],
    
    # Ch36
    "chapter-36-ai-cowork-mode.md": [
        ("## Cowork模式是什么？", "![Cowork模式对比](../images/chapter-36-cowork-comparison.svg)"),
    ],
    
    # Ch37
    "chapter-37-ai-harness-platform.md": [
        ("## Harness平台的设计理念", "![Harness平台架构](../images/chapter-37-harness-arch.svg)"),
    ],
    
    # Ch38
    "chapter-38-ai-best-practices.md": [
        ("## AI工程成熟度评估", "![AI工程成熟度模型](../images/chapter-38-maturity-model.svg)"),
    ],
    
    # Ch39
    "chapter-39-ai-builder.md": [
        ("## 从使用者到建设者", "![AI时代程序员成长路线](../images/chapter-39-growth-path.svg)"),
    ],
}


def insert_images_to_chapter(filepath: Path, images: list):
    """插入图片到章节"""
    content = filepath.read_text(encoding='utf-8')
    modified = False
    
    for heading_pattern, image_md in images:
        # 查找标题位置
        pattern = re.escape(heading_pattern) + r'\s*\n'
        match = re.search(pattern, content)
        
        if match:
            # 检查是否已存在该图片
            if image_md in content:
                print(f"    跳过(已存在): {image_md[:50]}...")
                continue
            
            # 在标题后插入图片
            insert_pos = match.end()
            insert_text = f"\n{image_md}\n\n"
            content = content[:insert_pos] + insert_text + content[insert_pos:]
            modified = True
            print(f"    插入: {image_md[:50]}...")
        else:
            # 尝试模糊匹配
            heading_keywords = heading_pattern.replace('## ', '').replace('：', '').replace('，', '')[:10]
            if heading_keywords in content:
                # 找到近似位置，尝试插入
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if heading_keywords in line and line.startswith('##'):
                        if image_md not in content:
                            lines.insert(i + 1, '')
                            lines.insert(i + 2, image_md)
                            lines.insert(i + 3, '')
                            content = '\n'.join(lines)
                            modified = True
                            print(f"    插入(模糊): {image_md[:50]}...")
                        break
    
    if modified:
        filepath.write_text(content, encoding='utf-8')
        return True
    return False


def main():
    print("=" * 60)
    print("📝 开始插入图片到章节")
    print("=" * 60)
    
    inserted_count = 0
    skipped_count = 0
    
    for filename, images in CHAPTER_IMAGES.items():
        filepath = CHAPTERS_DIR / filename
        
        if not filepath.exists():
            print(f"\n⚠️ 文件不存在: {filename}")
            skipped_count += 1
            continue
        
        if not images:
            print(f"\n⏭️ {filename}: 无需插入")
            continue
        
        print(f"\n📄 {filename}")
        modified = insert_images_to_chapter(filepath, images)
        if modified:
            inserted_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 完成! 修改了 {inserted_count} 个文件")
    print(f"⏭️ 跳过了 {skipped_count} 个文件")
    print("=" * 60)


if __name__ == '__main__':
    main()
