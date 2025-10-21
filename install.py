#!/usr/bin/env python3
"""
安装脚本
检查依赖并安装 libimobiledevice-wrapper
"""

import subprocess
import sys
import platform
from pathlib import Path


def check_libimobiledevice():
    """检查 libimobiledevice 是否已安装"""
    print("检查 libimobiledevice...")
    
    try:
        # 检查 idevice_id 命令
        result = subprocess.run(
            ["idevice_id", "--help"], 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        
        if result.returncode == 0:
            print("✓ libimobiledevice 已安装")
            return True
        else:
            print("✗ libimobiledevice 未正确安装")
            return False
            
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        print("✗ libimobiledevice 未安装")
        return False


def install_libimobiledevice():
    """安装 libimobiledevice"""
    print("\n安装 libimobiledevice...")
    
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        print("检测到 macOS 系统")
        print("请运行以下命令安装 libimobiledevice:")
        print("brew install libimobiledevice")
        
    elif system == "linux":
        print("检测到 Linux 系统")
        
        # 检查包管理器
        if Path("/usr/bin/apt-get").exists():
            print("检测到 apt 包管理器")
            print("请运行以下命令安装 libimobiledevice:")
            print("sudo apt-get update")
            print("sudo apt-get install libimobiledevice6 libimobiledevice-utils")
            
        elif Path("/usr/bin/yum").exists():
            print("检测到 yum 包管理器")
            print("请运行以下命令安装 libimobiledevice:")
            print("sudo yum install libimobiledevice")
            
        elif Path("/usr/bin/dnf").exists():
            print("检测到 dnf 包管理器")
            print("请运行以下命令安装 libimobiledevice:")
            print("sudo dnf install libimobiledevice")
            
        else:
            print("未检测到支持的包管理器")
            print("请手动安装 libimobiledevice")
            
    elif system == "windows":
        print("检测到 Windows 系统")
        print("Windows 系统需要手动安装 libimobiledevice")
        print("请访问: https://github.com/libimobiledevice/libimobiledevice")
        
    else:
        print(f"不支持的系统: {system}")
        print("请手动安装 libimobiledevice")


def install_python_package():
    """安装 Python 包"""
    print("\n安装 Python 包...")
    
    try:
        # 检查是否在开发模式下安装
        if Path("pyproject.toml").exists():
            print("检测到开发环境，使用开发模式安装...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)
        else:
            print("使用 pip 安装包...")
            subprocess.run([sys.executable, "-m", "pip", "install", "libimobiledevice-wrapper"], check=True)
        
        print("✓ Python 包安装成功")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Python 包安装失败: {e}")
        return False


def check_python_dependencies():
    """检查 Python 依赖"""
    print("\n检查 Python 依赖...")
    
    required_packages = [
        "click",
        "aiofiles", 
        "rich",
        "aiohttp"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n缺少依赖包: {', '.join(missing_packages)}")
        print("正在安装...")
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install"
            ] + missing_packages, check=True)
            print("✓ 依赖包安装成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ 依赖包安装失败: {e}")
            return False
    
    return True


def test_installation():
    """测试安装"""
    print("\n测试安装...")
    
    try:
        # 测试导入
        from libimobiledevice_wrapper import LibiMobileDevice
        print("✓ 模块导入成功")
        
        # 测试基本功能
        device = LibiMobileDevice()
        devices = device.list_devices()
        print(f"✓ 设备检测成功，发现 {len(devices)} 个设备")
        
        # 测试 CLI
        result = subprocess.run(["libidevice", "--help"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ CLI 工具可用")
        else:
            print("✗ CLI 工具不可用")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False


def main():
    """主函数"""
    print("libimobiledevice-wrapper 安装脚本")
    print("=" * 40)
    
    # 检查 libimobiledevice
    if not check_libimobiledevice():
        install_libimobiledevice()
        print("\n请先安装 libimobiledevice，然后重新运行此脚本")
        return
    
    # 检查 Python 依赖
    if not check_python_dependencies():
        print("\n依赖检查失败，请手动安装缺少的包")
        return
    
    # 安装 Python 包
    if not install_python_package():
        print("\nPython 包安装失败")
        return
    
    # 测试安装
    if test_installation():
        print("\n🎉 安装完成！")
        print("\n使用方法:")
        print("1. 命令行工具: libidevice --help")
        print("2. Python 代码:")
        print("   from libimobiledevice_wrapper import LibiMobileDevice")
        print("   device = LibiMobileDevice()")
        print("   devices = device.list_devices()")
    else:
        print("\n❌ 安装测试失败，请检查错误信息")


if __name__ == "__main__":
    main()
