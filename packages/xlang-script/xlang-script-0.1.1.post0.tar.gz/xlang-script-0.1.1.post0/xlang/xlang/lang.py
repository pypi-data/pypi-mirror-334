from xlang.ir.IR import IRExecutor, Functions, create_builtins, IRType, IR
from xlang.parser import build_ast
from xlang.parser.IR_generator import IRGenerator
from xlang.ir.variable import *


class XLang:
    def __init__(self):
        pass

    def x_to_python(self, x_value):
        """将X语言值转换为Python值"""

        if isinstance(x_value, Int):
            return int(x_value.value)
        elif isinstance(x_value, Float):
            return float(x_value.value)
        elif isinstance(x_value, Bool):
            return bool(x_value.value)
        elif isinstance(x_value, String):
            return str(x_value.value)
        elif isinstance(x_value, NoneType):
            return None
        elif isinstance(x_value, Tuple):
            return [self.x_to_python(v) for v in x_value.value]
        elif isinstance(x_value, Variable):
            return self.x_to_python(x_value.value)
        elif isinstance(x_value, KeyValue):
            return {self.x_to_python(x_value.key): self.x_to_python(x_value.value)}
        elif isinstance(x_value, Lambda):
            return f"Lambda({x_value.signature}, {self.x_to_python(x_value.default_args_tuple)})"
        elif isinstance(x_value, Named):
            return f"{self.x_to_python(x_value.key)} => {self.x_to_python(x_value.value)}"
        elif isinstance(x_value, Ref):
            return f"&{self.x_to_python(x_value.value)}"
        elif isinstance(x_value, GetAttr):
            return f"{self.x_to_python(x_value.value)}.{self.x_to_python(x_value.key)}"
        elif isinstance(x_value, IndexOf):
            return f"{self.x_to_python(x_value.value)}[{self.x_to_python(x_value.key)}]"
        raise TypeError(f"Cant convert X type: {type(x_value)}")

    def python_to_x(self, py_value):
        """将Python值转换为X语言值"""
        from xlang.ir.variable import Int, Float, Bool, String, Tuple, KeyValue, NoneType

        if isinstance(py_value, int):
            return Int(py_value)
        elif isinstance(py_value, float):
            return Float(py_value)
        elif isinstance(py_value, bool):
            return Bool(py_value)
        elif isinstance(py_value, str):
            return String(py_value)
        elif py_value is None:
            return NoneType()
        elif isinstance(py_value, list):
            return Tuple([self.python_to_x(v) for v in py_value])
        elif isinstance(py_value, dict):
            values = [
                KeyValue(self.python_to_x(k), self.python_to_x(v))
                for k, v in py_value.items()
            ]
            return Tuple(values)
        raise TypeError(f"Cant convert Python type: {type(py_value)}")

    def compile(self, code, namespace="__MAIN__"):
        """编译X语言代码并返回IR"""
        ast = build_ast(code)
        functions = Functions()
        generator = IRGenerator(functions=functions, namespace=namespace)
        IRs = generator.generate(ast)
        IRs.append(IR(IRType.RETURN_NONE))
        functions.add("__main__", IRs)
        return functions

    def execute(
        self,
        code,
        entry="__main__",
        error_printer=print,
        output_printer=print,
        input_reader=input,
        open_func=open,
        should_stop_func=None,
        **kwargs,
    ):
        """执行X语言代码并返回结果"""
        ast = build_ast(code)
        functions = Functions()
        generator = IRGenerator(functions=functions)
        IRs = generator.generate(ast)
        IRs.append(IR(IRType.RETURN_NONE))
        functions.add("__main__", IRs)
        executor = IRExecutor(code, error_printer, output_printer, input_reader, should_stop_func, open_func)
        executor_args = {}
        for k, v in kwargs.items():
            executor_args[k] = self.python_to_x(v)
        result = executor.execute_with_let(functions, entry, executor_args)
        return self.x_to_python(result)

    def execute_with_context(
        self,
        code,
        context,
        stack,
        entry="__main__",
        error_printer=print,
        output_printer=print,
        input_reader=input,
        open_func=open,
        should_stop_func=None,
    ):
        """使用给定的上下文和堆栈执行X语言代码"""
        ast = build_ast(code)
        functions = Functions()
        generator = IRGenerator(functions=functions)
        IRs = generator.generate(ast)
        functions.add("__main__", IRs)
        executor = IRExecutor(code, error_printer, output_printer, input_reader, should_stop_func, open_func)
        result = executor.execute_with_provided_context(functions, entry, context, stack)
        return result

    def create_builtins_for_context(self, context, output_printer=print, input_reader=input):
        create_builtins(context, output_printer, input_reader)

    def parse(self, code):
        """解析X语言代码并返回AST"""
        return build_ast(code)
