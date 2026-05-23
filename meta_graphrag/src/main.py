"""主程序入口"""
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from cli import CLI


def main():
    """主函数"""
    try:
        cli = CLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n操作已取消", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n程序执行失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
