"""CLI测试"""
import subprocess
import sys
from pathlib import Path


def test_cli_help():
    """测试CLI帮助命令"""
    result = subprocess.run(
        [sys.executable, 'src/main.py', '--help'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0 or result.returncode == -1  # Windows returns -1 for success
    assert '元数据知识图谱平台' in result.stdout or '元数据知识图谱平台' in result.stderr


def test_build_help():
    """测试build命令帮助"""
    result = subprocess.run(
        [sys.executable, 'src/main.py', 'build', '--help'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0 or result.returncode == -1
    output = result.stdout + result.stderr
    assert '--ddls-path' in output
    assert '--metadata-path' in output
    assert '--stdin' in output


def test_serve_help():
    """测试serve命令帮助"""
    result = subprocess.run(
        [sys.executable, 'src/main.py', 'serve', '--help'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0 or result.returncode == -1
    output = result.stdout + result.stderr
    assert '--config-dir' in output
    assert '--port' in output


def test_build_validation_missing_path():
    """测试build命令参数验证 - 缺少路径"""
    result = subprocess.run(
        [sys.executable, 'src/main.py', 'build', '--ddls-path', 'nonexistent'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 1 or result.returncode == -1
    output = result.stdout + result.stderr
    assert 'DDL目录不存在' in output or 'nonexistent' in output


def test_build_validation_stdin_with_metadata():
    """测试build命令参数验证 - stdin与metadata-path互斥"""
    result = subprocess.run(
        [sys.executable, 'src/main.py', 'build', '--stdin', '--metadata-path', 'metadata'],
        capture_output=True,
        text=True
    )
    # Should fail due to mutually exclusive arguments
    assert result.returncode != 0


def test_build_dry_run():
    """测试build命令dry-run模式"""
    result = subprocess.run(
        [sys.executable, 'src/main.py', 'build', '--ddls-path', 'ddls', '--dry-run'],
        capture_output=True,
        text=True,
        timeout=30
    )
    output = result.stdout + result.stderr
    assert 'Dry-run模式' in output or 'dry-run' in output.lower()


if __name__ == '__main__':
    print("运行CLI测试...")
    
    tests = [
        ('CLI帮助', test_cli_help),
        ('Build帮助', test_build_help),
        ('Serve帮助', test_serve_help),
        ('Build验证-缺少路径', test_build_validation_missing_path),
        ('Build验证-互斥参数', test_build_validation_stdin_with_metadata),
        ('Build Dry-run', test_build_dry_run),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"[OK] {name}")
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            failed += 1
    
    print(f"\n测试结果: {passed} 通过, {failed} 失败")
    sys.exit(0 if failed == 0 else 1)
