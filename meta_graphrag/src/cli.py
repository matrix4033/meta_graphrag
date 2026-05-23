"""命令行接口"""
import argparse
import sys
from pathlib import Path
from typing import Tuple, Optional
from utils.logger import setup_logger, get_logger
from utils.config_loader import ConfigLoader
from utils.config_validator import ConfigValidator
from utils.error_codes import ErrorCode, ErrorMessage


class CLI:
    """命令行接口"""
    
    def __init__(self):
        """初始化CLI"""
        self.parser = argparse.ArgumentParser(
            description='元数据知识图谱平台',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        self.subparsers = self.parser.add_subparsers(dest='command', help='可用命令')
        self._setup_build_command()
        self._setup_serve_command()
        self.logger = None
    
    def _setup_build_command(self):
        """设置build命令"""
        build_parser = self.subparsers.add_parser(
            'build',
            help='构建知识图谱',
            description='从DDL文件和元数据文档构建知识图谱'
        )
        
        # 输入源选项（互斥）
        input_group = build_parser.add_mutually_exclusive_group(required=True)
        input_group.add_argument(
            '--ddls-path',
            type=str,
            help='DDL文件目录路径'
        )
        input_group.add_argument(
            '--stdin',
            action='store_true',
            help='从标准输入读取JSON格式数据'
        )
        
        # 元数据路径（可选，仅在使用--ddls-path时有效）
        build_parser.add_argument(
            '--metadata-path',
            type=str,
            help='元数据文档目录路径（可选）'
        )
        
        # 配置选项
        build_parser.add_argument(
            '--config-dir',
            type=str,
            default='./config',
            help='配置文件目录路径（默认：./config）'
        )
        
        # 数据库选项
        build_parser.add_argument(
            '--clear-db',
            action='store_true',
            help='构建前清空Neo4j数据库'
        )
        
        # 调试选项
        build_parser.add_argument(
            '--dry-run',
            action='store_true',
            help='只解析不写入数据库'
        )
        
        build_parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='详细输出模式'
        )
    
    def _setup_serve_command(self):
        """设置serve命令"""
        serve_parser = self.subparsers.add_parser(
            'serve',
            help='启动MCP服务器',
            description='启动MCP服务器提供图数据库检索服务'
        )
        
        # 配置选项
        serve_parser.add_argument(
            '--config-dir',
            type=str,
            default='./config',
            help='配置文件目录路径（默认：./config）'
        )
        
        # 网络选项
        serve_parser.add_argument(
            '--port',
            type=int,
            help='MCP服务器端口（默认：使用stdio）'
        )
        
        serve_parser.add_argument(
            '--host',
            type=str,
            default='0.0.0.0',
            help='MCP服务器主机地址（仅在使用端口时有效，默认：0.0.0.0）'
        )
        
        # 调试选项
        serve_parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='详细输出模式'
        )
    
    def _validate_build_args(self, args) -> Tuple[bool, Optional[str]]:
        """
        验证build命令参数
        
        Args:
            args: 命令行参数
        
        Returns:
            (是否有效, 错误消息)
        """
        # 验证互斥性：--stdin与--metadata-path互斥
        if args.stdin and args.metadata_path:
            return False, "错误：--stdin不能与--metadata-path同时使用"
        
        # 验证路径存在性
        if args.ddls_path:
            ddls_path = Path(args.ddls_path)
            if not ddls_path.exists():
                return False, f"错误：DDL目录不存在：{args.ddls_path}"
            if not ddls_path.is_dir():
                return False, f"错误：DDL路径不是目录：{args.ddls_path}"
        
        if args.metadata_path:
            metadata_path = Path(args.metadata_path)
            if not metadata_path.exists():
                return False, f"错误：元数据目录不存在：{args.metadata_path}"
            if not metadata_path.is_dir():
                return False, f"错误：元数据路径不是目录：{args.metadata_path}"
        
        # 验证配置目录
        config_dir = Path(args.config_dir)
        if not config_dir.exists():
            return False, f"错误：配置目录不存在：{args.config_dir}"
        if not config_dir.is_dir():
            return False, f"错误：配置路径不是目录：{args.config_dir}"
        
        return True, None
    
    def _validate_serve_args(self, args) -> Tuple[bool, Optional[str]]:
        """
        验证serve命令参数
        
        Args:
            args: 命令行参数
        
        Returns:
            (是否有效, 错误消息)
        """
        # 验证配置目录
        config_dir = Path(args.config_dir)
        if not config_dir.exists():
            return False, f"错误：配置目录不存在：{args.config_dir}"
        if not config_dir.is_dir():
            return False, f"错误：配置路径不是目录：{args.config_dir}"
        
        # 验证端口号
        if args.port:
            if not (1 <= args.port <= 65535):
                return False, f"错误：端口号必须在1-65535之间：{args.port}"
        
        # 验证host参数只在指定端口时有效
        if args.host != '0.0.0.0' and not args.port:
            return False, "错误：--host参数只能在指定--port时使用"
        
        return True, None
    
    def _run_build(self, args):
        """
        执行build命令
        
        Args:
            args: 命令行参数
        """
        # 设置日志
        self.logger = setup_logger('cli', verbose=args.verbose)
        
        # 验证参数
        valid, error_msg = self._validate_build_args(args)
        if not valid:
            self.logger.error(error_msg)
            print(f"\n{error_msg}\n", file=sys.stderr)
            print("使用方法：", file=sys.stderr)
            print("  python src/main.py build --ddls-path PATH [--metadata-path PATH] [OPTIONS]", file=sys.stderr)
            print("  python src/main.py build --stdin [OPTIONS]", file=sys.stderr)
            print("\n详细帮助请运行：python src/main.py build --help", file=sys.stderr)
            sys.exit(1)
        
        self.logger.info("=" * 60)
        self.logger.info("开始构建知识图谱")
        self.logger.info("=" * 60)
        
        try:
            # 加载配置
            self.logger.info("步骤 1/6: 加载配置文件...")
            config_dir = Path(args.config_dir)
            loader = ConfigLoader(config_dir)
            configs = loader.load_all_configs()
            self.logger.info("[OK] 配置文件加载成功")
            
            # 验证配置
            self.logger.info("步骤 2/6: 验证配置...")
            validator = ConfigValidator()
            is_valid, errors = validator.validate_all_configs(configs)
            if not is_valid:
                error_msg = ErrorMessage.get_message(
                    ErrorCode.CONFIG_VALIDATION_ERROR,
                    errors="\n  - ".join(errors)
                )
                self.logger.critical(error_msg)
                print(f"\n配置验证失败：\n  - {chr(10).join(errors)}\n", file=sys.stderr)
                sys.exit(1)
            self.logger.info("[OK] 配置验证通过")

            # 解析输入数据
            self.logger.info("步骤 3/6: 解析输入数据...")
            ddl_data = []
            excel_data = []
            
            if args.stdin:
                # 从标准输入读取
                self.logger.info("从标准输入读取数据...")
                # TODO: 实现标准输入处理
                self.logger.warning("标准输入功能尚未实现")
            else:
                # 从文件目录读取
                from parser.file_scanner import FileScanner
                from parser.ddl_parser import DDLParser
                from parser.excel_parser import ExcelParser
                
                scanner = FileScanner()
                
                if args.ddls_path:
                    self.logger.info(f"扫描DDL文件: {args.ddls_path}")
                    sql_files = scanner.scan_sql_files(args.ddls_path)
                    
                    self.logger.info(f"解析 {len(sql_files)} 个DDL文件...")
                    ddl_parser = DDLParser(configs['parser_config'])
                    
                    for sql_file in sql_files:
                        parsed = ddl_parser.parse_file(sql_file)
                        if parsed:
                            ddl_data.append(parsed)
                    
                    self.logger.info(f"[OK] 成功解析 {len(ddl_data)} 个DDL文件")
                
                if args.metadata_path:
                    self.logger.info(f"扫描元数据文件: {args.metadata_path}")
                    excel_files = scanner.scan_excel_files(args.metadata_path)
                    
                    self.logger.info(f"解析 {len(excel_files)} 个Excel文件...")
                    excel_parser = ExcelParser(configs['excel_config'])
                    
                    for excel_file in excel_files:
                        records = excel_parser.parse_excel(excel_file)
                        excel_data.extend(records)
                    
                    self.logger.info(f"[OK] 成功解析 {len(excel_data)} 条元数据记录")
            
            self.logger.info("[OK] 数据解析完成")
            
            # 构建图谱
            if not args.dry_run:
                # 连接Neo4j
                self.logger.info("步骤 4/6: 连接Neo4j数据库...")
                from graph.neo4j_connection import Neo4jConnection
                neo4j_conn = Neo4jConnection(configs['neo4j_config'])
                self.logger.info("[OK] Neo4j连接成功")

                # 清空数据库（如果指定）
                if args.clear_db:
                    self.logger.info("清空Neo4j数据库...")
                    with neo4j_conn.get_session() as session:
                        session.run("MATCH (n) DETACH DELETE n")
                    self.logger.info("[OK] 数据库已清空")

                self.logger.info("步骤 5/6: 构建知识图谱...")
                from graph.graph_builder import GraphBuilder
                builder = GraphBuilder(neo4j_conn, configs)
                builder.build_graph(ddl_data, excel_data)
                self.logger.info("[OK] 知识图谱构建完成")

                # 创建索引
                self.logger.info("步骤 6/6: 创建索引...")
                from graph.index_manager import IndexManager
                with neo4j_conn.get_session() as session:
                    index_manager = IndexManager(session, configs['index_config'])
                    index_manager.create_all_indexes()
                self.logger.info("[OK] 索引创建完成")
            else:
                self.logger.info("Dry-run模式：跳过数据库写入")
            
            self.logger.info("=" * 60)
            self.logger.info("知识图谱构建成功完成！")
            self.logger.info("=" * 60)
            
        except KeyboardInterrupt:
            self.logger.warning("\n用户中断操作")
            sys.exit(130)
        except Exception as e:
            self.logger.critical(f"构建失败: {e}", exc_info=args.verbose)
            print(f"\n构建失败: {e}\n", file=sys.stderr)
            sys.exit(1)
    
    def _run_serve(self, args):
        """
        执行serve命令
        
        Args:
            args: 命令行参数
        """
        # 设置日志
        self.logger = setup_logger('cli', verbose=args.verbose)
        
        # 验证参数
        valid, error_msg = self._validate_serve_args(args)
        if not valid:
            self.logger.error(error_msg)
            print(f"\n{error_msg}\n", file=sys.stderr)
            print("使用方法：", file=sys.stderr)
            print("  python src/main.py serve [--config-dir PATH] [--port PORT] [--host HOST] [OPTIONS]", file=sys.stderr)
            print("\n详细帮助请运行：python src/main.py serve --help", file=sys.stderr)
            sys.exit(1)
        
        self.logger.info("=" * 60)
        self.logger.info("启动MCP服务器")
        self.logger.info("=" * 60)
        
        try:
            # 加载配置
            self.logger.info("加载配置文件...")
            config_dir = Path(args.config_dir)
            
            # 加载配置
            loader = ConfigLoader(config_dir)
            configs = loader.load_all_configs()
            
            # 验证配置
            self.logger.info("验证配置...")
            validator = ConfigValidator()
            is_valid, errors = validator.validate_all_configs(configs)
            if not is_valid:
                error_msg = ErrorMessage.get_message(
                    ErrorCode.CONFIG_VALIDATION_ERROR,
                    errors="\n  - ".join(errors)
                )
                self.logger.critical(error_msg)
                print(f"\n配置验证失败：\n  - {chr(10).join(errors)}\n", file=sys.stderr)
                sys.exit(1)
            self.logger.info("[OK] 配置验证通过")
            
            # 初始化MCP服务器
            self.logger.info("初始化MCP服务器...")
            from mcp.mcp_server import MCPServer
            server = MCPServer(config_dir, verbose=args.verbose)
            
            # 启动服务器
            if args.port:
                self.logger.info(f"MCP服务器启动在 {args.host}:{args.port}")
                self.logger.warning("TCP端口模式尚未实现，将使用stdio模式")
                server.run_stdio()
            else:
                self.logger.info("MCP服务器启动（stdio模式）")
                server.run_stdio()
            
        except KeyboardInterrupt:
            self.logger.info("\nMCP服务器已停止")
            sys.exit(0)
        except Exception as e:
            self.logger.critical(f"服务器启动失败: {e}", exc_info=args.verbose)
            print(f"\n服务器启动失败: {e}\n", file=sys.stderr)
            sys.exit(1)
    
    def run(self):
        """执行命令"""
        args = self.parser.parse_args()
        
        if args.command == 'build':
            self._run_build(args)
        elif args.command == 'serve':
            self._run_serve(args)
        else:
            self.parser.print_help()
            sys.exit(1)


if __name__ == '__main__':
    cli = CLI()
    cli.run()
