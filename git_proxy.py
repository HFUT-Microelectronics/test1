"""在终端交互管理 Git 全局代理，无需安装第三方库。"""

import shutil
import subprocess


PROXY = "http://127.0.0.1:7897"
KEYS = ("http.proxy", "https.proxy")


def git_config(*args):
    """通过参数列表执行 Git，避免 shell 命令拼接。"""
    return subprocess.run(
        ["git", "config", "--global", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def show_status():
    print("\n当前 Git 全局代理：")
    for key in KEYS:
        result = git_config("--get-all", key)
        if result.returncode == 0:
            print(f"  {key}: {result.stdout.strip()}")
        elif result.returncode == 1:
            print(f"  {key}: 未设置")
        else:
            print(f"  读取 {key} 失败：{result.stderr.strip()}")


def change_proxy(enable):
    success = True
    for key in KEYS:
        if enable:
            result = git_config("--replace-all", key, PROXY)
            allowed_codes = (0,)
        else:
            result = git_config("--unset-all", key)
            # Git 在配置项不存在时返回 5，这也意味着无需取消。
            allowed_codes = (0, 5)
        if result.returncode not in allowed_codes:
            success = False
            print(f"修改 {key} 失败：{result.stderr.strip()}")

    if success:
        if enable:
            print(f"\n已开启 Git 全局代理：{PROXY}")
            print("请确保 Clash Verge 已运行，且代理端口为 7897。")
        else:
            print("\n已移除 Git 全局 http.proxy 和 https.proxy 配置。")
    else:
        print("\n部分配置修改失败，请检查下面的当前状态。")
    show_status()

