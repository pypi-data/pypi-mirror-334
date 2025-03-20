import ctypes
import subprocess
import platform
import sys
import threading
import time
import urllib.parse  # 修改导入方式
from det_cli.protocol_handler import handle_protocol
# 全局协议名称变量
PROTOCOL_NAME = "det-cli"

import platform
import ctypes
import os
import logging
# ANSI 颜色代码（仅适用于支持 ANSI 的终端，如 Windows Terminal、PowerShell 7+）
LOG_COLORS = {
    "DEBUG": "\033[37m",    # 白色
    "INFO": "\033[32m",     # 绿色
    "WARNING": "\033[33m",  # 黄色
    "ERROR": "\033[31m",    # 红色
    "CRITICAL": "\033[41m", # 红色背景
    "RESET": "\033[0m"      # 重置颜色
}

class ColorFormatter(logging.Formatter):
    def format(self, record):
        log_color = LOG_COLORS.get(record.levelname, LOG_COLORS["RESET"])
        log_msg = super().format(record)
        return f"{log_color}{log_msg}{LOG_COLORS['RESET']}"

formatter = ColorFormatter("[%(levelname)s]%(asctime)s: %(message)s", datefmt="%H:%M:%S")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger = logging.getLogger()
if logger.hasHandlers():
    logger.handlers.clear()
logger.setLevel(logging.INFO)  # 设置日志级别
logger.addHandler(console_handler)
def is_admin():
    """检查当前用户是否有管理员权限"""
    if platform.system() == 'Windows':
        # Windows上检查管理员权限
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    elif platform.system() == 'Darwin':
        # macOS上检查管理员权限 (通过检查UID是否为0)
        return os.geteuid() == 0
    else:
        # 其他操作系统返回False
        return False



def register_protocol():
    if platform.system() == 'Windows':
        logging.info("此脚本正在注册 Windows 协议...")

        # 请求管理员权限
        if not is_admin():
            logging.error("当前没有管理员权限，请使用管理员权限重新运行。")
            return

        python_path = sys.executable  # 使用当前环境的 Python 解释器
        script_path = __file__  # 获取当前脚本路径

        # 注册协议到 Windows 注册表
        reg_path = rf"HKEY_CLASSES_ROOT\{PROTOCOL_NAME}"

        reg_command = f"reg add {reg_path} /ve /t REG_SZ /d \"URL:{PROTOCOL_NAME} Protocol\" /f"
        reg_protocol_command = f"reg add {reg_path} /v \"URL Protocol\" /t REG_SZ /f"
        reg_command_exec = f'reg add {reg_path}\\shell\\open\\command /ve /t REG_SZ /d "\"{python_path}\" \"{script_path}\" \"%1\"" /f'

        try:
            # 检查协议是否已注册
            check_reg = subprocess.run(
                f'reg query {reg_path}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            if check_reg.returncode == 0:
                print(f"协议 '{PROTOCOL_NAME}://' 已经注册，是否更新(y/n): ", end='')
                user_input = input().strip().lower()

                if user_input == 'y':
                    pass
                else:
                    logging.error("协议未更新。")
                    return

            # 注册协议
            logging.info(f"运行: {reg_command}")
            subprocess.run(reg_command, shell=True, check=True)
            logging.info(f"运行: {reg_protocol_command}")
            subprocess.run(reg_protocol_command, shell=True, check=True)
            logging.info(f"运行: {reg_command_exec}")
            subprocess.run(reg_command_exec, shell=True, check=True)
            logging.info(f"协议 '{PROTOCOL_NAME}://' 注册成功。")

        except subprocess.CalledProcessError as e:
            logging.error(f"注册协议时发生错误: {e}")
        except Exception as e:
            logging.error(f"未预料的错误: {e}")

    elif platform.system() == 'Darwin':
        logging.info("此脚本正在注册 macOS 协议...")

        if not is_admin():
            logging.error("当前没有管理员权限，请使用管理员权限重新运行。")
            return

        python_path = sys.executable  # 使用当前环境的 Python 解释器
        script_path = __file__  # 获取当前脚本路径

        # 创建一个 `launchd` 配置文件来处理自定义协议
        plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
            <dict>
                <key>Label</key>
                <string>{PROTOCOL_NAME}.protocol</string>
                <key>ProgramArguments</key>
                <array>
                    <string>{python_path}</string>
                    <string>{script_path}</string>
                    <string>%1</string>
                </array>
                <key>RunAtLoad</key>
                <true/>
                <key>KeepAlive</key>
                <true/>
                <key>StandardOutPath</key>
                <string>/tmp/{PROTOCOL_NAME}_stdout.log</string>
                <key>StandardErrorPath</key>
                <string>/tmp/{PROTOCOL_NAME}_stderr.log</string>
            </dict>
        </plist>'''

        plist_path = f"/Library/LaunchDaemons/com.{PROTOCOL_NAME}.protocol.plist"

        try:
            # 写入 plist 配置文件
            with open(plist_path, 'w') as plist_file:
                plist_file.write(plist_content)

            # 加载 plist 配置文件
            subprocess.run(f"sudo launchctl load {plist_path}", shell=True, check=True)
            logging.info(f"协议 '{PROTOCOL_NAME}://' 在 macOS 上注册成功。")

        except subprocess.CalledProcessError as e:
            logging.error(f"注册协议时发生错误: {e}")
        except Exception as e:
            logging.error(f"未预料的错误: {e}")

    else:
        logging.error("当前平台不支持协议注册。")

    # 阻止控制台窗口自动关闭
    input("按任意键退出...")




def handle_custom_protocol(url):
    # 解析 URL 参数
    logging.info(f"请求路径{url}")
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    # 提取参数 id 和 name
    id = query_params.get('id', [None])[0]
    name = query_params.get('name', [None])[0]
    ide_path = query_params.get('idePath', [None])[0]
    project_path = query_params.get('projectPath', [None])[0]

    if id and name:
        logging.info(f"获取配置 id={id} , name={name} ,idePath = {ide_path} , projectPath={project_path}")
        handle_protocol(id, name,ide_path,project_path)
    else:
        logging.info("缺少 'id' 或 'name' 参数.")



if __name__ == '__main__':
    if len(sys.argv) > 1:
        url = sys.argv[1]
        handle_custom_protocol(url)
    logger.info("程序即将退出...")

    time.sleep(3)

