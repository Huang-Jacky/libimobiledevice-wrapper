#!/usr/bin/env python3
"""
libimobiledevice-wrapper 使用示例
演示如何使用这个工具进行 iOS 设备管理
"""

import asyncio
import json
import time
from pathlib import Path

from libimobiledevice_wrapper import LibiMobileDevice, WebDriverAgent, LibiMobileDeviceError, WebDriverAgentError


def sync_example():
    """同步使用示例"""
    print("=== 同步使用示例 ===")

    try:
        # 创建设备实例
        device = LibiMobileDevice()

        # 列出连接的设备
        devices = device.list_devices()
        print(f"连接的设备: {devices}")

        if not devices:
            print("没有连接的设备")
            return

        udid = devices[0]
        print(f"使用设备: {udid}")

        # 获取设备信息
        info = device.get_device_info(udid)
        print(f"设备信息: {json.dumps(info, indent=2, ensure_ascii=False)}")

        # 列出已安装应用
        apps = device.list_apps(udid)
        print(f"已安装应用数量: {len(apps)}")

        # 显示前5个应用
        for i, app in enumerate(apps[:5], 1):
            print(f"{i}. {app['name']} ({app['bundle_id']})")

        # 获取设备日志（保存到文件）
        log_file = f"device_log_{udid}.log"
        device.get_device_logs(udid, output_file=log_file)
        print(f"设备日志已保存到: {log_file}")

    except LibiMobileDeviceError as e:
        print(f"操作失败: {e}")


async def async_example():
    """异步使用示例"""
    print("\n=== 异步使用示例 ===")

    try:
        # 创建设备实例
        device = LibiMobileDevice()

        # 异步列出设备
        devices = await device.list_devices_async()
        print(f"异步发现的设备: {devices}")

        if not devices:
            print("没有连接的设备")
            return

        udid = devices[0]

        # 异步获取设备信息
        info = await device.get_device_info_async(udid)
        print(f"异步获取的设备信息: {json.dumps(info, indent=2, ensure_ascii=False)}")

        # 异步列出应用
        apps = await device.list_apps_async(udid)
        print(f"异步获取的应用数量: {len(apps)}")

    except LibiMobileDeviceError as e:
        print(f"异步操作失败: {e}")


async def webdriveragent_example():
    """WebDriverAgent 使用示例"""
    print("\n=== WebDriverAgent 使用示例 ===")

    try:
        # 获取设备 UDID
        device = LibiMobileDevice()
        devices = device.list_devices()

        if not devices:
            print("没有连接的设备")
            return

        udid = devices[0]

        # 创建 WebDriverAgent 实例
        wda = WebDriverAgent(udid)

        async with wda:
            # 创建会话
            session_id = await wda.create_session()
            print(f"WebDriver 会话已创建: {session_id}")

            # 获取会话信息
            session_info = await wda.get_session_info()
            print(f"会话信息: {json.dumps(session_info, indent=2, ensure_ascii=False)}")

            # 获取窗口大小
            window_size = await wda.get_window_size()
            print(f"窗口大小: {window_size}")

            # 获取当前活动应用
            active_app = await wda.get_active_app()
            print(f"当前活动应用: {active_app}")

            # 截取屏幕截图
            screenshot = await wda.screenshot()
            screenshot_file = f"screenshot_{udid}.png"
            with open(screenshot_file, 'wb') as f:
                f.write(screenshot)
            print(f"屏幕截图已保存到: {screenshot_file}")

            # 点击屏幕中心
            if window_size:
                center_x = window_size.get('width', 0) // 2
                center_y = window_size.get('height', 0) // 2
                await wda.tap(center_x, center_y)
                print(f"已点击屏幕中心: ({center_x}, {center_y})")

            # 按下 Home 键
            await wda.press_home()
            print("已按下 Home 键")

    except WebDriverAgentError as e:
        print(f"WebDriverAgent 操作失败: {e}")
    except LibiMobileDeviceError as e:
        print(f"设备操作失败: {e}")


def app_management_example():
    """应用管理示例"""
    print("\n=== 应用管理示例 ===")

    try:
        device = LibiMobileDevice()
        devices = device.list_devices()

        if not devices:
            print("没有连接的设备")
            return

        udid = devices[0]

        # 列出所有应用
        apps = device.list_apps(udid)
        print(f"设备上已安装 {len(apps)} 个应用")

        # 查找系统应用
        system_apps = [app for app in apps if app['bundle_id'].startswith('com.apple.')]
        print(f"系统应用: {len(system_apps)} 个")

        # 查找第三方应用
        third_party_apps = [app for app in apps if not app['bundle_id'].startswith('com.apple.')]
        print(f"第三方应用: {len(third_party_apps)} 个")

        # 显示一些第三方应用
        if third_party_apps:
            print("\n第三方应用示例:")
            for app in third_party_apps[:5]:
                print(f"- {app['name']} ({app['bundle_id']})")

        # 获取指定应用的详细信息
        if third_party_apps:
            test_app = third_party_apps[0]
            print(f"\n获取应用详细信息: {test_app['name']}")
            try:
                app_info = device.get_app_info(udid, test_app['bundle_id'])
                if 'error' not in app_info:
                    print(f"应用名称: {app_info.get('CFBundleDisplayName', 'N/A')}")
                    print(f"版本号: {app_info.get('CFBundleShortVersionString', 'N/A')}")
                    print(f"构建版本: {app_info.get('CFBundleVersion', 'N/A')}")
                    print(f"可执行文件: {app_info.get('CFBundleExecutable', 'N/A')}")
                    print(f"最低系统版本: {app_info.get('MinimumOSVersion', 'N/A')}")
                else:
                    print(f"获取应用信息失败: {app_info['error']}")
            except LibiMobileDeviceError as e:
                print(f"获取应用信息失败: {e}")

        # 尝试启动一个应用（如果存在）
        if third_party_apps:
            test_app = third_party_apps[0]
            print(f"\n尝试启动应用: {test_app['name']}")
            try:
                device.launch_app(udid, test_app['bundle_id'])
                print("应用启动成功")
            except LibiMobileDeviceError as e:
                print(f"应用启动失败: {e}")

    except LibiMobileDeviceError as e:
        print(f"应用管理操作失败: {e}")


def app_logs_example():
    """应用日志示例"""
    print("\n=== 应用日志示例 ===")

    try:
        device = LibiMobileDevice()
        devices = device.list_devices()

        if not devices:
            print("没有连接的设备")
            return

        udid = devices[0]

        # 列出应用
        apps = device.list_apps(udid)
        third_party_apps = [app for app in apps if not app['bundle_id'].startswith('com.apple.')]

        if not third_party_apps:
            print("没有找到第三方应用")
            return

        test_app = third_party_apps[0]
        bundle_id = test_app['bundle_id']

        print(f"测试应用: {test_app['name']} ({bundle_id})")

        # 获取应用日志（30秒，包含错误关键字）
        print("\n获取应用日志（30秒，过滤错误信息）...")
        logs = device.get_device_logs(udid, duration=30, keywords=['error', 'Error', 'exception'])

        if logs:
            print(f"发现 {len(logs)} 条匹配的日志:")
            for i, log in enumerate(logs[:10], 1):  # 只显示前10条
                print(f"{i}. [{log['level']}] {log['message']}")

            if len(logs) > 10:
                print(f"... 还有 {len(logs) - 10} 条日志")
        else:
            print("未发现匹配的日志")

        # 保存日志到文件
        log_file = f"app_logs_{bundle_id.replace('.', '_')}.log"
        device.get_device_logs(udid, duration=10, keywords=['error', 'Error'], output_file=log_file)
        print(f"日志已保存到: {log_file}")

    except LibiMobileDeviceError as e:
        print(f"应用日志操作失败: {e}")


def file_operations_example():
    """文件操作示例"""
    print("\n=== 文件操作示例 ===")

    try:
        device = LibiMobileDevice()
        devices = device.list_devices()

        if not devices:
            print("没有连接的设备")
            return

        udid = devices[0]

        # 创建测试文件
        test_file = Path("test_file.txt")
        test_content = f"这是测试文件，创建时间: {time.time()}"
        test_file.write_text(test_content, encoding='utf-8')

        # 推送文件到设备
        remote_path = "/tmp/test_file.txt"
        device.push_file(udid, test_file, remote_path)
        print(f"文件已推送到设备: {test_file} -> {remote_path}")

        # 从设备拉取文件
        local_backup = f"backup_{udid}_test_file.txt"
        device.pull_file(udid, remote_path, local_backup)
        print(f"文件已从设备拉取: {remote_path} -> {local_backup}")

        # 验证文件内容
        if Path(local_backup).exists():
            content = Path(local_backup).read_text(encoding='utf-8')
            print(f"拉取的文件内容: {content}")
            Path(local_backup).unlink()  # 清理

        # 清理测试文件
        test_file.unlink()

    except LibiMobileDeviceError as e:
        print(f"文件操作失败: {e}")


def device_logs_example():
    """设备日志监控示例"""
    print("\n=== 设备日志监控示例 ===")

    try:
        device = LibiMobileDevice()
        devices = device.list_devices()

        if not devices:
            print("没有连接的设备")
            return

        udid = devices[0]

        # 方法1：使用简洁的日志捕获API
        print("使用简洁的日志捕获API（10秒）...")
        log_file = f"device_logs_{udid}.log"

        with device.monitor_device_logs(
                udid=udid,
                keywords=["error", "Error"],
                log_file_path=log_file,
                duration=10
        ) as monitor:
            print("正在监控设备日志...")
            import time
            time.sleep(5)  # 监控5秒
            print(f"已捕获 {len(monitor.get_logs())} 条日志")

        print(f"日志已保存到: {log_file}")

        # 方法2：使用实时监控
        print("\n使用实时监控（5秒）...")
        monitor = device.monitor_device_logs(udid, keywords=["error", "Error"])
        monitor.start()

        import time
        time.sleep(5)
        monitor.stop()

        logs = monitor.get_logs()
        print(f"实时监控捕获了 {len(logs)} 条日志")

        if logs:
            print("最近的日志:")
            for log in logs[-3:]:  # 显示最后3条
                print(f"- [{log['level']}] {log['message'][:100]}...")

    except LibiMobileDeviceError as e:
        print(f"设备日志监控失败: {e}")


def system_operations_example():
    """系统操作示例"""
    print("\n=== 系统操作示例 ===")

    try:
        device = LibiMobileDevice()
        devices = device.list_devices()

        if not devices:
            print("没有连接的设备")
            return

        udid = devices[0]

        # 获取设备属性
        print("获取设备属性...")
        props = device.get_device_props(udid)
        print(f"设备属性: {json.dumps(props, indent=2, ensure_ascii=False)}")

        # 注意：重启和关机操作会实际执行，这里只演示API调用
        print("\n⚠️  以下操作会实际执行，请谨慎使用:")
        print("device.reboot_device(udid)  # 重启设备")
        print("device.shutdown_device(udid)  # 关机设备")

        # 如果需要实际测试，取消注释下面的代码
        # print("重启设备...")
        # device.reboot_device(udid)
        # print("设备重启命令已发送")

    except LibiMobileDeviceError as e:
        print(f"系统操作失败: {e}")


def app_install_uninstall_example():
    """应用安装/卸载示例"""
    print("\n=== 应用安装/卸载示例 ===")

    try:
        device = LibiMobileDevice()
        devices = device.list_devices()

        if not devices:
            print("没有连接的设备")
            return

        udid = devices[0]

        # 列出当前应用
        apps = device.list_apps(udid)
        third_party_apps = [app for app in apps if not app['bundle_id'].startswith('com.apple.')]

        print(f"当前已安装 {len(third_party_apps)} 个第三方应用")

        if third_party_apps:
            # 选择一个应用进行测试
            test_app = third_party_apps[0]
            bundle_id = test_app['bundle_id']

            print(f"\n测试应用: {test_app['name']} ({bundle_id})")

            # 注意：卸载操作会实际执行，这里只演示API调用
            print("⚠️  卸载操作会实际执行，请谨慎使用:")
            print(f"device.uninstall_app(udid, '{bundle_id}')")

            # 如果需要实际测试，取消注释下面的代码
            # print("卸载应用...")
            # device.uninstall_app(udid, bundle_id)
            # print("应用卸载命令已发送")

        # 安装应用示例（需要实际的 .ipa 文件）
        print("\n安装应用示例:")
        print("device.install_app(udid, '/path/to/app.ipa')")

    except LibiMobileDeviceError as e:
        print(f"应用安装/卸载操作失败: {e}")


def cli_commands_example():
    """CLI 命令使用示例"""
    print("\n=== CLI 命令使用示例 ===")

    print("以下是可用的命令行工具:")
    print()

    print("1. 设备管理:")
    print("   libidevice list-devices                    # 列出设备")
    print("   libidevice info --udid <udid>              # 获取设备信息")
    print("   libidevice apps --udid <udid>              # 列出应用")
    print()

    print("2. 应用管理:")
    print("   libidevice install --udid <udid> <app.ipa> # 安装应用")
    print("   libidevice uninstall --udid <udid> <bundle_id> # 卸载应用")
    print("   libidevice app-info --udid <udid> <bundle_id>  # 获取应用信息")
    print("   libidevice launch --udid <udid> <bundle_id>   # 启动应用")
    print()

    print("3. 文件操作:")
    print("   libidevice pull --udid <udid> <remote> <local>  # 拉取文件")
    print("   libidevice push --udid <udid> <local> <remote>  # 推送文件")
    print()

    print("4. 日志监控:")
    print("   libidevice device-logs --udid <udid> --keywords 'ERROR' --output logs.txt")
    print("   libidevice device-logs --udid <udid> --duration 30 --keywords 'error'")
    print()

    print("5. 系统操作:")
    print("   libidevice reboot --udid <udid>            # 重启设备")
    print("   libidevice shutdown --udid <udid>          # 关机设备")
    print()

    print("6. 模块方式使用:")
    print("   python3 -m libimobiledevice_wrapper.cli <command>")


async def main():
    """主函数"""
    print("libimobiledevice-wrapper 使用示例")
    print("=" * 50)

    # 同步示例
    sync_example()

    # 异步示例
    await async_example()

    # WebDriverAgent 示例
    await webdriveragent_example()

    # 应用管理示例
    app_management_example()

    # 应用日志示例
    app_logs_example()

    # 文件操作示例
    file_operations_example()

    # 设备日志监控示例
    device_logs_example()

    # 系统操作示例
    system_operations_example()

    # 应用安装/卸载示例
    app_install_uninstall_example()

    # CLI 命令示例
    cli_commands_example()

    print("\n所有示例执行完成!")


if __name__ == "__main__":
    asyncio.run(main())
