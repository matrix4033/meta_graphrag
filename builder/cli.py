#!/usr/bin/env python3
"""数据治理 Builder CLI — 确定性 SQL 质量检查规则生成器。

用法:
  python builder/cli.py validity --table T_CUSTOMER --dialect mysql
  python builder/cli.py uniqueness --table T_CUSTOMER --dialect mysql
  python builder/cli.py --all --table T_CUSTOMER --dialect mysql
  python builder/cli.py --list-builders
  python builder/cli.py --help
"""

import argparse
import json
import sys
import os

# 允许直接从项目根目录运行
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from builder.base import BaseBuilder
from builder.validity import ValidityBuilder
from builder.uniqueness import UniquenessBuilder


BUILDERS = {
    "validity": ValidityBuilder,
    "uniqueness": UniquenessBuilder,
}


def load_config(path="config/config.json"):
    """加载项目配置。"""
    if not os.path.exists(path):
        print(f"[错误] 配置文件不存在: {path}", file=sys.stderr)
        print(f"[提示] 请创建 {path}，可参考 data-governance-workflow.html 中的配置示例", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_metadata(path):
    """加载元数据 JSON 文件（由 Agent 从 MCP 查询后生成）。"""
    if not path:
        return None
    if not os.path.exists(path):
        print(f"[错误] 元数据文件不存在: {path}", file=sys.stderr)
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"[错误] 元数据文件格式错误: {e}", file=sys.stderr)
        return None


def get_field_metadata(metadata, table_name):
    """从元数据中提取指定表的字段列表。"""
    if not metadata:
        return []
    if "fields" in metadata:
        return metadata["fields"]
    if "tables" in metadata and table_name in metadata["tables"]:
        return metadata["tables"][table_name].get("fields", [])
    return []


def run_builder(builder_cls, config, table_name, schema, fields, primary_key, output_dir):
    """运行单个 Builder 并输出结果。"""
    builder = builder_cls(
        config=config,
        table_name=table_name,
        schema=schema,
        fields=fields,
        primary_key=primary_key,
    )

    rules = builder.build()
    if not rules:
        print(f"[{builder_cls.__name__}] 无规则生成，跳过。")
        return 0

    sql_blocks = [builder.generate_sql(r) for r in rules]
    output = builder.format_output(rules, sql_blocks)

    # stdout 输出（Agent 捕获）
    print(output)

    # 文件输出 — SQL
    sql_path = builder.save_output(output, subdir="sqls")
    print(f"\n-- [已保存] {sql_path}", file=sys.stderr)

    # 文件输出 — 规则 CSV
    csv_path = builder.save_rules_csv(rules)
    if csv_path:
        print(f"-- [已保存] {csv_path}", file=sys.stderr)

    return len(rules)


def _build_shared_parser():
    """构建共享参数（主 parser 和子命令共用）。"""
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--config", default="config/config.json",
                   help="配置文件路径 (默认: config/config.json)")
    p.add_argument("--table", "-t", default=None, help="目标表名")
    p.add_argument("--schema", "-s", default=None, help="数据库 schema")
    p.add_argument("--dialect", "-d", default=None,
                   help="数据库方言 (mysql / starrocks / postgresql)")
    p.add_argument("--metadata", "-m", default=None,
                   help="元数据 JSON 文件路径（由 Agent 从 MCP 查询生成）")
    p.add_argument("--primary-key", "-k", default=None, help="主键字段名")
    p.add_argument("--output", "-o", default="output", help="输出目录 (默认: output)")
    return p


def main():
    shared_parser = _build_shared_parser()

    parser = argparse.ArgumentParser(
        parents=[shared_parser],
        description="数据治理 Builder CLI — 确定性 SQL 质量检查规则生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python builder/cli.py validity --table T_CUSTOMER
  python builder/cli.py uniqueness --table T_CUSTOMER --dialect mysql
  python builder/cli.py --all --table T_CUSTOMER --dialect postgresql
  python builder/cli.py --list-builders
        """,
    )

    parser.add_argument("--all", "-a", action="store_true",
                        help="全量模式：一次性运行所有 Builder")
    parser.add_argument("--list-builders", action="store_true",
                        help="列出所有可用的 Builder 类型")

    # 子命令: python builder/cli.py <builder> --table ...
    subparser = parser.add_subparsers(dest="command", title="Builder 类型")
    for name in BUILDERS:
        p = subparser.add_parser(name, parents=[shared_parser],
                                 help=f"运行 {name} 规则生成器")

    args = parser.parse_args()

    # --list-builders
    if args.list_builders:
        print("可用的 Builder 类型：")
        print("=" * 50)
        for name, cls in BUILDERS.items():
            doc = cls.__doc__ or "无说明"
            print(f"  {name:<20} {doc.strip()}")
        print("=" * 50)
        print("调用方式: python builder/cli.py <builder> --table <表名>")
        return

    # 加载配置
    config = load_config(args.config)
    if args.dialect:
        config["dialect"] = args.dialect
    if args.output:
        config["output_dir"] = args.output

    table_name = args.table
    if not table_name and args.metadata:
        metadata = load_metadata(args.metadata)
        table_name = metadata.get("table_name", "")

    if not table_name:
        print("[错误] 请指定 --table 或提供 --metadata", file=sys.stderr)
        sys.exit(1)

    # 加载元数据
    metadata = load_metadata(args.metadata)
    fields = get_field_metadata(metadata, table_name)
    schema = args.schema or (metadata.get("schema") if metadata else None)
    primary_key = args.primary_key or (metadata.get("primary_key") if metadata else None)

    # 执行
    if args.command:
        # 子命令模式
        if args.command not in BUILDERS:
            print(f"[错误] 不支持的 Builder: {args.command}", file=sys.stderr)
            print(f"[提示] 支持的 Builder: {', '.join(BUILDERS.keys())}", file=sys.stderr)
            sys.exit(1)
        count = run_builder(
            BUILDERS[args.command], config, table_name,
            schema, fields, primary_key, args.output
        )
        print(f"\n-- [完成] {args.command}: 生成 {count} 条规则", file=sys.stderr)

    elif args.all:
        # 全量模式
        total = 0
        for name, cls in BUILDERS.items():
            print(f"\n{'=' * 60}", file=sys.stderr)
            print(f"[{name}] 开始生成...", file=sys.stderr)
            count = run_builder(
                cls, config, table_name,
                schema, fields, primary_key, args.output
            )
            total += count
        print(f"\n{'=' * 60}", file=sys.stderr)
        print(f"[完成] 全量模式：共生成 {total} 条规则", file=sys.stderr)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
