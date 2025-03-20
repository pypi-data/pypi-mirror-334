from .ast import XLangASTNode, XLangASTNodeTypes
from ..ir.IR import IRType, IR, Functions
from typing import List


class IRGenerator:

    def __init__(self, functions, namespace="__MAIN__"):
        self.function_signture_counter = 0
        self.namespace = namespace
        self.functions = functions
        self.scope_stack = []  # 元素形式: (类型, 附加信息)
        # 类型可以是: 'loop', 'frame', 'function'等
        self.label_counter = 0

    def label_generator(self):
        self.label_counter += 1
        return f"{self.namespace}::__label_{self.label_counter}__"

    def function_signature_generator(self, node):
        self.function_signture_counter += 1
        return f"{self.namespace}::__function_{self.function_signture_counter}__"

    def generate_debug_info(self, node: XLangASTNode) -> IR:
        return IR(IRType.DEBUG_INFO, {
            "code_position": node.node_position,
        })

    def generate_without_redirect(self, node) -> List[IR]:
        node_type = node.node_type

        debug_info = self.generate_debug_info(node)

        if node_type == XLangASTNodeTypes.BODY:
            irs = []
            irs.append(debug_info)
            irs.append(IR(IRType.NEW_FRAME))

            # 记录进入新作用域
            self.scope_stack.append(("frame", None))

            for child in node.children:
                irs.extend(self.generate_without_redirect(child))

            # 离开作用域
            self.scope_stack.pop()

            irs.append(IR(IRType.POP_FRAME))
            return irs

        elif node_type == XLangASTNodeTypes.FUNCTION_DEF:
            irs = []
            irs.append(debug_info)
            args = node.children[0]
            if args.node_type != XLangASTNodeTypes.TUPLE:
                args = XLangASTNode(XLangASTNodeTypes.TUPLE, [args])

            # 解析函数参数IR
            args_ir = self.generate_without_redirect(args)

            # 解析函数体IR
            signture = self.function_signature_generator(node)

            generator = IRGenerator(self.functions, signture)
            body_ir = generator.generate(node.children[1])
            body_ir.append(IR(IRType.RETURN_NONE))
            # 生成函数定义IR

            self.functions.add(signture, body_ir)

            irs.extend(args_ir)  # 构建默认参数的tuple
            irs.append(IR(IRType.LOAD_LAMBDA, [signture, node.node_position]))
            return irs

        elif node_type == XLangASTNodeTypes.ASSIGN:
            irs = []
            irs.append(debug_info)
            irs.extend(self.generate_without_redirect(node.children[0]))
            irs.extend(self.generate_without_redirect(node.children[1]))
            irs.append(IR(IRType.SET_VAL))
            return irs

        elif node_type == XLangASTNodeTypes.VARIABLE:
            irs = []
            irs.append(debug_info)
            irs.append(IR(IRType.GET_VAL, node.children))
            return irs

        elif node_type == XLangASTNodeTypes.LET:
            irs = []
            irs.append(debug_info)
            irs.extend(self.generate_without_redirect(node.children[1]))
            irs.append(IR(IRType.LET_VAL, node.children[0].children))
            return irs

        elif node_type == XLangASTNodeTypes.FUNCTION_CALL:
            irs = []
            irs.append(debug_info)
            for child in node.children:
                irs.extend(self.generate_without_redirect(child))
            irs.append(IR(IRType.CALL_LAMBDA))
            return irs

        elif node_type == XLangASTNodeTypes.OPERATION:
            irs = []
            irs.append(debug_info)
            if len(node.children) == 2:
                irs.extend(self.generate_without_redirect(node.children[1]))
                irs.append(IR(IRType.UNARY_OP, node.children[0]))
                return irs
            irs.extend(self.generate_without_redirect(node.children[0]))
            irs.extend(self.generate_without_redirect(node.children[2]))
            irs.append(IR(IRType.BINARAY_OP, node.children[1]))
            return irs
        elif node_type == XLangASTNodeTypes.INDEX_OF:
            irs = []
            irs.append(debug_info)
            irs.extend(self.generate_without_redirect(node.children[0]))
            irs.extend(self.generate_without_redirect(node.children[1]))
            irs.append(IR(IRType.INDEX_OF))
            return irs
        elif node_type == XLangASTNodeTypes.GET_ATTR:
            irs = []
            irs.append(debug_info)
            irs.extend(self.generate_without_redirect(node.children[0]))
            irs.extend(self.generate_without_redirect(node.children[1]))
            irs.append(IR(IRType.GET_ATTR))
            return irs

        elif node_type == XLangASTNodeTypes.RETURN:
            irs = []
            irs.append(debug_info)
            irs.extend(self.generate_without_redirect(node.children))
            irs.append(IR(IRType.RETURN))
            return irs

        elif node_type == XLangASTNodeTypes.NUMBER:
            irs = []
            irs.append(debug_info)
            if "." in node.children:
                irs.append(IR(IRType.LOAD_FLOAT, float(node.children)))
            else:
                irs.append(IR(IRType.LOAD_INT, int(node.children)))
            return irs

        elif node_type == XLangASTNodeTypes.TUPLE:
            irs = []
            irs.append(debug_info)
            tuple_size = 0
            for child in node.children:
                if child.node_type == XLangASTNodeTypes.NONE:
                    continue
                irs.extend(self.generate_without_redirect(child))
                tuple_size += 1
            irs.append(IR(IRType.BUILD_TUPLE, tuple_size))
            return irs

        elif node_type == XLangASTNodeTypes.KEY_VAL:
            irs = []
            irs.append(debug_info)
            irs.extend(self.generate_without_redirect(node.children[0]))
            irs.extend(self.generate_without_redirect(node.children[1]))
            irs.append(IR(IRType.BUILD_KEY_VAL))
            return irs
        elif node_type == XLangASTNodeTypes.NAMED_ARGUMENT:
            irs = []
            irs.append(debug_info)
            irs.extend(self.generate_without_redirect(node.children[0]))
            irs.extend(self.generate_without_redirect(node.children[1]))
            irs.append(IR(IRType.BUILD_NAMED))
            return irs
        elif node_type == XLangASTNodeTypes.STRING:
            irs = []
            irs.append(debug_info)
            irs.append(IR(IRType.LOAD_STRING, node.children))
            return irs

        elif node_type == XLangASTNodeTypes.SEPARATOR:
            irs = []
            irs.append(debug_info)
            for child in node.children:
                irs.append(IR(IRType.RESET_STACK))
                irs.extend(self.generate_without_redirect(child))
            return irs
        elif node_type == XLangASTNodeTypes.NULL:
            irs = []
            irs.append(debug_info)
            irs.append(IR(IRType.LOAD_NONE))
            return irs
        elif node_type == XLangASTNodeTypes.NONE:
            return [IR(IRType.LOAD_NONE)]
        elif node_type == XLangASTNodeTypes.BOOLEN:
            irs = []
            irs.append(debug_info)
            irs.append(IR(IRType.LOAD_BOOL, node.children))
            return irs
        elif node_type == XLangASTNodeTypes.IF:
            if len(node.children) == 2:
                irs = []
                irs.append(debug_info)
                irs.extend(self.generate_without_redirect(node.children[0]))
                body = self.generate_without_redirect(node.children[1])
                label = self.label_generator()
                else_label = self.label_generator()
                irs.append(IR(IRType.REDIRECT_JUMP_IF_FALSE, label))
                irs.extend(body)
                irs.append(IR(IRType.REDIRECT_JUMP, else_label))
                irs.append(IR(IRType.REDIRECT_LABEL, label))
                irs.append(IR(IRType.LOAD_NONE))
                irs.append(IR(IRType.REDIRECT_LABEL, else_label))
                return irs
            elif len(node.children) == 3:
                irs = []
                irs.append(debug_info)
                irs.extend(self.generate_without_redirect(node.children[0]))
                body = self.generate_without_redirect(node.children[1])
                else_body = self.generate_without_redirect(node.children[2])
                label = self.label_generator()
                else_label = self.label_generator()
                irs.append(IR(IRType.REDIRECT_JUMP_IF_FALSE, label))
                irs.extend(body)
                irs.append(IR(IRType.REDIRECT_JUMP, else_label))
                irs.append(IR(IRType.REDIRECT_LABEL, label))
                irs.extend(else_body)
                irs.append(IR(IRType.REDIRECT_LABEL, else_label))
                return irs

        elif node_type == XLangASTNodeTypes.BREAK:
            irs = []
            irs.append(debug_info)
            irs.extend(self.generate_without_redirect(node.children))

            # 查找最近的循环
            frames_to_pop = 0
            found_loop = False
            loop_label = None
            # 从栈顶向下查找，统计中间的作用域帧
            for scope_type, info in reversed(self.scope_stack):
                if scope_type == "loop":
                    found_loop = True
                    loop_label = info
                    break
                elif scope_type == "frame":
                    frames_to_pop += 1

            if not found_loop:
                raise SyntaxError("'break' outside loop")

            # 如果有需要弹出的帧，添加POP_FRAME指令
            for _ in range(frames_to_pop):
                irs.append(IR(IRType.POP_FRAME))

            irs.append(IR(IRType.REDIRECT_JUMP, loop_label[1])) # 跳出循环

            return irs

        elif node_type == XLangASTNodeTypes.CONTINUE:
            irs = []
            irs.append(debug_info)
            irs.extend(self.generate_without_redirect(node.children))

            # 查找最近的循环
            frames_to_pop = 0
            found_loop = False
            loop_label = None

            # 从栈顶向下查找，统计中间的作用域帧
            for scope_type, info in reversed(self.scope_stack):
                if scope_type == "loop":
                    found_loop = True
                    loop_label = info
                    break
                elif scope_type == "frame":
                    frames_to_pop += 1

            if not found_loop:
                raise SyntaxError("'continue' outside loop")

            # 如果有需要弹出的帧，添加POP_FRAME指令
            for _ in range(frames_to_pop):
                irs.append(IR(IRType.POP_FRAME))
            irs.append(IR(IRType.REDIRECT_JUMP, loop_label[0])) # 跳回循环头
            return irs

        elif node_type == XLangASTNodeTypes.WHILE:
            irs = []
            irs.append(debug_info)

            # 记录进入循环
            while_head = self.label_generator()
            while_med = self.label_generator()
            while_end = self.label_generator()
            self.scope_stack.append(("loop", (while_head, while_end))) # 头尾标签

            irs.append(IR(IRType.REDIRECT_LABEL, while_head))
            # 生成条件代码
            condition = self.generate_without_redirect(node.children[0])
            irs.extend(condition)

            # 条件判断，如果为假则跳出循环
            irs.append(IR(IRType.REDIRECT_JUMP_IF_FALSE, while_med)) 

            # 生成循环体代码
            body = self.generate_without_redirect(node.children[1])
            irs.extend(body)

            # 循环结束后跳回条件判断
            irs.append(IR(IRType.REDIRECT_JUMP, while_head))
            irs.append(IR(IRType.REDIRECT_LABEL, while_med))
            irs.append(IR(IRType.LOAD_NONE)) # 如果没有返回值，返回None
            irs.append(IR(IRType.REDIRECT_LABEL, while_end))
            # 离开循环
            self.scope_stack.pop()
            return irs

        elif node_type == XLangASTNodeTypes.MODIFY:
            irs = []
            irs.append(debug_info)
            val = self.generate_without_redirect(node.children[1])
            if node.children[0] == 'copy':
                irs.extend(val)
                irs.append(IR(IRType.COPY_VAL))
            elif node.children[0] == 'ref':
                irs.extend(val)
                irs.append(IR(IRType.REF_VAL))
            elif node.children[0] == 'deref':
                irs.extend(val)
                irs.append(IR(IRType.DEREF_VAL))
            elif node.children[0] == 'keyof':
                irs.extend(val)
                irs.append(IR(IRType.KEY_OF))
            elif node.children[0] == 'valueof':
                irs.extend(val)
                irs.append(IR(IRType.VALUE_OF))
            elif node.children[0] == 'assert':
                irs.extend(val)
                irs.append(IR(IRType.ASSERT))
            elif node.children[0] == 'selfof':
                irs.extend(val)
                irs.append(IR(IRType.SELF_OF))
            elif node.children[0] == 'import':
                irs.extend(val)
                irs.append(IR(IRType.IMPORT, node.node_position))
            elif node.children[0] == 'wrap':
                irs.extend(val)
                irs.append(IR(IRType.BUILD_WRAP))
            else:
                raise ValueError(f"Unknown modifier: {node.children[0]}")
            return irs
        else:
            raise Exception(f"Unknown node type: {node_type}")

    def redirect_jump(self, irs: List[IR]) -> List[IR]:
        """
        重定向所有跳转指令，将REDIRECT_JUMP和REDIRECT_JUMP_IF_FALSE转换为JUMP_OFFSET和JUMP_IF_FALSE

        Args:
            irs: IR指令列表

        Returns:
            处理后的IR指令列表
        """

        reduced_irs = []
        label_map = {}
        for ir in irs:
            if ir.ir_type == IRType.REDIRECT_LABEL:
                label_map[ir.value] = len(reduced_irs)
            else:
                reduced_irs.append(ir)

        # 转换所有跳转指令
        for i, ir in enumerate(reduced_irs):
            if ir.ir_type == IRType.REDIRECT_JUMP:
                label = ir.value
                if label not in label_map:
                    raise ValueError(f"Label not found: {label}")
                offset = label_map[label] - i - 1
                reduced_irs[i] = IR(IRType.JUMP_OFFSET, offset)
            elif ir.ir_type == IRType.REDIRECT_JUMP_IF_FALSE:
                label = ir.value
                if label not in label_map:
                    raise ValueError(f"Label not found: {label}")
                offset = label_map[label] - i - 1
                reduced_irs[i] = IR(IRType.JUMP_IF_FALSE, offset)

        return reduced_irs

    def retain_latest_debug_info(self, irs: List[IR]) -> List[IR]:
        """
        移除相邻的debug_info指令，只保留最新的一个

        Args:
            irs: 原始IR指令列表

        Returns:
            处理后的IR指令列表
        """
        if not irs:
            return []

        result = []
        last_was_debug = False

        for ir in irs:
            if ir.ir_type == IRType.DEBUG_INFO:
                if last_was_debug:
                    # 如果前一条也是DEBUG_INFO，则替换它
                    result[-1] = ir
                else:
                    # 否则添加此DEBUG_INFO
                    result.append(ir)
                    last_was_debug = True
            else:
                # 非DEBUG_INFO指令直接添加
                result.append(ir)
                last_was_debug = False

        return result
    def generate(self, node) -> List[IR]:
        irs = self.generate_without_redirect(node)
        irs = self.retain_latest_debug_info(irs)
        return self.redirect_jump(irs)
