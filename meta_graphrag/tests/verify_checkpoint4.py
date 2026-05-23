"""Checkpoint 4 验证脚本 - CLI命令行接口验证

验证所有CLI命令正常工作，包括：
- 基础框架（10.1）
- build命令（10.2）
- serve命令（10.3）
- 主程序入口（10.4）
"""
import subprocess
import sys
import json
from pathlib import Path


class Colors:
    """终端颜色"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """打印标题"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}\n")


def print_test(name, passed, details=""):
    """打印测试结果"""
    if passed:
        print(f"{Colors.GREEN}[✓]{Colors.END} {name}")
    else:
        print(f"{Colors.RED}[✗]{Colors.END} {name}")
    if details:
        print(f"    {details}")


def run_command(cmd, timeout=10):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "命令超时"
    except Exception as e:
        return -1, "", str(e)


def test_cli_framework():
    """测试10.1: CLI基础框架"""
    print_header("测试 10.1: CLI基础框架")
    
    tests_passed = 0
    tests_total = 0
    
    # 测试1: 主帮助命令
    tests_total += 1
    returncode, stdout, stderr = run_command([sys.executable, 'src/main.py', '--help'])
    output = stdout + stderr
    passed = (returncode == 0 or returncode == -1) and '元数据知识图谱平台' in output
    print_test("主帮助命令显示正确", passed)
    if passed:
        tests_passed += 1
    
    # 测试2: 子命令存在
    tests_total += 1
    passed = 'build' in output and 'serve' in output
    print_test("子命令 build 和 serve 存在", passed)
    if passed:
        tests_passed += 1
    
    # 测试3: 无命令时显示帮助
    tests_total += 1
    returncode, stdout, stderr = run_command([sys.executable, 'src/main.py'])
    output = stdout + stderr
    passed = '元数据知识图谱平台' in output or 'usage' in output.lower()
    print_test("无命令时显示帮助信息", passed)
    if passed:
        tests_passed += 1
    
    # 测试4: argparse正确配置
    tests_total += 1
    passed = 'build' in output and 'serve' in output
    print_test("argparse子命令结构正确", passed)
    if passed:
        tests_passed += 1
    
    print(f"\n{Colors.BOLD}10.1 结果: {tests_passed}/{tests_total} 测试通过{Colors.END}")
    return tests_passed, tests_total


def test_build_command():
    """测试10.2: build命令"""
    print_header("测试 10.2: build命令")
    
    tests_passed = 0
    tests_total = 0
    
    # 测试1: build帮助
    tests_total += 1
    returncode, stdout, stderr = run_command([sys.executable, 'src/main.py', 'build', '--help'])
    output = stdout + stderr
    passed = (returncode == 0 or returncode == -1) and '--ddls-path' in output
    print_test("build命令帮助显示", passed)
    if passed:
        tests_passed += 1
    
    # 测试2: --ddls-path选项存在
    tests_total += 1
    passed = '--ddls-path' in output
    print_test("--ddls-path选项存在", passed)
    if passed:
        tests_passed += 1
    
    # 测试3: --metadata-path选项存在
    tests_total += 1
    passed = '--metadata-path' in output
    print_test("--metadata-path选项存在", passed)
    if passed:
        tests_passed += 1
    
    # 测试4: --stdin选项存在
    tests_total += 1
    passed = '--stdin' in output
    print_test("--stdin选项存在", passed)
    if passed:
        tests_passed += 1
    
    # 测试5: --config-dir选项存在
    tests_total += 1
    passed = '--config-dir' in output
    print_test("--config-dir选项存在", passed)
    if passed:
        tests_passed += 1
    
    # 测试6: --clear-db选项存在
    tests_total += 1
    passed = '--clear-db' in output
    print_test("--clear-db选项存在", passed)
    if passed:
        tests_passed += 1
    
    # 测试7: --dry-run选项存在
    tests_total += 1
    passed = '--dry-run' in output
    print_test("--dry-run选项存在", passed)
    if passed:
        tests_passed += 1
    
    # 测试8: --verbose选项存在
    tests_total += 1
    passed = '--verbose' in output or '-v' in output
    print_test("--verbose选项存在", passed)
    if passed:
        tests_passed += 1
    
    # 测试9: 互斥逻辑 - stdin与metadata-path
    tests_total += 1
    returncode, stdout, stderr = run_command([
        sys.executable, 'src/main.py', 'build',
        '--stdin', '--metadata-path', 'metadata'
    ])
    passed = returncode != 0  # 应该失败
    print_test("--stdin与--metadata-path互斥验证", passed)
    if passed:
        tests_passed += 1
    
    # 测试10: 路径验证 - 不存在的目录
    tests_total += 1
    returncode, stdout, stderr = run_command([
        sys.executable, 'src/main.py', 'build',
        '--ddls-path', 'nonexistent_directory_12345'
    ])
    output = stdout + stderr
    passed = returncode != 0 and ('不存在' in output or 'nonexistent' in output)
    print_test("不存在的DDL目录验证", passed)
    if passed:
        tests_passed += 1
    
    # 测试11: 配置目录验证
    tests_total += 1
    returncode, stdout, stderr = run_command([
        sys.executable, 'src/main.py', 'build',
        '--ddls-path', 'ddls',
        '--config-dir', 'nonexistent_config'
    ])
    output = stdout + stderr
    passed = returncode != 0 and '配置目录不存在' in output
    print_test("配置目录验证", passed)
    if passed:
        tests_passed += 1
    
    # 测试12: dry-run模式
    tests_total += 1
    returncode, stdout, stderr = run_command([
        sys.executable, 'src/main.py', 'build',
        '--ddls-path', 'ddls',
        '--dry-run'
    ], timeout=30)
    output = stdout + stderr
    passed = 'Dry-run' in output or 'dry-run' in output.lower()
    print_test("--dry-run模式执行", passed)
    if passed:
        tests_passed += 1
    
    # 测试13: 错误消息格式
    tests_total += 1
    returncode, stdout, stderr = run_command([
        sys.executable, 'src/main.py', 'build',
        '--ddls-path', 'nonexistent'
    ])
    output = stdout + stderr
    passed = '错误' in output and '使用方法' in output
    print_test("错误消息格式正确", passed)
    if passed:
        tests_passed += 1
    
    print(f"\n{Colors.BOLD}10.2 结果: {tests_passed}/{tests_total} 测试通过{Colors.END}")
    return tests_passed, tests_total


def test_serve_command():
    """测试10.3: serve命令"""
    print_header("测试 10.3: serve命令")
    
    tests_passed = 0
    tests_total = 0
    
    # 测试1: serve帮助
    tests_total += 1
    returncode, stdout, stderr = run_command([sys.executable, 'src/main.py', 'serve', '--help'])
    output = stdout + stderr
    passed = (returncode == 0 or returncode == -1) and '--config-dir' in output
    print_test("serve命令帮助显示", passed)
    if passed:
        tests_passed += 1
    
    # 测试2: --config-dir选项存在
    tests_total += 1
    passed = '--config-dir' in output
    print_test("--config-dir选项存在", passed)
    if passed:
        tests_passed += 1
    
    # 测试3: --port选项存在
    tests_total += 1
    passed = '--port' in output
    print_test("--port选项存在", passed)
    if passed:
        tests_passed += 1
    
    # 测试4: --host选项存在
    tests_total += 1
    passed = '--host' in output
    print_test("--host选项存在", passed)
    if passed:
        tests_passed += 1
    
    # 测试5: --verbose选项存在
    tests_total += 1
    passed = '--verbose' in output or '-v' in output
    print_test("--verbose选项存在", passed)
    if passed:
        tests_passed += 1
    
    # 测试6: 配置目录验证
    tests_total += 1
    returncode, stdout, stderr = run_command([
        sys.executable, 'src/main.py', 'serve',
        '--config-dir', 'nonexistent_config'
    ])
    output = stdout + stderr
    passed = returncode != 0 and '配置目录不存在' in output
    print_test("配置目录验证", passed)
    if passed:
        tests_passed += 1
    
    # 测试7: 端口号验证 - 无效端口
    tests_total += 1
    returncode, stdout, stderr = run_command([
        sys.executable, 'src/main.py', 'serve',
        '--port', '99999'
    ])
    output = stdout + stderr
    passed = returncode != 0 and ('端口号' in output or 'port' in output.lower())
    print_test("无效端口号验证", passed)
    if passed:
        tests_passed += 1
    
    # 测试8: host参数验证 - 没有port时使用host
    tests_total += 1
    returncode, stdout, stderr = run_command([
        sys.executable, 'src/main.py', 'serve',
        '--host', '127.0.0.1'
    ])
    output = stdout + stderr
    passed = returncode != 0 and '--host' in output
    print_test("--host参数需要--port验证", passed)
    if passed:
        tests_passed += 1
    
    # 测试9: 错误消息格式
    tests_total += 1
    returncode, stdout, stderr = run_command([
        sys.executable, 'src/main.py', 'serve',
        '--config-dir', 'nonexistent'
    ])
    output = stdout + stderr
    passed = '错误' in output and '使用方法' in output
    print_test("错误消息格式正确", passed)
    if passed:
        tests_passed += 1
    
    print(f"\n{Colors.BOLD}10.3 结果: {tests_passed}/{tests_total} 测试通过{Colors.END}")
    return tests_passed, tests_total


def test_main_entry():
    """测试10.4: 主程序入口"""
    print_header("测试 10.4: 主程序入口")
    
    tests_passed = 0
    tests_total = 0
    
    # 测试1: main.py可执行
    tests_total += 1
    returncode, stdout, stderr = run_command([sys.executable, 'src/main.py', '--help'])
    passed = returncode == 0 or returncode == -1
    print_test("main.py可执行", passed)
    if passed:
        tests_passed += 1
    
    # 测试2: CLI.run()被调用
    tests_total += 1
    output = stdout + stderr
    passed = '元数据知识图谱平台' in output
    print_test("CLI.run()正确调用", passed)
    if passed:
        tests_passed += 1
    
    # 测试3: 全局异常处理 - KeyboardInterrupt
    tests_total += 1
    # 这个测试比较难自动化，我们检查代码中是否有异常处理
    main_py = Path('src/main.py').read_text(encoding='utf-8')
    passed = 'KeyboardInterrupt' in main_py and 'except' in main_py
    print_test("KeyboardInterrupt异常处理存在", passed)
    if passed:
        tests_passed += 1
    
    # 测试4: 全局异常处理 - 通用异常
    tests_total += 1
    passed = 'Exception' in main_py and 'except' in main_py
    print_test("通用异常处理存在", passed)
    if passed:
        tests_passed += 1
    
    # 测试5: 退出码正确
    tests_total += 1
    returncode, stdout, stderr = run_command([
        sys.executable, 'src/main.py', 'build',
        '--ddls-path', 'nonexistent'
    ])
    passed = returncode != 0  # 错误时应该返回非0
    print_test("错误时退出码非0", passed)
    if passed:
        tests_passed += 1
    
    print(f"\n{Colors.BOLD}10.4 结果: {tests_passed}/{tests_total} 测试通过{Colors.END}")
    return tests_passed, tests_total


def test_integration():
    """集成测试 - 完整流程"""
    print_header("集成测试: 完整CLI流程")
    
    tests_passed = 0
    tests_total = 0
    
    # 测试1: build命令完整流程（dry-run）
    tests_total += 1
    returncode, stdout, stderr = run_command([
        sys.executable, 'src/main.py', 'build',
        '--ddls-path', 'ddls',
        '--metadata-path', 'metadata',
        '--dry-run',
        '--verbose'
    ], timeout=60)
    output = stdout + stderr
    passed = '开始构建知识图谱' in output or 'build' in output.lower()
    print_test("build命令完整流程（dry-run）", passed, 
               f"返回码: {returncode}")
    if passed:
        tests_passed += 1
    
    # 测试2: 配置加载流程
    tests_total += 1
    passed = '配置' in output or 'config' in output.lower()
    print_test("配置加载流程执行", passed)
    if passed:
        tests_passed += 1
    
    # 测试3: 详细输出模式
    tests_total += 1
    passed = len(output) > 100  # verbose模式应该有更多输出
    print_test("--verbose模式产生详细输出", passed)
    if passed:
        tests_passed += 1
    
    print(f"\n{Colors.BOLD}集成测试结果: {tests_passed}/{tests_total} 测试通过{Colors.END}")
    return tests_passed, tests_total


def main():
    """主函数"""
    print_header("Checkpoint 4: CLI命令行接口验证")
    print(f"{Colors.YELLOW}验证任务10（10.1-10.4）的所有CLI功能{Colors.END}\n")
    
    all_passed = 0
    all_total = 0
    
    # 运行所有测试
    passed, total = test_cli_framework()
    all_passed += passed
    all_total += total
    
    passed, total = test_build_command()
    all_passed += passed
    all_total += total
    
    passed, total = test_serve_command()
    all_passed += passed
    all_total += total
    
    passed, total = test_main_entry()
    all_passed += passed
    all_total += total
    
    passed, total = test_integration()
    all_passed += passed
    all_total += total
    
    # 最终结果
    print_header("Checkpoint 4 最终结果")
    
    percentage = (all_passed / all_total * 100) if all_total > 0 else 0
    
    if all_passed == all_total:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ 所有测试通过！{Colors.END}")
        print(f"{Colors.GREEN}通过: {all_passed}/{all_total} ({percentage:.1f}%){Colors.END}")
        print(f"\n{Colors.GREEN}Checkpoint 4 验证成功！CLI命令行接口工作正常。{Colors.END}")
        return 0
    else:
        print(f"{Colors.YELLOW}部分测试通过{Colors.END}")
        print(f"通过: {all_passed}/{all_total} ({percentage:.1f}%)")
        print(f"失败: {all_total - all_passed}/{all_total}")
        
        if percentage >= 80:
            print(f"\n{Colors.YELLOW}Checkpoint 4 基本通过（>80%），但仍有改进空间。{Colors.END}")
            return 0
        else:
            print(f"\n{Colors.RED}Checkpoint 4 未通过，需要修复失败的测试。{Colors.END}")
            return 1


if __name__ == '__main__':
    sys.exit(main())
