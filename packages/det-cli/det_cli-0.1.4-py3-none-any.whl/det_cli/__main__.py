import sys
from det_cli.register import handle_custom_protocol

if __name__ == "__main__":
    # 接受命令行参数
    if len(sys.argv) > 1:
        url = sys.argv[1]
        handle_custom_protocol(url)
