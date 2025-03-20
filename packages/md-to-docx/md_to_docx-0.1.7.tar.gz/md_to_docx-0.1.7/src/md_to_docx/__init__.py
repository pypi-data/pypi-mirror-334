"""
Markdown to DOCX converter with Mermaid diagram support

This module provides tools to convert Markdown files to DOCX format,
including rendering Mermaid diagrams as images.

Optional dependencies:
- pymermaid: pip install pymermaid  # 用于纯Python渲染Mermaid图表
- mermaid-py: pip install mermaid-py==0.7.0  # 功能丰富的Mermaid渲染工具

Basic usage:
  from md_to_docx import md_to_docx
  
  # Convert markdown to docx
  md_to_docx(markdown_content, output_file="output.docx")
"""

__version__ = "0.1.1"

import click
import sys
import asyncio
import logging
import os
from pathlib import Path
from typing import Any
from mcp.server import Server
import mcp.types as types
import re
import textwrap

# Handle imports for both package usage and direct script execution
try:
    # When used as a package
    from .core import md_to_docx, render_mermaid_to_image
except ImportError:
    # When run directly
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from src.md_to_docx.core import md_to_docx, render_mermaid_to_image

from mcp.server.fastmcp import FastMCP

__all__ = ["md_to_docx", "render_mermaid_to_image"]

# Initialize FastMCP server
mcp = FastMCP("md_to_docx")

# 添加 textwrap 导入，用于文本换行
import textwrap

@mcp.resource("dir://desktop")
def desktop() -> list[str]:
    """List the files in the user's desktop"""
    desktop = Path.home() / "Desktop"
    return [str(f) for f in desktop.iterdir()]

@mcp.resource("dir://mermaid_docx")
def mermaid_docx_files() -> list[str]:
    """列出E:\Examples\mcpServerExample\mermaidToDocx目录下的所有文件"""
    directory = Path("E:/Examples/mcpServerExample/mermaidToDocx")
    return [str(f) for f in directory.iterdir()]

# 图片资源处理
@mcp.resource("img://{path}")
def image_resource(path: str) -> bytes:
    """处理图片资源，支持本地路径和网络URL"""
    try:
        logging.info(f"处理图片资源: {path}")
        if path.startswith(('http://', 'https://')):
            # 处理网络图片
            import requests
            response = requests.get(path, timeout=10)
            response.raise_for_status()
            return response.content
        else:
            # 处理本地图片
            img_path = Path(path)
            if not img_path.exists():
                logging.warning(f"图片文件不存在: {path}")
                return b'Image not found'
            return img_path.read_bytes()
    except Exception as e:
        logging.error(f"处理图片资源出错: {e}")
        return b'Error processing image'

def generate_placeholder_image(text: str) -> bytes:
    """生成一个包含错误信息的占位图像"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # 创建一个带有文本的图像
        width, height = 400, 200
        image = Image.new("RGB", (width, height), (240, 240, 240))
        draw = ImageDraw.Draw(image)
        
        # 绘制边框
        draw.rectangle([0, 0, width-1, height-1], outline=(200, 200, 200))
        
        # 添加文本
        try:
            # 尝试使用系统字体
            font = ImageFont.truetype("arial.ttf", 14)
        except:
            # 如果没有可用字体，使用默认字体
            font = ImageFont.load_default()
            
        draw.text((20, 20), "图片资源错误", fill=(255, 0, 0), font=font)
        
        # 将长文本分行显示
        wrapped_text = '\n'.join(textwrap.wrap(text, width=40))
        y_position = 50
        for line in wrapped_text.split('\n'):
            draw.text((20, y_position), line, fill=(0, 0, 0), font=font)
            y_position += 20
            
        # 返回图像的二进制数据
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()
    except Exception:
        # 如果无法创建图像，返回一个极简的1x1像素
        return b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?\x00\x05\xfe\x02\xfe\xdc\xccY\xe7\x00\x00\x00\x00IEND\xaeB`\x82'

# Mermaid 图表资源处理
@mcp.resource("mermaid://{diagram_code}")
def mermaid_diagram_resource(diagram_code: str) -> bytes:
    """将 Mermaid 图表代码渲染为图片
    
    Args:
        diagram_code: URL 编码后的 Mermaid 图表代码
        
    Returns:
        渲染后的图片二进制数据
    """
    try:
        # URL 解码
        import urllib.parse
        decoded_code = urllib.parse.unquote(diagram_code)
        logging.info(f"处理 Mermaid 图表: {decoded_code[:50]}...")
        
        # 调用渲染函数
        image_data = render_mermaid_to_image(decoded_code)
        return image_data
    except Exception as e:
        logging.error(f"渲染 Mermaid 图表出错: {e}")
        return b'Error rendering Mermaid diagram'

# 文档样式模板资源
@mcp.resource("template://{template_name}")
def document_template_resource(template_name: str) -> dict:
    """提供文档样式模板配置
    
    Args:
        template_name: 模板名称，如 'default', 'academic', 'modern' 等
        
    Returns:
        样式模板配置字典
    """
    try:
        logging.info(f"加载文档样式模板: {template_name}")
        
        # 预定义的模板
        templates = {
            "default": {
                "title_style": {"font_size": 16, "bold": True, "color": "000000"},
                "heading1_style": {"font_size": 14, "bold": True, "color": "000000"},
                "heading2_style": {"font_size": 12, "bold": True, "color": "000000"},
                "paragraph_style": {"font_size": 11, "line_spacing": 1.15},
                "table_style": "Table Grid",
                "code_block_style": {"font_name": "Courier New", "font_size": 9},
            },
            "academic": {
                "title_style": {"font_size": 16, "bold": True, "color": "000000"},
                "heading1_style": {"font_size": 14, "bold": True, "color": "000000"},
                "heading2_style": {"font_size": 12, "bold": True, "color": "000000"},
                "paragraph_style": {"font_size": 12, "line_spacing": 1.5},
                "table_style": "Light Shading",
                "code_block_style": {"font_name": "Consolas", "font_size": 10},
            },
            "modern": {
                "title_style": {"font_size": 18, "bold": True, "color": "2F5496"},
                "heading1_style": {"font_size": 16, "bold": True, "color": "2F5496"},
                "heading2_style": {"font_size": 14, "bold": True, "color": "2F5496"},
                "paragraph_style": {"font_size": 11, "line_spacing": 1.15},
                "table_style": "Light Grid Accent 1",
                "code_block_style": {"font_name": "Consolas", "font_size": 9.5},
            },
        }
        
        # 返回请求的模板，如果不存在则返回默认模板
        return templates.get(template_name.lower(), templates["default"])
    except Exception as e:
        logging.error(f"加载样式模板出错: {e}")
        return {"error": str(e)}

# 外部资源引用处理
@mcp.resource("external://{url}")
def external_resource(url: str) -> dict:
    """处理外部资源引用，如 YouTube 视频、Gist 等。
    
    返回外部资源的元数据，用于在 DOCX 中添加引用或链接。
    
    Args:
        url: 外部资源的 URL
        
    Returns:
        资源元数据字典
    """
    try:
        logging.info(f"处理外部资源: {url}")
        import urllib.parse
        decoded_url = urllib.parse.unquote(url)
        
        # 识别资源类型
        resource_type = "unknown"
        title = ""
        description = ""
        
        if "youtube.com" in decoded_url or "youtu.be" in decoded_url:
            resource_type = "youtube"
            title = "YouTube 视频"
            description = f"视频链接: {decoded_url}"
        elif "github.com" in decoded_url:
            if "/gist/" in decoded_url:
                resource_type = "gist"
                title = "GitHub Gist"
            else:
                resource_type = "github"
                title = "GitHub 仓库"
            description = f"GitHub 链接: {decoded_url}"
        elif "drive.google.com" in decoded_url:
            resource_type = "gdrive"
            title = "Google Drive 文件"
            description = f"Google Drive 链接: {decoded_url}"
        else:
            title = "外部资源"
            description = f"链接: {decoded_url}"
        
        return {
            "type": resource_type,
            "url": decoded_url,
            "title": title,
            "description": description,
        }
    except Exception as e:
        logging.error(f"处理外部资源出错: {e}")
        return {"error": str(e), "url": url}

@mcp.prompt("analyze_markdown")
def analyze_markdown_prompt(markdown_text: str) -> str:
    """分析 Markdown 文档结构并提供优化建议。
    
    这个提示函数接收 Markdown 文本，然后分析其结构，包括标题层级、
    图片和链接数量、代码块和 Mermaid 图表等元素，并提供潜在的优化建议。
    
    Args:
        markdown_text: 要分析的 Markdown 文本
        
    Returns:
        分析结果和优化建议的格式化文本
        
    Examples:
        >>> analyze_markdown_prompt("# 标题\\n这是正文\\n```mermaid\\ngraph TD;\\nA-->B;\\n```")
        '文档分析：\\n- 标题层级：1 级标题: 1个\\n- 代码块：1个 (mermaid)\\n...'
    """
    try:
        if not markdown_text:
            return "提供的 Markdown 文本为空，无法分析。"

        logging.debug(f"Analyzing Markdown content of length {len(markdown_text)}")
        
        # 分析结果数据结构
        analysis = {
            "标题层级": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
            "段落数": 0,
            "链接数": 0,
            "图片数": 0,
            "代码块": {"总数": 0, "mermaid": 0},
            "表格数": 0,
            "列表数": {"有序": 0, "无序": 0},
            "总字数": len(markdown_text),
            "平均段落长度": 0,
        }
        
        # 记录当前是否在代码块中
        in_code_block = False
        code_block_type = ""
        paragraphs = []
        current_paragraph = ""
        
        # 逐行分析 Markdown
        lines = markdown_text.split('\n')
        for i, line in enumerate(lines):
            # 识别标题
            for h_level in range(6, 0, -1):
                prefix = '#' * h_level + ' '
                if line.startswith(prefix):
                    analysis["标题层级"][h_level] += 1
                    break
            
            # 识别代码块
            if line.startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    analysis["代码块"]["总数"] += 1
                    # 检查是否是 mermaid 图表
                    if line.startswith('```mermaid'):
                        analysis["代码块"]["mermaid"] += 1
                        code_block_type = "mermaid"
                else:
                    in_code_block = False
                    code_block_type = ""
                continue
            
            # 如果在代码块中，继续下一行
            if in_code_block:
                continue
                
            # 识别链接和图片
            analysis["链接数"] += line.count('](') - line.count('![')
            analysis["图片数"] += line.count('![')
            
            # 识别表格行
            if '|' in line and line.strip().startswith('|') and line.strip().endswith('|'):
                analysis["表格数"] = analysis.get("表格数", 0) + 1
            
            # 识别列表项
            stripped_line = line.strip()
            if stripped_line.startswith('- ') or stripped_line.startswith('* ') or stripped_line.startswith('+ '):
                analysis["列表数"]["无序"] += 1
            elif stripped_line and stripped_line[0].isdigit() and '. ' in stripped_line[:5]:
                analysis["列表数"]["有序"] += 1
            
            # 收集段落数据
            if line.strip():
                current_paragraph += line + " "
            elif current_paragraph:
                paragraphs.append(current_paragraph.strip())
                current_paragraph = ""
        
        # 添加最后一个段落
        if current_paragraph.strip():
            paragraphs.append(current_paragraph.strip())
        
        # 计算段落统计信息
        analysis["段落数"] = len(paragraphs)
        if paragraphs:
            paragraph_lengths = [len(p) for p in paragraphs]
            analysis["平均段落长度"] = sum(paragraph_lengths) / len(paragraphs)
        
        # 生成分析报告
        report = ["# Markdown 文档分析"]
        report.append("\n## 基本信息")
        report.append(f"- 总字数: {analysis['总字数']} 字")
        report.append(f"- 段落数: {analysis['段落数']} 个")
        if analysis['段落数'] > 0:
            report.append(f"- 平均段落长度: {analysis['平均段落长度']:.1f} 字")
        
        report.append("\n## 文档结构")
        headers = sum(analysis["标题层级"].values())
        if headers > 0:
            report.append("### 标题层级:")
            for level, count in analysis["标题层级"].items():
                if count > 0:
                    report.append(f"- {level} 级标题: {count} 个")
        else:
            report.append("- 未检测到标题")
        
        report.append("\n### 内容元素:")
        report.append(f"- 链接: {analysis['链接数']} 个")
        report.append(f"- 图片: {analysis['图片数']} 个")
        report.append(f"- 代码块: {analysis['代码块']['总数']} 个")
        if analysis['代码块']['mermaid'] > 0:
            report.append(f"  - 其中 Mermaid 图表: {analysis['代码块']['mermaid']} 个")
        report.append(f"- 表格: {analysis['表格数']} 个")
        report.append(f"- 列表: 有序 {analysis['列表数']['有序']} 个, 无序 {analysis['列表数']['无序']} 个")
        
        # 生成优化建议
        report.append("\n## 优化建议")
        if headers == 0:
            report.append("- 建议添加标题，以提高文档结构和导航性")
        if analysis["标题层级"][1] == 0:
            report.append("- 建议添加一个主标题（# 一级标题）")
        if analysis["标题层级"][1] > 1:
            report.append("- 文档中有多个一级标题，建议保持一个主标题，使用二级标题区分不同部分")
        
        if analysis['段落数'] > 0 and analysis['平均段落长度'] > 300:
            report.append("- 段落平均长度较长，考虑分割长段落以提高可读性")
        
        if analysis['链接数'] == 0 and analysis['总字数'] > 500:
            report.append("- 考虑添加相关参考链接，增加文档价值")
        
        report.append("\n## DOCX 转换建议")
        if analysis['代码块']['mermaid'] > 0:
            report.append("- Mermaid 图表将在转换时自动渲染为图片")
        if analysis['表格数'] > 0:
            report.append(f"- 检查表格格式是否规范，确保表格头与内容对齐")
        
        return "\n".join(report)
    except Exception as e:
        logging.error(f"Error analyzing Markdown: {e}")
        return f"分析 Markdown 时出错: {str(e)}"


@mcp.prompt("optimize_mermaid")
def optimize_mermaid_prompt(mermaid_code: str) -> str:
    """优化 Mermaid 图表代码并提供改进建议。
    
    这个提示函数接收 Mermaid 图表代码，分析其结构，并提供优化建议，
    如布局调整、样式改进等，帮助用户创建更清晰、更美观的图表。
    
    Args:
        mermaid_code: Mermaid 图表的代码（不包含 ```mermaid 标记）
        
    Returns:
        优化后的 Mermaid 代码和改进建议
        
    Examples:
        >>> optimize_mermaid_prompt("graph TD;\\nA-->B;")
        '优化建议：\\n1. 添加节点标题\\n2. 考虑使用颜色区分不同类型节点\\n\\n优化后的代码：\\ngraph TD;\\nA[开始] -->|处理| B[结束];'
    """
    try:
        if not mermaid_code or len(mermaid_code.strip()) < 5:
            return "提供的 Mermaid 代码为空或过短，无法分析。"

        logging.debug(f"Optimizing Mermaid diagram of length {len(mermaid_code)}")
        
        # 用于存储分析结果
        diagram_type = "未知"
        node_count = 0
        edge_count = 0
        has_styles = False
        has_titles = False
        suggestions = []
        optimized_code = mermaid_code
        
        # 尝试确定图表类型
        first_line = mermaid_code.strip().split('\n')[0].strip()
        if first_line.startswith('graph '):
            diagram_type = "流程图"
            # 检查方向
            direction = first_line[6:].strip().rstrip(';')
            if direction in ['TB', 'TD']:
                direction_desc = "从上到下"
            elif direction == 'BT':
                direction_desc = "从下到上"
            elif direction == 'RL':
                direction_desc = "从右到左"
            elif direction == 'LR':
                direction_desc = "从左到右"
            else:
                direction_desc = "未指定明确方向"
                suggestions.append("明确指定图表方向，如 `graph TD` 或 `graph LR`")
        elif first_line.startswith('sequenceDiagram'):
            diagram_type = "时序图"
        elif first_line.startswith('classDiagram'):
            diagram_type = "类图"
        elif first_line.startswith('stateDiagram'):
            diagram_type = "状态图"
        elif first_line.startswith('erDiagram'):
            diagram_type = "ER图"
        elif first_line.startswith('gantt'):
            diagram_type = "甘特图"
        elif first_line.startswith('pie'):
            diagram_type = "饼图"
        
        # 分析图表内容
        lines = mermaid_code.strip().split('\n')
        
        # 检查节点和边
        for line in lines[1:]:
            line = line.strip()
            if '-->' in line or '---' in line or '==>' in line or '-.->' in line:
                edge_count += 1
                
                # 检查边是否有标签
                if '|' in line and '|' in line.split('-->')[0]:
                    has_styles = True
                
                # 识别节点 ID
                parts = re.split(r'-->|---|\=\=>|-\.->|\-\-', line)
                for part in parts:
                    if part and part.strip():
                        node_id = part.strip().split('[')[0].split('(')[0].strip()
                        if node_id:
                            node_count += 1
                            
                # 检查节点是否有标题
                if '[' in line and ']' in line:
                    has_titles = True
            
            # 检查样式
            if 'style ' in line or 'class ' in line or 'classDef ' in line:
                has_styles = True
        
        # 生成特定类型图表的建议
        if diagram_type == "流程图":
            if not has_titles and node_count > 0:
                suggestions.append("为节点添加描述性标题，如 `A[开始]` 而不仅仅是 `A`")
                
                # 尝试优化代码 - 为节点添加简单标题
                new_lines = []
                for line in lines:
                    if '-->' in line:
                        parts = line.split('-->')
                        new_parts = []
                        for i, part in enumerate(parts):
                            if i < len(parts) - 1:
                                # 尝试为左侧添加标题
                                node_id = part.strip()
                                if '[' not in node_id and '(' not in node_id:
                                    placeholder = f"节点{node_id}"
                                    part = f"{node_id}[{placeholder}]"
                            new_parts.append(part)
                        new_line = '-->'.join(new_parts)
                        new_lines.append(new_line)
                    else:
                        new_lines.append(line)
                optimized_code = '\n'.join(new_lines)
            
            if not has_styles and node_count > 3:
                suggestions.append("考虑使用颜色和形状区分不同类型的节点，提高可读性")
                suggestions.append("为边添加描述性标签，如 `A -->|操作| B`")
                
                # 可以添加样式示例
                if len(lines) > 0 and diagram_type == "流程图":
                    style_example = """
classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
classDef important fill:#f96,stroke:#333,stroke-width:2px;
class NodeA,NodeB important;
"""
                    optimized_code += style_example
            
        elif diagram_type == "时序图":
            if node_count < 2:
                suggestions.append("时序图至少应包含两个参与者")
            if edge_count < 1:
                suggestions.append("添加参与者之间的消息交互")
            if "Note" not in mermaid_code:
                suggestions.append("考虑使用 Note 添加说明，如 `Note over A: 说明文字`")
        
        elif diagram_type == "甘特图":
            if "section" not in mermaid_code:
                suggestions.append("使用 section 将任务分组，提高可读性")
        
        # 通用的建议
        if node_count > 10 and diagram_type == "流程图":
            suggestions.append("节点数量较多，考虑将图表分解为多个子图表或使用子图（subgraph）")
        
        if edge_count > 15 and diagram_type == "流程图":
            suggestions.append("连接较多，可能导致图表复杂，考虑简化结构或分解为多个图表")
        
        # 根据分析生成报告
        report = [f"# Mermaid {diagram_type}分析与优化"]
        
        report.append("\n## 图表信息")
        if diagram_type == "流程图":
            report.append(f"- 图表类型: {diagram_type}")
            if 'direction_desc' in locals():
                report.append(f"- 方向: {direction_desc}")
        else:
            report.append(f"- 图表类型: {diagram_type}")
        
        report.append(f"- 节点数量: 约 {max(1, node_count // 2)} 个")
        report.append(f"- 连接数量: 约 {edge_count} 个")
        report.append(f"- 使用样式: {'是' if has_styles else '否'}")
        report.append(f"- 节点标题: {'已添加' if has_titles else '未添加'}")
        
        # 添加建议
        if suggestions:
            report.append("\n## 优化建议")
            for i, sugg in enumerate(suggestions, 1):
                report.append(f"{i}. {sugg}")
        else:
            report.append("\n## 优化建议")
            report.append("- 图表结构良好，无需重大修改")
        
        # DOCX 转换提示
        report.append("\n## DOCX 转换提示")
        report.append("- Mermaid 图表将在转换为 DOCX 时自动渲染为图片")
        report.append("- 确保图表方向和大小适合文档页面布局")
        if diagram_type == "流程图" and edge_count > 10:
            report.append("- 图表较复杂，在 DOCX 中可能需要调整页面布局以容纳")
        
        # 添加优化后的代码
        if optimized_code != mermaid_code:
            report.append("\n## 优化后的代码")
            report.append("```mermaid")
            report.append(optimized_code)
            report.append("```")
            report.append("\n*注：这只是一个优化建议，请根据实际需求调整*")
        
        return "\n".join(report)
    except Exception as e:
        logging.error(f"Error optimizing Mermaid diagram: {e}")
        import traceback
        traceback.print_exc()
        return f"优化 Mermaid 图表时出错: {str(e)}"


@mcp.tool()
async def md_to_docx_tool(
    md_content: str, 
    output_file: str = None, 
    debug_mode: bool = False, 
    table_style: str = 'Table Grid',
    mermaid_theme: str = 'default'
) -> str:
    """将Markdown文件转换为DOCX，并将Mermaid图表渲染为图片。
    
    Args:
        md_content: 要转换的Markdown内容
        output_file: 可选的输出文件路径，默认为'output.docx'
        debug_mode: 是否启用调试模式
        table_style: 表格样式，默认为'Table Grid'，可选值见下方列表
        mermaid_theme: Mermaid图表主题，默认为'default'，可选值：['default', 'dark', 'forest', 'ocean', 'elegant']
        
    Returns:
        保存的DOCX文件路径
        
    Table Styles:
        ['Normal Table', 'Table Grid', 'Light Shading', 'Light Shading Accent 1', 
         'Light Shading Accent 2', 'Light Shading Accent 3', 'Light Shading Accent 4', 
         'Light Shading Accent 5', 'Light Shading Accent 6', 'Light List', 
         'Light List Accent 1', 'Light List Accent 2', 'Light List Accent 3', 
         'Light List Accent 4', 'Light List Accent 5', 'Light List Accent 6', 
         'Light Grid', 'Light Grid Accent 1', 'Light Grid Accent 2', 
         'Light Grid Accent 3', 'Light Grid Accent 4', 'Light Grid Accent 5', 
         'Light Grid Accent 6', 'Medium Shading 1', 'Medium Shading 1 Accent 1', 
         'Medium Shading 1 Accent 2', 'Medium Shading 1 Accent 3', 
         'Medium Shading 1 Accent 4', 'Medium Shading 1 Accent 5', 
         'Medium Shading 1 Accent 6', 'Medium Shading 2', 'Medium Shading 2 Accent 1', 
         'Medium Shading 2 Accent 2', 'Medium Shading 2 Accent 3', 
         'Medium Shading 2 Accent 4', 'Medium Shading 2 Accent 5', 
         'Medium Shading 2 Accent 6', 'Medium List 1', 'Medium List 1 Accent 1', 
         'Medium List 1 Accent 2', 'Medium List 1 Accent 3', 'Medium List 1 Accent 4', 
         'Medium List 1 Accent 5', 'Medium List 1 Accent 6', 'Medium List 2', 
         'Medium List 2 Accent 1', 'Medium List 2 Accent 2', 'Medium List 2 Accent 3', 
         'Medium List 2 Accent 4', 'Medium List 2 Accent 5', 'Medium List 2 Accent 6', 
         'Medium Grid 1', 'Medium Grid 1 Accent 1', 'Medium Grid 1 Accent 2', 
         'Medium Grid 1 Accent 3', 'Medium Grid 1 Accent 4', 'Medium Grid 1 Accent 5', 
         'Medium Grid 1 Accent 6', 'Medium Grid 2', 'Medium Grid 2 Accent 1', 
         'Medium Grid 2 Accent 2', 'Medium Grid 2 Accent 3', 'Medium Grid 2 Accent 4', 
         'Medium Grid 2 Accent 5', 'Medium Grid 2 Accent 6', 'Medium Grid 3', 
         'Medium Grid 3 Accent 1', 'Medium Grid 3 Accent 2', 'Medium Grid 3 Accent 3', 
         'Medium Grid 3 Accent 4', 'Medium Grid 3 Accent 5', 'Medium Grid 3 Accent 6', 
         'Dark List', 'Dark List Accent 1', 'Dark List Accent 2', 'Dark List Accent 3', 
         'Dark List Accent 4', 'Dark List Accent 5', 'Dark List Accent 6', 
         'Colorful Shading', 'Colorful Shading Accent 1', 'Colorful Shading Accent 2', 
         'Colorful Shading Accent 3', 'Colorful Shading Accent 4', 
         'Colorful Shading Accent 5', 'Colorful Shading Accent 6', 'Colorful List', 
         'Colorful List Accent 1', 'Colorful List Accent 2', 'Colorful List Accent 3', 
         'Colorful List Accent 4', 'Colorful List Accent 5', 'Colorful List Accent 6', 
         'Colorful Grid', 'Colorful Grid Accent 1', 'Colorful Grid Accent 2', 
         'Colorful Grid Accent 3', 'Colorful Grid Accent 4', 'Colorful Grid Accent 5', 
         'Colorful Grid Accent 6']
    """
    return md_to_docx(md_content, output_file, debug_mode, table_style, mermaid_theme)


def serve():
    """Run the MCP server."""
    mcp.run(transport='stdio')


@click.group()
def cli():
    """MD to DOCX converter with Mermaid diagram support."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', type=str, help='Path to the output DOCX file (default: input_file_name.docx)')
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode')
@click.option('-t', '--table-style', type=str, default='Table Grid', 
              help='Style to apply to tables (default: Table Grid). Common styles include: Table Normal, Table Grid, Light Shading, Light List, Light Grid, Medium Shading 1, Medium Shading 2, etc.')
def convert(input_file, output, debug, table_style):
    """Convert Markdown file to DOCX file with Mermaid diagram support."""
    # Process input file path
    input_path = Path(input_file)
    
    # Determine output file path
    if output:
        output_path = output
    else:
        # Replace .md extension with .docx, or add .docx if no extension
        if input_path.suffix.lower() == '.md':
            output_path = str(input_path.with_suffix('.docx'))
        else:
            output_path = f"{input_file}.docx"
    
    try:
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        click.echo(f"Converting {input_file} to {output_path}...")
        click.echo(f"Using table style: {table_style}")
        
        # Convert to DOCX
        result = md_to_docx(md_content, output_path, debug, table_style)
        
        click.echo(f"Conversion completed successfully! Output file: {result}")
        return 0
    
    except Exception as e:
        click.echo(f"Error during conversion: {e}", err=True)
        import traceback
        traceback.print_exc()
        return 1


@cli.command()
@click.option("-v", "--verbose", count=True, help="Increase verbosity (can be used multiple times)")
def server(verbose):
    """Run as an MCP server."""
    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)
    # Don't use asyncio.run() here as mcp.run() handles the event loop itself
    serve()


def main():
    """Entry point for the application."""
    return cli()


if __name__ == "__main__":
    sys.exit(main()) 