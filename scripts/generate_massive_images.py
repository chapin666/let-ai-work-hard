#!/usr/bin/env python3
"""
大规模 SVG 图片生成器 - 完整版
目标：生成150+张图片
"""
import os
import math
from pathlib import Path

IMAGES_DIR = Path("/root/.openclaw/workspace/let-ai-work-hard/images")
COLORS = {
    'primary': '#3b82f6', 'primary_light': '#dbeafe',
    'success': '#10b981', 'success_light': '#d1fae5',
    'warning': '#f59e0b', 'warning_light': '#fef3c7',
    'danger': '#ef4444', 'danger_light': '#fee2e2',
    'text': '#1f2937', 'text_light': '#6b7280',
    'bg': '#ffffff', 'border': '#e5e7eb', 'bg_light': '#f9fafb',
}

class SVGGen:
    def __init__(self):
        IMAGES_DIR.mkdir(exist_ok=True)
        self.count = 0
    
    def save(self, name, content):
        path = IMAGES_DIR / name
        path.write_text(content, encoding='utf-8')
        self.count += 1
        if self.count % 30 == 0:
            print(f"  已生成 {self.count} 张...")
        return path

    def flow(self, title, steps, filename):
        h = 100 + len(steps) * 70
        nodes = []
        y = 60
        for i, step in enumerate(steps):
            nodes.append(f'<circle cx="60" cy="{y}" r="20" fill="{COLORS["primary"]}"/><text x="60" y="{y+5}" text-anchor="middle" font-size="14" fill="white">{i+1}</text>')
            nodes.append(f'<rect x="100" y="{y-20}" width="600" height="40" rx="8" fill="{COLORS["bg"]}" stroke="{COLORS["border"]}"/><text x="120" y="{y+5}" font-size="12" fill="{COLORS["text"]}">{step[:45]}</text>')
            if i < len(steps)-1:
                nodes.append(f'<line x1="60" y1="{y+20}" x2="60" y2="{y+50}" stroke="{COLORS["primary"]}" stroke-width="2"/>')
            y += 70
        svg = f'<svg width="800" height="{h}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="{COLORS["bg_light"]}"/><text x="400" y="35" text-anchor="middle" font-size="16" fill="{COLORS["text"]}" font-weight="bold">{title}</text>{"".join(nodes)}</svg>'
        return self.save(filename, svg)

    def compare(self, title, left, right, l_items, r_items, filename):
        h = max(150 + len(l_items)*30, 150 + len(r_items)*30)
        li = ''.join([f'<text x="185" y="{160+i*30}" text-anchor="middle" font-size="11" fill="{COLORS["text"]}">• {it[:22]}</text>' for i,it in enumerate(l_items)])
        ri = ''.join([f'<text x="615" y="{160+i*30}" text-anchor="middle" font-size="11" fill="{COLORS["text"]}">• {it[:22]}</text>' for i,it in enumerate(r_items)])
        svg = f'<svg width="800" height="{h}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="{COLORS["bg_light"]}"/><text x="400" y="40" text-anchor="middle" font-size="18" fill="{COLORS["text"]}" font-weight="bold">{title}</text><rect x="40" y="70" width="340" height="{h-100}" rx="10" fill="{COLORS["bg"]}" stroke="{COLORS["danger"]}" stroke-width="2"/><rect x="40" y="70" width="340" height="40" rx="10" fill="{COLORS["danger"]}"/><text x="210" y="97" text-anchor="middle" font-size="14" fill="white">{left}</text>{li}<rect x="420" y="70" width="340" height="{h-100}" rx="10" fill="{COLORS["bg"]}" stroke="{COLORS["success"]}" stroke-width="2"/><rect x="420" y="70" width="340" height="40" rx="10" fill="{COLORS["success"]}"/><text x="590" y="97" text-anchor="middle" font-size="14" fill="white">{right}</text>{ri}<circle cx="400" cy="{h//2}" r="20" fill="{COLORS["primary"]}"/><text x="400" y="{h//2+5}" text-anchor="middle" font-size="12" fill="white">VS</text></svg>'
        return self.save(filename, svg)

    def concept(self, title, items, filename):
        w, h = 800, 500
        cx, cy = 400, 280
        nodes = []
        n = len(items)
        for i, (name, desc) in enumerate(items):
            angle = 2 * math.pi * i / n - math.pi / 2
            x, y = cx + 180 * math.cos(angle) * 1.3, cy + 140 * math.sin(angle)
            nodes.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{COLORS["border"]}" stroke-width="2"/>')
            nodes.append(f'<circle cx="{x}" cy="{y}" r="55" fill="{COLORS["bg"]}" stroke="{COLORS["primary"]}" stroke-width="2"/>')
            nodes.append(f'<text x="{x}" y="{y-5}" text-anchor="middle" font-size="12" fill="{COLORS["primary"]}" font-weight="bold">{name[:8]}</text>')
            if desc: nodes.append(f'<text x="{x}" y="{y+12}" text-anchor="middle" font-size="9" fill="{COLORS["text_light"]}">{desc[:10]}</text>')
        nodes.append(f'<circle cx="{cx}" cy="{cy}" r="75" fill="{COLORS["primary_light"]}" stroke="{COLORS["primary"]}" stroke-width="3"/>')
        svg = f'<svg width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="{COLORS["bg_light"]}"/><text x="400" y="45" text-anchor="middle" font-size="18" fill="{COLORS["text"]}" font-weight="bold">{title}</text>{"".join(nodes)}</svg>'
        return self.save(filename, svg)

    def arch(self, title, layers, filename):
        h = 100 + len(layers) * 85
        boxes = []
        for i, (name, comps) in enumerate(layers):
            y = 80 + i * 85
            ctext = " | ".join(comps[:3])
            boxes.append(f'<rect x="100" y="{y}" width="600" height="70" rx="8" fill="{COLORS["bg"]}" stroke="{COLORS["primary"]}" stroke-width="2"/><text x="120" y="{y+25}" font-size="13" fill="{COLORS["primary"]}" font-weight="bold">{name}</text><text x="120" y="{y+52}" font-size="11" fill="{COLORS["text"]}">{ctext}</text>')
        svg = f'<svg width="800" height="{h}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="{COLORS["bg_light"]}"/><text x="400" y="50" text-anchor="middle" font-size="18" fill="{COLORS["text"]}" font-weight="bold">{title}</text>{"".join(boxes)}</svg>'
        return self.save(filename, svg)

    def checklist(self, title, items, filename):
        h = 100 + len(items) * 35
        rows = []
        for i, (item, ok) in enumerate(items):
            y = 90 + i * 35
            color = COLORS["success"] if ok else COLORS["border"]
            sym = "✓" if ok else "○"
            rows.append(f'<circle cx="50" cy="{y}" r="10" fill="{COLORS["bg"]}" stroke="{color}" stroke-width="2"/><text x="50" y="{y+4}" text-anchor="middle" font-size="12" fill="{color}">{sym}</text><text x="75" y="{y+4}" font-size="12" fill="{COLORS["text"]}">{item[:40]}</text>')
        svg = f'<svg width="600" height="{h}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="{COLORS["bg_light"]}"/><text x="300" y="50" text-anchor="middle" font-size="16" fill="{COLORS["text"]}" font-weight="bold">{title}</text>{"".join(rows)}</svg>'
        return self.save(filename, svg)

    def chat(self, title, msgs, filename):
        h = 100 + len(msgs) * 60
        bubbles = []
        y = 80
        for role, txt in msgs:
            isu = role == "user"
            x, color = (50 if isu else 200), (COLORS["primary_light"] if isu else COLORS["bg"])
            bubbles.append(f'<rect x="{x}" y="{y}" width="200" height="45" rx="12" fill="{color}" stroke="{COLORS["border"]}"/><text x="{x+100}" y="{y+28}" text-anchor="middle" font-size="11" fill="{COLORS["text"]}">{txt[:25]}</text>')
            y += 60
        svg = f'<svg width="450" height="{h}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="{COLORS["bg_light"]}"/><text x="225" y="40" text-anchor="middle" font-size="16" fill="{COLORS["text"]}" font-weight="bold">{title}</text>{"".join(bubbles)}</svg>'
        return self.save(filename, svg)

    def stats(self, title, data, filename):
        maxv = max(v for _,v in data) if data else 100
        bw = min(60, 500 // len(data))
        bars = []
        for i,(l,v) in enumerate(data):
            x, bh = 80 + i*(bw+15), (v/maxv)*200
            bars.append(f'<rect x="{x}" y="{280-bh}" width="{bw}" height="{bh}" fill="{COLORS["primary"]}" rx="4"/><text x="{x+bw//2}" y="{270-bh}" text-anchor="middle" font-size="10" fill="{COLORS["text"]}">{v}</text><text x="{x+bw//2}" y="{300}" text-anchor="middle" font-size="9" fill="{COLORS["text_light"]}">{l[:6]}</text>')
        svg = f'<svg width="700" height="350" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="{COLORS["bg_light"]}"/><text x="350" y="40" text-anchor="middle" font-size="16" fill="{COLORS["text"]}" font-weight="bold">{title}</text><line x1="60" y1="280" x2="640" y2="280" stroke="{COLORS["border"]}" stroke-width="2"/>{"".join(bars)}</svg>'
        return self.save(filename, svg)

    def scene(self, title, person, action, filename):
        svg = f'''<svg width="700" height="350" xmlns="http://www.w3.org/2000/svg">
<rect width="100%" height="100%" fill="{COLORS["bg_light"]}"/>
<rect x="40" y="40" width="620" height="270" rx="15" fill="{COLORS["bg"]}" stroke="{COLORS["border"]}"/>
<rect x="60" y="60" width="140" height="90" rx="5" fill="{COLORS["primary_light"]}"/>
<rect x="450" y="160" width="180" height="110" rx="5" fill="{COLORS["border"]}"/>
<circle cx="280" cy="180" r="35" fill="{COLORS["primary_light"]}" stroke="{COLORS["primary"]}" stroke-width="2"/>
<rect x="240" y="230" width="80" height="70" rx="8" fill="{COLORS["success_light"]}" stroke="{COLORS["success"]}" stroke-width="2"/>
<ellipse cx="180" cy="130" rx="90" ry="35" fill="white" stroke="{COLORS["primary"]}" stroke-width="2"/>
<text x="400" y="30" text-anchor="middle" font-size="16" fill="{COLORS["text"]}" font-weight="bold">{title}</text>
<text x="180" y="135" text-anchor="middle" font-size="11" fill="{COLORS["text"]}">{action[:20]}</text>
<text x="280" y="320" text-anchor="middle" font-size="13" fill="{COLORS["text_light"]}">{person}</text>
</svg>'''
        return self.save(filename, svg)

def main():
    gen = SVGGen()
    print("="*60)
    print("🎨 批量生成图片 - 目标150张")
    print("="*60)

    # 第一部分：Ch1-9
    print("\n📚 第一部分：初识AI...")
    gen.scene("小王的周三", "小王", "正则怎么写？", "ch01-scene.svg")
    gen.chat("第一次对话", [("user", "写手机号正则"), ("ai", "/^1[3-9]\\d{9}$/")], "ch01-chat.svg")
    gen.concept("AI优势", [("速度", "秒级响应"), ("准确", "减少错误"), ("全面", "考虑边界")], "ch01-advantages.svg")
    
    gen.concept("AI边界", [("擅长", "编码"), ("边界", "创意"), ("风险", "安全")], "ch02-boundaries.svg")
    gen.compare("能力对比", "不擅长", "擅长", ["创意设计", "伦理判断"], ["代码生成", "数据处理"], "ch02-compare.svg")
    
    gen.flow("工具选型流程", ["明确需求", "评估预算", "对比试用", "团队推广"], "ch03-flow.svg")
    gen.compare("Cursor对比", "Copilot", "Cursor", ["单行补全"], ["Agent模式"], "ch03-compare.svg")
    gen.arch("工具矩阵", [("编辑器", ["VSCode"]), ("Agent", ["Claude"])], "ch03-matrix.svg")
    gen.checklist("选型检查", [("功能满足", True), ("价格合理", True)], "ch03-check.svg")
    
    gen.flow("Prompt优化", ["初稿", "分析", "迭代", "固化"], "ch04-optimize.svg")
    gen.compare("Prompt对比", "差Prompt", "好Prompt", ["写个登录"], ["Vue3登录组件"], "ch04-compare.svg")
    gen.concept("Prompt要素", [("角色", "专家"), ("任务", "明确"), ("输出", "格式")], "ch04-elements.svg")
    
    gen.flow("CoT流程", ["拆解问题", "逐步推理", "展示过程", "验证结果"], "ch05-cot-flow.svg")
    gen.compare("CoT对比", "直接", "CoT", ["一步到位"], ["分步拆解"], "ch05-compare.svg")
    
    gen.scene("Cursor首日", "小张", "Tab停不下来", "ch06-scene.svg")
    gen.flow("核心操作", ["Tab补全", "Ctrl+K对话", "@引用", "Agent执行"], "ch06-ops.svg")
    
    gen.flow("复杂项目", ["分析结构", "理解依赖", "制定计划", "分步执行"], "ch07-complex.svg")
    gen.arch("IDE工作流", [("输入", ["自然语言"]), ("处理", ["AI分析"])], "ch07-workflow.svg")
    
    gen.flow("博客流程", ["确定主题", "生成大纲", "撰写内容", "发布推广"], "ch08-blog.svg")
    gen.flow("小册流程", ["确定选题", "设计大纲", "并行写作", "排版发布"], "ch09-booklet.svg")

    # 第二部分：Ch10-11
    print("\n📚 第二部分：演讲与学习...")
    gen.flow("演讲准备", ["确定主题", "生成内容", "制作PPT", "模拟演练"], "ch10-speaking.svg")
    gen.arch("学习系统", [("输入", ["目标"]), ("处理", ["规划"]), ("输出", ["成果"])], "ch11-learning.svg")

    # 第三部分：Ch12-21
    print("\n📚 第三部分：开发实战...")
    gen.flow("前端开发", ["需求分析", "组件设计", "交互实现", "测试集成"], "ch12-frontend.svg")
    gen.flow("后端开发", ["API设计", "数据建模", "接口实现", "添加测试"], "ch13-backend.svg")
    gen.flow("代码重构", ["识别坏味道", "评估收益", "安全重构", "验证功能"], "ch14-refactor.svg")
    gen.concept("审查维度", [("功能", "正确性"), ("可读性", "命名"), ("性能", "效率")], "ch15-review.svg")
    gen.flow("性能优化", ["分析瓶颈", "定位问题", "实施优化", "验证效果"], "ch16-performance.svg")
    gen.flow("测试设计", ["分析需求", "识别场景", "生成用例", "补充边界"], "ch17-test.svg")
    gen.arch("自动化架构", [("测试层", ["单元"]), ("AI层", ["生成"])], "ch18-automation.svg")
    gen.flow("API测试", ["定义契约", "生成用例", "执行测试", "报告结果"], "ch19-api.svg")
    gen.flow("安全测试", ["风险识别", "漏洞扫描", "修复建议", "验证修复"], "ch20-security.svg")
    gen.flow("SQL优化", ["分析慢查", "识别瓶颈", "生成优化", "验证效果"], "ch21-sql.svg")

    # 第四部分：Ch22-26
    print("\n📚 第四部分：工程运维...")
    gen.flow("脚本自动化", ["识别任务", "分析步骤", "生成脚本", "部署调度"], "ch22-script.svg")
    gen.flow("Docker化", ["分析依赖", "编写Dockerfile", "构建镜像", "部署监控"], "ch23-docker.svg")
    gen.arch("CI/CD架构", [("源码", ["Git"]), ("构建", ["编译"]), ("部署", ["发布"])], "ch24-cicd.svg")
    gen.concept("可观测性", [("指标", "Metrics"), ("日志", "Logging"), ("追踪", "Tracing")], "ch25-observability.svg")
    gen.flow("数据分析", ["明确目标", "采集清洗", "探索分析", "可视化"], "ch26-data.svg")

    # 第五部分：Ch27-32
    print("\n📚 第五部分：团队协作...")
    gen.flow("需求分析", ["收集需求", "澄清细化", "结构化", "生成PRD"], "ch27-requirements.svg")
    gen.compare("选型评估", "传统", "AI辅助", ["主观判断"], ["多维度分析"], "ch28-tech.svg")
    gen.flow("项目管理", ["目标设定", "生成WBS", "任务分配", "进度跟踪"], "ch29-project.svg")
    gen.arch("协作架构", [("产品", ["需求"]), ("开发", ["任务"])], "ch30-collab.svg")
    gen.flow("知识库", ["确定分类", "收集文档", "AI整理", "建立检索"], "ch31-knowledge.svg")
    gen.concept("优先级矩阵", [("P0", "紧急重要"), ("P1", "重要"), ("P2", "紧急")], "ch32-priority.svg")

    # 第六部分：Ch33-38
    print("\n📚 第六部分：Agent与平台...")
    gen.arch("OpenClaw架构", [("交互", ["聊天"]), ("Agent", ["理解"]), ("工具", ["执行"])], "ch33-arch.svg")
    gen.flow("助手工作流", ["接收指令", "理解意图", "规划步骤", "调用工具"], "ch33-workflow.svg")
    gen.arch("多Agent架构", [("协调", ["分发"]), ("专业", ["代码"]), ("存储", ["知识"])], "ch34-multi.svg")
    gen.flow("批量处理", ["扫描文件", "分析内容", "生成规则", "执行转换"], "ch35-batch.svg")
    gen.compare("Cowork对比", "传统", "Cowork", ["人找工具"], ["AI主动"], "ch36-cowork.svg")
    gen.arch("Harness架构", [("界面", ["IDE"]), ("AI", ["生成"]), ("服务", ["管理"])], "ch37-harness.svg")
    gen.concept("成熟度模型", [("L1", "个体"), ("L2", "团队"), ("L3", "流程"), ("L4", "平台")], "ch38-maturity.svg")

    # 第七部分：Ch39
    print("\n📚 第七部分：成长路线...")
    gen.concept("成长路线", [("使用者", "熟练工具"), ("整合者", "融入流程"), ("建设者", "搭建平台")], "ch39-growth.svg")

    print(f"\n✅ 完成！共生成 {gen.count} 张图片")
    return gen.count

if __name__ == "__main__":
    main()
