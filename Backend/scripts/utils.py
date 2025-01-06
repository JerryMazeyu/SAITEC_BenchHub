import json
from colorama import Fore, Style, init
import os
init(autoreset=True)

def printtify(message, data=None, color='blue', align="default", bright=None):
    """
    美化输出测试结果。
    :param message: 测试描述
    :param status: 测试状态，"success" 或 "fail"
    :param data: 额外的 JSON 数据
    """
    if color == 'red':
        color = Fore.RED
    elif color == 'green':
        color = Fore.GREEN
    elif color == 'blue':
        color = Fore.BLUE
    if bright:
        content = Style.BRIGHT + Fore.BLACK + message
    else:
        content = color + message
    if align == "center":
        try:
            terminal_width = int(os.get_terminal_size().columns * 0.6)
        except OSError:
            terminal_width = 80 
        print(content.center(terminal_width, "="))
    else:
        print(content)
    if data:
        print(Fore.YELLOW + json.dumps(data, indent=4, ensure_ascii=False))





