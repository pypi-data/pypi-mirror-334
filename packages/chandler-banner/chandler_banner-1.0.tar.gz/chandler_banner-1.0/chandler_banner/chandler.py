import pyfiglet
from termcolor import colored
import colorama

# 初始化 colorama，让 Windows 终端支持 ANSI 颜色
colorama.init()

def banner1():
    """
    生成并打印固定文本和颜色的 ASCII 结构字体
    """
    text = "Chandler Liu12138"  # 你可以修改这里的固定文本
    color = "green"  # 你可以修改这里的固定颜色

    try:
        ascii_art = pyfiglet.figlet_format(text)
        colored_text = colored(ascii_art, color)
        print(colored_text)
    except Exception as e:
        print(f"生成 ASCII 失败: {e}")
    input("流水落花春去也，天上人间……")

# 仅当直接运行此文件时才执行（测试用）
if __name__ == "__main__":
    banner1()
