#!/usr/bin/env python3
import sys
import os
import argparse
import json
import time
import traceback
import atexit  # 用于保存历史记录
from xlang.xlang.lang import XLang
from xlang.ir.context import Context
from xlang.ir.variable import Int, Float, Bool, String, NoneType, Tuple, KeyValue

# 引入prompt_toolkit相关模块
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML

# XLang关键字列表 - 用于自动补全
XLANG_KEYWORDS = [
    "if",
    "else",
    "while",
    "break",
    "continue",
    "return",
    "int",
    "float",
    "str",
    "bool",
    "null",
    "true",
    "false",
    "import",
    "self",
    "keyof",
    "valueof",
    "selfof",
    "assert",
    "copy",
    "ref",
    "deref",
    "help()",
    "exit()",
    "clear()",
    "vars()",
]


class XLangCompleter(Completer):
    """XLang自动补全器"""

    def __init__(self, context=None):
        self.context = context
        self.keywords = XLANG_KEYWORDS

    def update_context(self, context):
        """更新上下文以获取最新的变量和函数名"""
        self.context = context


    def get_context_items(self):
        """从上下文中获取变量和函数名以及它们的说明"""
        if not self.context or not self.context.frames:
            return []

        items = {}  # 使用字典存储变量名和对应的说明

        # 从所有帧中收集变量名及其值
        for frame, is_func, _, hidden in self.context.frames:
            if not hidden and isinstance(frame, dict):
                for var_name, var_value in frame.items():
                    # 只添加新变量或更新较新帧中的变量
                    if var_name not in items:
                        description = self._get_description(var_value)
                        items[var_name] = description

        return items


    def _get_description(self, value):
        """根据变量值生成说明文本"""
        return f"{type(value).__name__}: {value}"

    def get_completions(self, document, complete_event):
        """prompt_toolkit补全函数"""
        word = document.get_word_before_cursor()

        # 获取上下文变量和其说明
        context_items = self.get_context_items()

        # 先处理关键字
        for keyword in self.keywords:
            if keyword.startswith(word):
                yield Completion(keyword, start_position=-len(word), display_meta="keyword")

        # 然后处理上下文中的变量
        for var_name, description in context_items.items():
            if var_name.startswith(word):
                yield Completion(
                    var_name, start_position=-len(word), display_meta=description
            )


def setup_prompt_toolkit():
    """配置prompt_toolkit"""
    # 设置历史记录文件
    history_dir = os.path.expanduser("~/.xlang")
    os.makedirs(history_dir, exist_ok=True)
    history_file = os.path.join(history_dir, "history")

    style = Style.from_dict(
        {
            "prompt": "#00aa00 bold",
            "continuation": "#aaaa00",
        }
    )

    # 创建Session
    session = PromptSession(
        history=FileHistory(history_file),
        auto_suggest=AutoSuggestFromHistory(),
        style=style,
    )

    return session, history_file


def multiline_input(session, prompt=">>> ", continuation_prompt="... "):
    """使用prompt_toolkit支持多行输入的函数"""
    lines = []
    line = session.prompt(HTML(f"<prompt>{prompt}</prompt>"))
    lines.append(line)

    # 检查是否需要继续获取输入
    open_braces = line.count("{") - line.count("}")
    open_brackets = line.count("[") - line.count("]")
    open_parens = line.count("(") - line.count(")")

    # 如果有未闭合的括号或代码块，继续获取输入
    while open_braces > 0 or open_brackets > 0 or open_parens > 0:
        line = session.prompt(
            HTML(f"<continuation>{continuation_prompt}</continuation>")
        )
        lines.append(line)

        open_braces += line.count("{") - line.count("}")
        open_brackets += line.count("[") - line.count("]")
        open_parens += line.count("(") - line.count(")")

    return "\n".join(lines)


def main():
    """X Lang command line tool entry point"""
    parser = argparse.ArgumentParser(
        description="X Lang - Lightweight programming language"
    )
    parser.add_argument("-c", "--code", help="Execute X Lang code")
    parser.add_argument("-f", "--file", help="Execute X Lang code from file")
    parser.add_argument("-o", "--output", help="Output file for compiled code")
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Start interactive mode"
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="Show version information"
    )
    parser.add_argument(
        "--ast", action="store_true", help="Output abstract syntax tree"
    )
    parser.add_argument(
        "--ir", action="store_true", help="Output intermediate representation"
    )
    parser.add_argument("--time", action="store_true", help="Show execution time")

    args = parser.parse_args()
    xlang = XLang()

    # Show version information
    if args.version:
        print("X Lang version 0.1.0")
        return

    # Handle command line arguments
    if args.code:
        # Direct code execution
        try:
            start_time = time.time()

            if args.ast:
                ast = xlang.parse(args.code)
                print(json.dumps(ast.to_dict(), ensure_ascii=False))
            elif args.ir:
                ir = xlang.compile(args.code)
                print(json.dumps(ir.export_to_dict(), ensure_ascii=False))
            else:
                result = xlang.execute(args.code)
                if result is not None:
                    print(result)

            if args.time:
                print(f"Execution time: {time.time() - start_time:.6f} seconds")
        except Exception as e:

            traceback.print_exc()
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.file:
        try:
            # Execute file
            with open(args.file, "r", encoding="utf-8") as f:
                code = f.read()

            start_time = time.time()

            # If output file is specified, compile to .xir
            if args.output:
                ir = xlang.compile(code)
                # Ensure output directory exists
                output_dir = os.path.dirname(os.path.abspath(args.output))
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)
                # Write compilation result
                with open(args.output, "w", encoding="utf-8") as out_file:
                    out_file.write(json.dumps(ir.export_to_dict(), ensure_ascii=False))
                print(f"Compiled to: {args.output}")
            elif args.ast:
                ast = xlang.parse(code)
                print(json.dumps(ast.to_dict(), ensure_ascii=False))
            elif args.ir:
                ir = xlang.compile(code)
                print(json.dumps(ir.export_to_dict(), ensure_ascii=False))
            else:
                # Direct execution
                result = xlang.execute(code)
                if result is not None:
                    print(result)

            if args.time:
                print(f"Execution time: {time.time() - start_time:.6f} seconds")
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            traceback.print_exc()
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.interactive:
        # Interactive mode with prompt_toolkit support
        print("X Lang Interactive Mode")
        print("Enter 'exit()' or press Ctrl+C to exit")
        print("Use arrow keys for history navigation, Tab for completion")
        print()

        # 设置prompt_toolkit
        session, history_file = setup_prompt_toolkit()

        # Create separate interpreter instance to maintain state
        context = Context()
        stack = []
        context.new_frame(stack=stack, enter_func=True, hidden=True)
        interpreter = XLang()
        interpreter.create_builtins_for_context(context)
        context.new_frame(stack=stack, enter_func=True)
        # 设置自动补全
        completer = XLangCompleter(context)
        session.completer = completer

        while True:
            try:
                # 检测多行输入
                try:
                    # 获取用户输入，支持多行输入
                    user_input = multiline_input(session)

                    # 如果为空行，则继续
                    if not user_input.strip():
                        continue

                    # 检查退出命令
                    if user_input.strip() == "exit()":
                        context.pop_frame(stack, exit_func=True)
                        context.pop_frame(stack, exit_func=True)
                        break

                    # 特殊命令处理
                    if user_input.strip() == "help()":
                        print("XLang Help:")
                        print("  exit()  - Exit the interpreter")
                        print("  help()  - Display this help message")
                        print("  clear() - Clear the screen")
                        print("  vars()  - List all variables in current scope")
                        continue

                    if user_input.strip() == "clear()":
                        os.system("cls" if os.name == "nt" else "clear")
                        continue

                    if user_input.strip() == "vars()":
                        # 显示当前作用域中的所有变量
                        current_frame = context.frames[-1]
                        if current_frame:
                            print("Variables in current scope:")
                            for var_name, var_value in current_frame[0].items():
                                print(f"  {var_name} = {var_value}")
                        else:
                            print("No variables in current scope")
                        continue

                    # 执行代码
                    start_time = time.time()
                    result = interpreter.execute_with_context(
                        user_input, context, stack
                    )

                    # 更新补全器的上下文
                    completer.update_context(context)

                    # 显示结果
                    if not isinstance(result, NoneType):
                        print(result)

                    if args.time:
                        print(f"Execution time: {time.time() - start_time:.6f} seconds")

                except EOFError:
                    # Ctrl+D 处理
                    print("\nExited")
                    context.pop_frame(stack, exit_func=True)
                    context.pop_frame(stack, exit_func=True)
                    break

            except KeyboardInterrupt:
                # Ctrl+C 处理
                print("\nOperation cancelled")
                continue
            except Exception as e:
                # 详细错误信息
                error_type = type(e).__name__
                print(f"{error_type}: {e}")

                # 显示错误行号和文件（如果可用）
                tb = traceback.extract_tb(sys.exc_info()[2])
                if tb:
                    filename, line, func, text = tb[-1]
                    if filename != "<string>":  # 避免显示内部执行的行号
                        print(f"  at line {line}, in {func}")
                        if text:
                            print(f"  {text}")

                traceback.print_exc()
    else:
        # If no arguments provided, show help
        parser.print_help()


if __name__ == "__main__":
    main()
