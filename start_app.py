#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Image PDF Processor Startup Script
"""

import sys
import os

def check_dependencies():
    """Check if dependencies are installed"""
    try:
        import tkinter
        print("✓ tkinter 已安装")
    except ImportError:
        print("✗ tkinter 未安装，请安装 tkinter")
        return False
    
    try:
        from PIL import Image
        print("✓ Pillow 已安装")
    except ImportError:
        print("✗ Pillow 未安装，请运行: pip install Pillow")
        return False
    
    try:
        import PyPDF2
        print("✓ PyPDF2 已安装")
    except ImportError:
        print("✗ PyPDF2 未安装，请运行: pip install PyPDF2")
        return False
    
    return True

def main():
    print("=" * 50)
    print("图片PDF处理工具启动检查")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3:
        print("警告: 建议使用Python 3.x版本")
    
    # Check dependencies
    print("\n检查依赖包:")
    if not check_dependencies():
        print("\n请先安装缺失的依赖包，然后重新运行程序")
        input("按回车键退出...")
        return
    
    print("\n所有依赖检查通过！")
    print("正在启动图片PDF处理工具...")
    
    # Start main program
    try:
        from image_pdf_processor import main as app_main
        app_main()
    except Exception as e:
        print(f"启动程序时出错: {e}")
        input("按回车键退出...")

if __name__ == "__main__":
    main()
