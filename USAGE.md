# 使用说明

## 快速开始

### 1. 安装依赖

首先确保系统已安装 libimobiledevice：

```bash
# macOS
brew install libimobiledevice

# Ubuntu/Debian
sudo apt-get install libimobiledevice6 libimobiledevice-utils
```

### 2. 安装 Python 包

```bash
# 开发模式安装
pip install -e .

# 或使用安装脚本
python install.py
```

### 3. 基本使用

#### 命令行工具

```bash
# 列出连接的设备
python3 -m libimobiledevice_wrapper.cli list-devices

# 获取设备信息
python3 -m libimobiledevice_wrapper.cli info --udid <device_udid>

# 获取设备信息（JSON格式）
python3 -m libimobiledevice_wrapper.cli info --udid <device_udid> --json

# 列出已安装应用
python3 -m libimobiledevice_wrapper.cli apps --udid <device_udid>

# 安装应用
python3 -m libimobiledevice_wrapper.cli install --udid <device_udid> /path/to/app.ipa

# 获取应用详细信息
python3 -m libimobiledevice_wrapper.cli app-info --udid <device_udid> --bundle-id com.example.app

# 获取设备日志
python3 -m libimobiledevice_wrapper.cli device-logs --udid <device_udid> --duration 60 --keywords "error,exception"

# 实时监控设备日志
python3 -m libimobiledevice_wrapper.cli device-logs --udid <device_udid> --keywords "error"

# 卸载应用
python3 -m libimobiledevice_wrapper.cli uninstall --udid <device_udid> --bundle-id com.example.app

# 从设备拉取文件
python3 -m libimobiledevice_wrapper.cli pull --udid <device_udid> --remote-path /path/on/device --local-path /local/path

# 推送文件到设备
python3 -m libimobiledevice_wrapper.cli push --udid <device_udid> --local-path /local/file --remote-path /path/on/device

# 重启设备
python3 -m libimobiledevice_wrapper.cli reboot --udid <device_udid>

# 关机设备
python3 -m libimobiledevice_wrapper.cli shutdown --udid <device_udid>

# 获取设备日志
python3 -m libimobiledevice_wrapper.cli device-logs --udid <device_udid> --duration 60 --keywords "error,exception"

# 实时监控设备日志
python3 -m libimobiledevice_wrapper.cli device-logs --udid <device_udid> --keywords "error"

# 异步命令
python3 -m libimobiledevice_wrapper.cli async-cmd info --udid <device_udid>
python3 -m libimobiledevice_wrapper.cli async-cmd app-info --udid <device_udid> --bundle-id com.example.app
python3 -m libimobiledevice_wrapper.cli async-cmd install --udid <device_udid> --app-path /path/to/app.ipa
```

#### Python API

```python
from libimobiledevice_wrapper import LibiMobileDevice

# 同步使用
device = LibiMobileDevice()
devices = device.list_devices()
print(f"连接的设备: {devices}")

# 异步使用
import asyncio

async def main():
    device = LibiMobileDevice()
    devices = await device.list_devices_async()
    print(f"连接的设备: {devices}")
    
    # 获取应用详细信息
    if devices:
        udid = devices[0]
        
        # 获取设备信息
        device_info = await device.get_device_info_async(udid)
        print(f"设备信息: {device_info['DeviceName']}")
        
        # 列出已安装应用
        apps = await device.list_apps_async(udid)
        print(f"已安装应用: {len(apps)} 个")
        
        if apps:
            # 获取应用详细信息
            app_info = await device.get_app_info_async(udid, apps[0]['bundle_id'])
            print(f"应用信息: {app_info['CFBundleName']}")
            
            # 获取设备日志
            logs = await device.get_device_logs_async(udid, duration=30, keywords=['error'])
            print(f"设备日志: {len(logs)} 条")
            
            # 简洁日志捕获
            monitor = device.monitor_device_logs(
                udid, 
                keywords=['error'],
                log_file_path="device_logs.txt",
                duration=30  # 30秒后自动停止
            )
            monitor.start()
            time.sleep(20)  # 捕获20秒
            monitor.stop()  # 自动保存到文件
            print(f"日志已保存，共 {len(monitor.get_logs())} 条")
            
            # 或使用上下文管理器
            with device.monitor_device_logs(udid, keywords=['error'], log_file_path="auto_logs.txt") as auto_monitor:
                time.sleep(15)
            # 自动停止并保存

## API 文档

### LibiMobileDevice 类

主要的设备管理类，提供所有 libimobiledevice 功能的封装。

#### 设备管理

- `list_devices()` / `list_devices_async()` - 列出连接的设备
- `get_device_info(udid)` / `get_device_info_async(udid)` - 获取设备信息
- `get_device_props(udid)` / `get_device_props_async(udid)` - 获取设备属性

#### 应用管理

- `install_app(udid, app_path)` / `install_app_async(udid, app_path)` - 安装应用
- `uninstall_app(udid, bundle_id)` / `uninstall_app_async(udid, bundle_id)` - 卸载应用
- `list_apps(udid)` / `list_apps_async(udid)` - 列出已安装应用
- `get_app_info(udid, bundle_id)` / `get_app_info_async(udid, bundle_id)` - 获取指定应用的详细信息
- `launch_app(udid, bundle_id)` / `launch_app_async(udid, bundle_id)` - 启动应用

#### 文件操作

- `pull_file(udid, remote_path, local_path)` / `pull_file_async(udid, remote_path, local_path)` - 从设备拉取文件
- `push_file(udid, local_path, remote_path)` / `push_file_async(udid, local_path, remote_path)` - 推送文件到设备

#### 系统操作

- `reboot_device(udid)` / `reboot_device_async(udid)` - 重启设备
- `shutdown_device(udid)` / `shutdown_device_async(udid)` - 关机设备

#### 简洁日志捕获

- `monitor_device_logs(udid, keywords, callback, log_file_path, duration)` - 设备日志监控
  - 自动保存到文件，无需手动调用 save_logs
  - 支持关键字过滤
  - 支持指定时长自动停止
  - 支持上下文管理器

### 错误处理

所有方法都包含统一的错误处理：

```python
from libimobiledevice_wrapper import LibiMobileDeviceError

try:
    device = LibiMobileDevice()
    devices = device.list_devices()
except LibiMobileDeviceError as e:
    print(f"设备操作失败: {e}")
```

### 异步支持

所有方法都提供异步版本：

```python
import asyncio
from libimobiledevice_wrapper import LibiMobileDevice

async def main():
    device = LibiMobileDevice()
    
    # 异步方法以 _async 结尾
    devices = await device.list_devices_async()
    info = await device.get_device_info_async(devices[0])
    
asyncio.run(main())
```

#### WebDriverAgent 支持

```python
from libimobiledevice_wrapper import WebDriverAgent

async def wda_example():
    wda = WebDriverAgent(device_udid="<device_udid>")
    
    async with wda:
        # 创建会话
        session_id = await wda.create_session()
        
        # 截取屏幕截图
        screenshot = await wda.screenshot()
        
        # 点击屏幕
        await wda.tap(100, 200)
        
        # 启动应用
        await wda.launch_app("com.example.app")

asyncio.run(wda_example())
```

## 开发

### 运行测试

```bash
# 基本测试
python libimobiledevice_wrapper/tests.py

# 使用 pytest
pytest libimobiledevice_wrapper/tests.py -v
```

### 代码格式化

```bash
black libimobiledevice_wrapper/
```

### 运行示例

```bash
python example.py
```

## 故障排除

### 常见问题

1. **libimobiledevice 未找到**
   - 确保已安装 libimobiledevice
   - 检查 PATH 环境变量

2. **设备未连接**
   - 确保设备已通过 USB 连接
   - 检查设备是否信任计算机
   - 尝试重新插拔 USB 线

3. **权限问题**
   - macOS: 确保在系统偏好设置中允许终端访问设备
   - Linux: 可能需要添加 udev 规则

4. **WebDriverAgent 连接失败**
   - 确保 WebDriverAgent 已启动
   - 检查端口是否正确
   - 确保设备已解锁

### 调试

启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from libimobiledevice_wrapper import LibiMobileDevice
device = LibiMobileDevice()
```
