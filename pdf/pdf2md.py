#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF转Markdown工具
将PDF文件转换为Markdown格式，提取图片并保存到单独的文件夹
"""

import os
import re
import fitz  # PyMuPDF
from PIL import Image
import io
from pathlib import Path


def extract_images_from_page(page, page_num, images_dir):
    """
    从PDF页面中提取图片并保存
    
    Args:
        page: fitz页面对象
        page_num: 页码
        images_dir: 图片保存目录
        
    Returns:
        dict: 图片索引到保存路径的映射
    """
    image_map = {}
    image_list = page.get_images(full=True)
    
    for img_index, img_info in enumerate(image_list):
        xref = img_info[0]
        
        try:
            # 提取图片
            base_image = page.parent.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # 生成图片文件名
            img_filename = f"page{page_num}_img{img_index + 1}.{image_ext}"
            img_path = images_dir / img_filename
            
            # 保存图片
            with open(img_path, "wb") as img_file:
                img_file.write(image_bytes)
            
            # 记录图片位置信息
            image_map[xref] = {
                "path": img_path.name,
                "width": base_image.get("width", 0),
                "height": base_image.get("height", 0)
            }
            
        except Exception as e:
            print(f"警告: 提取图片 {img_index} 失败: {e}")
            
    return image_map


def get_text_with_image_positions(page):
    """
    获取文本内容，并记录图片的位置信息以便插入
    
    Args:
        page: fitz页面对象
        
    Returns:
        list: 按位置排序的内容块列表 (文本或图片)
    """
    blocks = []
    
    # 获取文本块
    text_dict = page.get_text("dict")
    
    for block in text_dict.get("blocks", []):
        if block.get("type") == 0:  # 文本块
            text_lines = []
            for line in block.get("lines", []):
                line_text = ""
                for span in line.get("spans", []):
                    line_text += span.get("text", "")
                if line_text.strip():
                    text_lines.append(line_text)
            
            if text_lines:
                blocks.append({
                    "type": "text",
                    "y": block.get("bbox", [0, 0, 0, 0])[1],  # Y坐标用于排序
                    "content": "\n".join(text_lines)
                })
    
    # 获取图片信息
    image_list = page.get_images(full=True)
    for img_index, img_info in enumerate(image_list):
        xref = img_info[0]
        # 获取图片在页面上的位置
        img_rects = page.get_image_rects(xref)
        if img_rects:
            for rect in img_rects:
                blocks.append({
                    "type": "image",
                    "y": rect.y0,
                    "xref": xref
                })
    
    # 按Y坐标排序
    blocks.sort(key=lambda x: x["y"])
    
    return blocks


def convert_page_to_markdown(page, page_num, images_dir):
    """
    将单个PDF页面转换为Markdown格式
    
    Args:
        page: fitz页面对象
        page_num: 页码
        images_dir: 图片保存目录
        
    Returns:
        str: Markdown格式的页面内容
    """
    # 提取图片
    image_map = extract_images_from_page(page, page_num, images_dir)
    
    # 获取带位置信息的内容块
    blocks = get_text_with_image_positions(page)
    
    # 构建Markdown内容
    md_lines = []
    md_lines.append(f"\n## 第 {page_num} 页\n")
    
    # 用于跟踪已处理的图片xref
    processed_xrefs = set()
    
    for block in blocks:
        if block["type"] == "text":
            text = block["content"].strip()
            if text:
                md_lines.append(text)
                md_lines.append("")
        elif block["type"] == "image":
            xref = block["xref"]
            if xref in image_map and xref not in processed_xrefs:
                img_info = image_map[xref]
                img_path = f"images/{img_info['path']}"
                md_lines.append(f"\n![图片](./{img_path})\n")
                processed_xrefs.add(xref)
    
    return "\n".join(md_lines)


def pdf_to_markdown(pdf_path, output_dir=None):
    """
    将PDF文件转换为Markdown文件
    
    Args:
        pdf_path: PDF文件路径
        output_dir: 输出目录，默认为PDF文件所在目录
        
    Returns:
        str: 生成的Markdown文件路径
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
    
    # 设置输出目录
    if output_dir is None:
        output_dir = pdf_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建图片保存目录
    pdf_name = pdf_path.stem
    images_dir = output_dir / f"{pdf_name}_images"
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # 打开PDF文件
    print(f"正在处理: {pdf_path.name}")
    doc = fitz.open(str(pdf_path))
    
    try:
        # 提取文档标题和基本信息
        md_content = []
        md_content.append(f"# {pdf_name}\n")
        md_content.append(f"*转换自: {pdf_path.name}*\n")
        md_content.append(f"*总页数: {doc.page_count}*\n")
        md_content.append("---\n")
        
        # 处理每一页
        for page_num in range(doc.page_count):
            page = doc[page_num]
            print(f"  处理第 {page_num + 1}/{doc.page_count} 页...")
            
            page_md = convert_page_to_markdown(page, page_num + 1, images_dir)
            md_content.append(page_md)
        
        # 生成输出文件名
        output_file = output_dir / f"{pdf_name}.md"
        
        # 写入Markdown文件
        full_content = "\n".join(md_content)
        
        # 清理多余的空行
        full_content = re.sub(r'\n{3,}', '\n\n', full_content)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(full_content)
        
        print(f"\n转换完成!")
        print(f"  Markdown文件: {output_file}")
        print(f"  图片目录: {images_dir}")
        
        return str(output_file)
        
    finally:
        doc.close()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="将PDF文件转换为Markdown格式")
    parser.add_argument("pdf_file", help="要转换的PDF文件路径")
    parser.add_argument("-o", "--output", help="输出目录（默认为PDF文件所在目录）")
    
    args = parser.parse_args()
    
    pdf_to_markdown(args.pdf_file, args.output)


if __name__ == "__main__":
    # 默认处理指定的PDF文件
    pdf_file = "/Users/baoyang/Documents/coding/github_self/python-script/pdf/iOS考研科目时间规划App开发文档.pdf"
    pdf_to_markdown(pdf_file)