#!/usr/bin/env python3
"""
批量 SVG 图片生成器
为全书章节生成统一风格的插图
"""
import os
from pathlib import Path

IMAGES_DIR = Path("/root/.openclaw/workspace/let-ai-work-hard/images")
COLORS = {
    'primary': '#3b82f6',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'text': '#1f2937',
    'text_light': '#6b7280',
    'bg': '#ffffff',
    'border': '#e5e7eb',
    'bg_light': '#f3f4f6'
}

class SVGGenerator:
    """SVG 图片生成器"""
    
    def __init__(self):
        IMAGES_DIR.mkdir(exist_ok=True)
    
    def save(self, filename: str, content: str):
        """保存 SVG 文件"""
        filepath = IMAGES_DIR / filename
        filepath.write_text(content, encoding='utf-8')
        print(f"  ✓ {filename}")
        return filepath

    def flowchart(self, title: str, steps: list, filename: str):
        """生成流程图"""
        width = 800
        step_height = 80
        padding = 40
        height = padding * 2 + len(steps) * step_height
        
        # 步骤节点
        nodes = []
        arrows = []
        y = padding + 30
        
        for i, step in enumerate(steps):
            # 节点背景
            nodes.append(f'''
            <rect x="200" y="{y}" width="400" height="50" rx="8" fill="{COLORS['bg']}" stroke="{COLORS['primary']}" stroke-width="2"/>
            <text x="400" y="{y+32}" text-anchor="middle" font-size="14" fill="{COLORS['text']}" font-family="system-ui">{step}</text>
            <circle cx="180" cy="{y+25}" r="15" fill="{COLORS['primary']}"/>
            <text x="180" y="{y+30}" text-anchor="middle" font-size="12" fill="white" font-family="system-ui" font-weight="bold">{i+1}</text>
            ''')
            
            # 箭头
            if i < len(steps) - 1:
                arrows.append(f'<path d="M400 {y+50} L400 {y+80}" stroke="{COLORS['text_light']}" stroke-width="2" marker-end="url(#arrowhead)"/>')
            
            y += step_height
        
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="{COLORS['text_light']}"/>
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="{COLORS['bg_light']}"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="{COLORS['text']}" font-family="system-ui">{title}</text>
  {''.join(nodes)}
  {''.join(arrows)}
</svg>'''
        
        return self.save(filename, svg)
    
    def comparison(self, title: str, left_title: str, right_title: str, 
                   left_items: list, right_items: list, filename: str):
        """生成对比图"""
        width = 800
        height = 500
        
        left_content = ''.join([f'<text x="180" y="{180+i*35}" text-anchor="middle" font-size="13" fill="{COLORS['text']}">• {item}</text>' for i, item in enumerate(left_items)])
        right_content = ''.join([f'<text x="620" y="{180+i*35}" text-anchor="middle" font-size="13" fill="{COLORS['text']}">• {item}</text>' for i, item in enumerate(right_items)])
        
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="{COLORS['bg_light']}"/>
  
  <!-- 标题 -->
  <text x="400" y="40" text-anchor="middle" font-size="20" font-weight="bold" fill="{COLORS['text']}" font-family="system-ui">{title}</text>
  
  <!-- 左侧 -->
  <rect x="50" y="70" width="330" height="400" rx="12" fill="{COLORS['bg']}" stroke="{COLORS['border']}" stroke-width="1"/>
  <rect x="50" y="70" width="330" height="50" rx="12" fill="{COLORS['danger']}"/>
  <text x="215" y="102" text-anchor="middle" font-size="16" font-weight="bold" fill="white" font-family="system-ui">{left_title}</text>
  {left_content}
  
  <!-- 右侧 -->
  <rect x="420" y="70" width="330" height="400" rx="12" fill="{COLORS['bg']}" stroke="{COLORS['border']}" stroke-width="1"/>
  <rect x="420" y="70" width="330" height="50" rx="12" fill="{COLORS['success']}"/>
  <text x="585" y="102" text-anchor="middle" font-size="16" font-weight="bold" fill="white" font-family="system-ui">{right_title}</text>
  {right_content}
  
  <!-- VS -->
  <circle cx="400" cy="270" r="25" fill="{COLORS['primary']}"/>
  <text x="400" y="276" text-anchor="middle" font-size="14" font-weight="bold" fill="white" font-family="system-ui">VS</text>
</svg>'''
        
        return self.save(filename, svg)
    
    def framework(self, title: str, items: list, filename: str, layout: str = "horizontal"):
        """生成框架/结构图"""
        width = 800
        
        if layout == "horizontal":
            height = 300
            box_width = 700 // len(items)
            x_start = 50
            
            boxes = []
            for i, (name, desc) in enumerate(items):
                x = x_start + i * (box_width + 10)
                boxes.append(f'''
                <rect x="{x}" y="100" width="{box_width}" height="150" rx="8" fill="{COLORS['bg']}" stroke="{COLORS['primary']}" stroke-width="2"/>
                <text x="{x + box_width//2}" y="135" text-anchor="middle" font-size="16" font-weight="bold" fill="{COLORS['primary']}" font-family="system-ui">{name}</text>
                <text x="{x + box_width//2}" y="175" text-anchor="middle" font-size="12" fill="{COLORS['text_light']}" font-family="system-ui">{desc}</text>
                ''')
                
                if i < len(items) - 1:
                    boxes.append(f'<path d="M{x + box_width + 5} 175 L{x + box_width + 10} 175" stroke="{COLORS['primary']}" stroke-width="2" marker-end="url(#arrowhead)"/>')
        else:  # vertical
            height = 120 + len(items) * 80
            boxes = []
            for i, (name, desc) in enumerate(items):
                y = 80 + i * 80
                boxes.append(f'''
                <rect x="150" y="{y}" width="500" height="60" rx="8" fill="{COLORS['bg']}" stroke="{COLORS['primary']}" stroke-width="2"/>
                <text x="180" y="{y+25}" font-size="15" font-weight="bold" fill="{COLORS['primary']}" font-family="system-ui">{name}</text>
                <text x="180" y="{y+48}" font-size="12" fill="{COLORS['text_light']}" font-family="system-ui">{desc}</text>
                <text x="120" y="{y+40}" text-anchor="middle" font-size="18" font-weight="bold" fill="{COLORS['primary']}" font-family="system-ui">{i+1}</text>
                ''')
        
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="{COLORS['primary']}"/>
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="{COLORS['bg_light']}"/>
  <text x="400" y="45" text-anchor="middle" font-size="20" font-weight="bold" fill="{COLORS['text']}" font-family="system-ui">{title}</text>
  {''.join(boxes)}
</svg>'''
        
        return self.save(filename, svg)
    
    def architecture(self, title: str, layers: list, filename: str):
        """生成架构分层图"""
        width = 800
        layer_height = 90
        height = 150 + len(layers) * layer_height
        
        layer_boxes = []
        for i, (layer_name, components) in enumerate(layers):
            y = 100 + i * layer_height
            # 层背景
            layer_boxes.append(f'<rect x="100" y="{y}" width="600" height="70" rx="8" fill="{COLORS['bg']}" stroke="{COLORS['primary']}" stroke-width="2"/>')
            # 层名称
            layer_boxes.append(f'<text x="130" y="{y+25}" font-size="14" font-weight="bold" fill="{COLORS['primary']}" font-family="system-ui">{layer_name}</text>')
            # 组件
            comp_text = " | ".join(components)
            layer_boxes.append(f'<text x="130" y="{y+55}" font-size="12" fill="{COLORS['text']}" font-family="system-ui">{comp_text}</text>')
        
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="{COLORS['bg_light']}"/>
  <text x="400" y="50" text-anchor="middle" font-size="20" font-weight="bold" fill="{COLORS['text']}" font-family="system-ui">{title}</text>
  {''.join(layer_boxes)}
</svg>'''
        
        return self.save(filename, svg)


def generate_all_images():
    """生成全书所有图片"""
    gen = SVGGenerator()
    
    print("=" * 60)
    print("🎨 开始生成全书插图")
    print("=" * 60)
    
    # ========== 第一部分：初识AI ==========
    print("\n📚 第一部分：初识AI")
    
    print("\n  Ch3 - 工具选型:")
    gen.flowchart("AI工具选型决策流程", [
        "明确使用场景和需求",
        "评估预算和团队规模",
        "对比主流工具特性",
        "小规模试用验证",
        "团队推广使用"
    ], "chapter-03-tool-selection-flow.svg")
    
    gen.comparison("主流AI编程工具对比", "传统开发", "AI辅助开发",
                  ["手动编写所有代码", "反复查阅文档", "调试耗时久", "重构风险高"],
                  ["AI生成基础代码", "智能上下文提示", "快速定位问题", "安全重构建议"],
                  "chapter-03-tools-compare.svg")
    
    print("\n  Ch4 - 提示工程基础:")
    gen.framework("RPCT提示框架", [
        ("Role", "定义AI角色身份"),
        ("Profile", "设定背景信息"),
        ("Constraint", "列出约束条件"),
        ("Task", "明确具体任务")
    ], "chapter-04-rpct-framework.svg")
    
    gen.flowchart("高质量Prompt构建流程", [
        "确定AI角色和专业领域",
        "补充必要的背景信息",
        "列出所有约束条件",
        "明确具体的任务目标",
        "添加输出格式要求"
    ], "chapter-04-prompt-structure.svg")
    
    print("\n  Ch5 - CoT与结构化输出:")
    gen.comparison("思维方式对比", "直接回答", "思维链(CoT)",
                  ["一步到位给出答案", "容易遗漏边界情况", "难以追溯思考过程", "复杂问题易出错"],
                  ["分步骤拆解问题", "全面考虑各种情况", "逻辑清晰可验证", "复杂任务更准确"],
                  "chapter-05-cot-comparison.svg")
    
    gen.flowchart("结构化输出工作流程", [
        "定义输出数据格式",
        "在Prompt中指定格式",
        "AI按格式生成内容",
        "解析结构化数据",
        "集成到应用程序"
    ], "chapter-05-structured-output.svg")
    
    print("\n  Ch6 - AI IDE入门:")
    gen.architecture("Cursor Agent模式架构", [
        ("用户层", ["自然语言描述需求", "审查AI生成的计划"]),
        ("Agent层", ["理解需求", "制定执行计划", "调用工具"]),
        ("工具层", ["文件读写", "终端命令", "代码搜索", "API调用"]),
        ("执行层", ["修改代码", "运行测试", "验证结果"])
    ], "chapter-06-agent-architecture.svg")
    
    print("\n  Ch7 - AI IDE进阶:")
    gen.flowchart("复杂项目AI协作流程", [
        "分析项目架构和依赖",
        "制定分阶段实施计划",
        "小步快跑迭代开发",
        "持续测试验证",
        "Review和优化"
    ], "chapter-07-advanced-workflow.svg")
    
    print("\n  Ch8 - 技术写作:")
    gen.flowchart("AI辅助博客写作流程", [
        "确定主题和关键词",
        "AI生成大纲结构",
        "分章节生成内容",
        "人工润色调整",
        "发布和推广"
    ], "chapter-08-blog-workflow.svg")
    
    print("\n  Ch9 - 小册出版:")
    gen.flowchart("AI辅助小册出版流程", [
        "确定选题和目标读者",
        "AI生成整体框架",
        "并行写作各章节",
        "统一风格审核",
        "排版和发布"
    ], "chapter-09-booklet-workflow.svg")
    
    # ========== 第二部分：演讲与学习 ==========
    print("\n📚 第二部分：演讲与学习")
    
    print("\n  Ch10 - 演讲:")
    gen.flowchart("AI辅助演讲准备流程", [
        "确定演讲主题和目标",
        "AI生成内容大纲",
        "制作演讲PPT",
        "模拟演练和计时",
        "现场演讲呈现"
    ], "chapter-10-speaking-workflow.svg")
    
    print("\n  Ch11 - 学习:")
    gen.architecture("AI辅助学习系统", [
        ("输入层", ["学习目标", "现有水平", "时间约束"]),
        ("规划层", ["路径设计", "资源推荐", "里程碑设定"]),
        ("执行层", ["内容生成", "练习题目", "答疑解惑"]),
        ("反馈层", ["进度跟踪", "弱项分析", "计划调整"])
    ], "chapter-11-learning-system.svg")
    
    # ========== 第三部分：开发实战 ==========
    print("\n📚 第三部分：开发实战")
    
    print("\n  Ch12-14 - 前后端与重构:")
    gen.flowchart("AI辅助前端开发流程", [
        "组件需求分析",
        "生成组件结构",
        "实现交互逻辑",
        "样式调整和优化",
        "测试和集成"
    ], "chapter-12-frontend-workflow.svg")
    
    gen.flowchart("AI辅助后端开发流程", [
        "API需求分析",
        "设计数据模型",
        "生成接口代码",
        "实现业务逻辑",
        "添加测试和文档"
    ], "chapter-13-backend-workflow.svg")
    
    gen.flowchart("代码重构决策流程", [
        "识别代码坏味道",
        "评估重构收益",
        "制定重构计划",
        "小步安全重构",
        "验证功能正确"
    ], "chapter-14-refactoring-flow.svg")
    
    print("\n  Ch15-17 - 代码审查与测试:")
    gen.framework("代码审查维度", [
        ("功能正确性", "逻辑是否符合预期"),
        ("代码可读性", "命名/注释/结构"),
        ("性能效率", "时间/空间复杂度"),
        ("安全性", "潜在漏洞风险")
    ], "chapter-15-review-dimensions.svg", layout="vertical")
    
    gen.flowchart("AI辅助测试设计流程", [
        "分析需求和功能点",
        "识别测试场景",
        "生成测试用例",
        "补充边界情况",
        "评审和优化"
    ], "chapter-17-test-design.svg")
    
    print("\n  Ch18-21 - 自动化与安全:")
    gen.architecture("自动化测试架构", [
        ("测试层", ["单元测试", "集成测试", "E2E测试"]),
        ("AI层", ["用例生成", "代码分析", "缺陷预测"]),
        ("执行层", ["测试运行器", "并行执行", "结果收集"]),
        ("报告层", ["覆盖率报告", "趋势分析", "失败通知"])
    ], "chapter-18-automation-arch.svg")
    
    gen.flowchart("AI辅助SQL优化流程", [
        "分析慢查询日志",
        "识别性能瓶颈",
        "AI生成优化建议",
        "验证执行计划",
        "监控优化效果"
    ], "chapter-21-sql-optimization.svg")
    
    # ========== 第四部分：工程与运维 ==========
    print("\n📚 第四部分：工程与运维")
    
    print("\n  Ch22-26 - 运维与数据分析:")
    gen.flowchart("脚本自动化开发流程", [
        "识别重复性任务",
        "分析任务执行步骤",
        "AI生成脚本代码",
        "本地测试验证",
        "部署和调度"
    ], "chapter-22-scripting-workflow.svg")
    
    gen.flowchart("Docker容器化流程", [
        "分析应用依赖",
        "编写Dockerfile",
        "构建镜像",
        "配置容器编排",
        "部署和监控"
    ], "chapter-23-docker-workflow.svg")
    
    gen.architecture("CI/CD流水线架构", [
        ("源码管理", ["Git提交", "分支策略", "代码审查"]),
        ("构建阶段", ["依赖安装", "编译打包", "镜像构建"]),
        ("测试阶段", ["单元测试", "集成测试", "安全扫描"]),
        ("部署阶段", ["预发布", "生产发布", "回滚机制"])
    ], "chapter-24-cicd-architecture.svg")
    
    gen.framework("可观测性三大支柱", [
        ("Metrics", "指标监控 - 系统状态量化"),
        ("Logging", "日志记录 - 事件追踪分析"),
        ("Tracing", "链路追踪 - 请求全链路"),
        ("Alerting", "告警通知 - 异常及时响应")
    ], "chapter-25-observability.svg", layout="vertical")
    
    gen.flowchart("数据分析工作流程", [
        "明确分析目标",
        "数据采集和清洗",
        "探索性数据分析",
        "AI辅助洞察发现",
        "可视化呈现"
    ], "chapter-26-data-analysis.svg")
    
    # ========== 第五部分：团队协作 ==========
    print("\n📚 第五部分：团队协作")
    
    print("\n  Ch27-32 - 产品与管理:")
    gen.flowchart("AI辅助需求分析流程", [
        "收集原始需求",
        "澄清和细化",
        "结构化整理",
        "生成PRD文档",
        "评审和确认"
    ], "chapter-27-requirements-flow.svg")
    
    gen.comparison("技术选型评估维度", "传统方式", "AI辅助方式",
                  ["主观经验判断", "信息收集耗时", "容易遗漏方案", "难以量化对比"],
                  ["多维度分析", "快速生成对比表", "全面方案调研", "客观评分机制"],
                  "chapter-28-tech-decision.svg")
    
    gen.flowchart("项目管理流程优化", [
        "项目目标设定",
        "AI生成WBS",
        "任务分配和排期",
        "进度自动跟踪",
        "风险预警和调整"
    ], "chapter-29-project-management.svg")
    
    gen.architecture("团队协作架构", [
        ("产品层", ["需求管理", "原型设计", "用户故事"]),
        ("开发层", ["任务管理", "代码协作", "技术方案"]),
        ("设计层", ["设计稿", "设计规范", "走查反馈"]),
        ("AI层", ["智能推荐", "自动化", "知识库"])
    ], "chapter-30-team-collab.svg")
    
    gen.flowchart("知识库建设流程", [
        "确定知识分类",
        "收集分散文档",
        "AI整理和结构化",
        "建立检索系统",
        "持续更新维护"
    ], "chapter-31-knowledge-workflow.svg")
    
    gen.framework("需求优先级矩阵", [
        ("P0-紧急重要", "立即处理，投入主要资源"),
        ("P1-重要不紧急", "规划排期，确保完成"),
        ("P2-紧急不重要", "快速处理或委托他人"),
        ("P3-不紧急不重要", "记录 backlog，有空再做")
    ], "chapter-32-priority-matrix.svg", layout="vertical")
    
    # ========== 第六部分：Agent与平台 ==========
    print("\n📚 第六部分：Agent与平台")
    
    print("\n  Ch33-35 - Agent开发:")
    gen.architecture("OpenClaw个人助手架构", [
        ("交互层", ["聊天界面", "语音输入", "命令行"]),
        ("Agent层", ["意图理解", "任务规划", "工具选择"]),
        ("工具层", ["文件操作", "网络请求", "代码执行"]),
        ("记忆层", ["对话历史", "用户偏好", "知识库"])
    ], "chapter-33-openclaw-arch.svg")
    
    gen.flowchart("个人助手工作流", [
        "接收用户指令",
        "理解意图和上下文",
        "规划执行步骤",
        "调用相应工具",
        "返回执行结果"
    ], "chapter-33-assistant-workflow.svg")
    
    gen.architecture("多Agent协作架构", [
        ("协调Agent", ["任务分发", "结果汇总", "冲突解决"]),
        ("专业Agent", ["代码Agent", "测试Agent", "文档Agent"]),
        ("通信总线", ["消息队列", "状态同步", "事件通知"]),
        ("共享存储", ["知识库", "中间结果", "执行日志"])
    ], "chapter-34-multi-agent.svg")
    
    gen.flowchart("批量代码处理流程", [
        "扫描目标文件",
        "分析文件类型和内容",
        "AI生成转换规则",
        "批量执行转换",
        "验证和回滚机制"
    ], "chapter-35-batch-processing.svg")
    
    print("\n  Ch36-38 - 平台与工程化:")
    gen.comparison("Cowork模式对比", "传统开发模式", "Cowork模式",
                  ["人找工具，被动响应", "单点沟通，信息孤岛", "人工检查，容易遗漏", "个人经验，难以复用"],
                  ["AI主动推荐和提醒", "全流程上下文共享", "自动化检查和反馈", "团队知识持续积累"],
                  "chapter-36-cowork-comparison.svg")
    
    gen.architecture("Harness平台架构", [
        ("开发者界面", ["IDE插件", "Web控制台", "CLI工具"]),
        ("AI引擎", ["代码生成", "智能分析", "质量评估"]),
        ("服务层", ["项目管理", "协作工具", "知识库"]),
        ("基础设施", ["计算资源", "存储系统", "网络服务"])
    ], "chapter-37-harness-arch.svg")
    
    gen.framework("AI工程成熟度模型", [
        ("L1-个体使用", "开发者个人使用AI工具"),
        ("L2-团队规范", "团队建立AI使用规范"),
        ("L3-流程集成", "AI嵌入开发测试流程"),
        ("L4-平台化", "建设统一的AI工程平台")
    ], "chapter-38-maturity-model.svg", layout="vertical")
    
    # ========== 第七部分：进阶与展望 ==========
    print("\n📚 第七部分：进阶与展望")
    
    print("\n  Ch39 - 成长路线:")
    gen.framework("AI时代程序员成长路线", [
        ("使用者", "熟练使用AI工具提升效率"),
        ("整合者", "将AI融入团队协作流程"),
        ("建设者", "搭建团队AI工程平台"),
        ("引领者", "推动组织AI转型")
    ], "chapter-39-growth-path.svg", layout="vertical")
    
    print("\n" + "=" * 60)
    print("✅ 全部图片生成完成!")
    print(f"📁 图片目录: {IMAGES_DIR}")
    print(f"📊 总计: {len(list(IMAGES_DIR.glob('*.svg')))} 张 SVG 图片")
    print("=" * 60)


if __name__ == '__main__':
    generate_all_images()
