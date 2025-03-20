from .lexer import XLangTokenizer, XLangTokenType
import enum
from enum import auto


class NextToken:
    # 用于获取下一个token list的类，自动匹配括号

    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def next(self, start_idx: int):
        stack = []
        next_tokens = []
        if start_idx >= len(self.tokens):
            return next_tokens
        while True:
            if (
                self.tokens[start_idx]["token"] in ("{", "[", "(")
                and self.tokens[start_idx]["type"] == XLangTokenType.TokenType_SYMBOL
            ):
                stack.append(self.tokens[start_idx]["token"])
                next_tokens.append(self.tokens[start_idx])
            elif (
                self.tokens[start_idx]["token"] in ("}", "]", ")")
                and self.tokens[start_idx]["type"] == XLangTokenType.TokenType_SYMBOL
            ):
                if len(stack) == 0:
                    return next_tokens
                    # raise Exception('Unmatched bracket')
                poped = stack.pop()
                if (
                    (poped == "{" and self.tokens[start_idx]["token"] != "}")
                    or (poped == "[" and self.tokens[start_idx]["token"] != "]")
                    or (poped == "(" and self.tokens[start_idx]["token"] != ")")
                ):
                    raise Exception("Unmatched bracket")

                next_tokens.append(self.tokens[start_idx])
            else:
                next_tokens.append(self.tokens[start_idx])
            start_idx += 1
            if len(stack) == 0 or start_idx >= len(self.tokens):
                break
        return next_tokens


class Gather:
    # 将token list中的token按照括号匹配进行分组，方便后续处理
    def __init__(self, tokens):
        self.tokens = tokens

    def gather(self):
        gathered = []
        offset = 0
        while next_token := NextToken(self.tokens).next(offset):
            gathered.append(next_token)
            offset += len(next_token)
        return gathered


def _is_body(token_list):
    if len(token_list) < 2:
        return False
    return token_list[0]["token"] == "{" and token_list[-1]["token"] == "}"


def _unwrap_body(token_list):
    if len(token_list) < 2:
        return []
    return token_list[1:-1]


def _is_pair(token_list):
    if len(token_list) < 2:
        return False
    return token_list[0]["token"] == "[" and token_list[-1]["token"] == "]"


def _unwrap_pair(token_list):
    if len(token_list) < 2:
        return []
    return token_list[1:-1]


def _is_tuple(token_list):
    if len(token_list) < 2:
        return False
    return token_list[0]["token"] == "(" and token_list[-1]["token"] == ")"


def _unwrap_tuple(token_list):
    if len(token_list) < 2:
        return []
    return token_list[1:-1]


def _is_let(token_list):
    if len(token_list) != 1:
        return False
    return (
        token_list[0]["token"] == ":="
        and token_list[0]["type"] == XLangTokenType.TokenType_SYMBOL
    )


def _is_assign(token_list):
    if len(token_list) != 1:
        return False
    return (
        token_list[0]["token"] == "="
        and token_list[0]["type"] == XLangTokenType.TokenType_SYMBOL
    )


def _concat(token_list):
    return "".join([token["token"] for token in token_list])


def _is_to(token_list):
    if len(token_list) != 1:
        return False
    return (
        token_list[0]["token"] == "->"
        and token_list[0]["type"] == XLangTokenType.TokenType_SYMBOL
    )


def _is_separator(token_list):
    if len(token_list) != 1:
        return False
    return (
        token_list[0]["token"] == ";"
        and token_list[0]["type"] == XLangTokenType.TokenType_SYMBOL
    )


def _is_comma(token_list):
    if len(token_list) != 1:
        return False
    return (
        token_list[0]["token"] == ","
        and token_list[0]["type"] == XLangTokenType.TokenType_SYMBOL
    )


def _is_string(token_list):
    if len(token_list) != 1:
        return False
    return token_list[0]["type"] == XLangTokenType.TokenType_STRING


def _is_number(token_list):
    if len(token_list) != 1:
        return False
    return token_list[0]["type"] == XLangTokenType.TokenType_NUMBER


def _is_symbol(token_list, symbol):
    if len(token_list) != 1:
        return False
    return (
        token_list[0]["token"] == symbol
        and token_list[0]["type"] == XLangTokenType.TokenType_SYMBOL
    )


def _is_identifier(token_list, symbol):
    if len(token_list) != 1:
        return False
    return (
        token_list[0]["type"] == XLangTokenType.TokenType_IDENTIFIER
        and token_list[0]["token"] == symbol
    )


class XLangASTNodeTypes(enum.Enum):
    NONE = auto()
    NULL = auto()
    STRING = auto()
    BOOLEN = auto()
    NUMBER = auto()
    VARIABLE = auto()
    LET = auto()
    NEVERRETURN = auto()
    BODY = auto()
    ASSIGN = auto()
    FUNCTION_DEF = auto()
    SEPARATOR = auto()
    FUNCTION_CALL = auto()
    OPERATION = auto()
    TUPLE = auto()
    KEY_VAL = auto()
    INDEX_OF = auto()
    GET_ATTR = auto()
    RETURN = auto()
    IF = auto()
    WHILE = auto()
    MODIFY = auto()
    NAMED_ARGUMENT = auto()
    BREAK = auto()
    CONTINUE = auto()


class XLangASTNode:
    def __init__(self, node_type: XLangASTNodeTypes, children, node_position=None):
        self.node_type = node_type
        self.children = children
        self.node_position = node_position  # 用于记录节点在源代码中的位置

    def __str__(self):
        return f"{self.node_type.name} {self.children}"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        if isinstance(self.children, XLangASTNode):
            return {
                "type": self.node_type.name,
                "children": self.children.to_dict(),
                "position": self.node_position,
            }
        if isinstance(self.children, list):
            return {
                "type": self.node_type.name,
                "children": [
                    child.to_dict() if isinstance(child, XLangASTNode) else child
                    for child in self.children
                ],
                "position": self.node_position,
            }
        if self.children is None:
            return {
                "type": self.node_type.name,
                "position": self.node_position,
            }
        return {
            "type": self.node_type.name,
            "children": self.children,
            "position": self.node_position,
        }
class NodeMatcher:
    def __init__(self):
        self.matchers = {}
        self.matcher_order = []

    def register(self, priority: int):
        """装饰器，用于注册匹配器并指定优先级"""

        def decorator(matcher_class):
            self.matchers[matcher_class.__name__] = matcher_class
            # 按优先级插入
            for i, (p, _) in enumerate(self.matcher_order):
                if priority > p:
                    self.matcher_order.insert(i, (priority, matcher_class.__name__))
                    break
            else:
                self.matcher_order.append((priority, matcher_class.__name__))
            return matcher_class

        return decorator

    def match(self, token_list, start_idx, skip_priority=None):
        """按优先级顺序尝试匹配"""

        if token_list is None or len(token_list) == 0:
            return XLangASTNode(XLangASTNodeTypes.NONE, None), 0
        for priority, matcher_name in self.matcher_order:
            if skip_priority is not None and priority >= skip_priority:
                continue
            matcher_class = self.matchers[matcher_name]
            matcher = matcher_class(token_list)
            node, offset = matcher.match(start_idx)
            if node:
                return node, offset
        return None, 0


node_matcher = NodeMatcher()


@node_matcher.register(priority=70)
class XLangSeparator:
    # 匹配 ;
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        # 后向匹配，先搜索分号
        offset = 0

        left = []
        separated = []
        last_offset = 0
        while start_idx + offset < len(self.token_list):
            if _is_separator(self.token_list[start_idx + offset]):
                node, node_offset = node_matcher.match(left, 0)
                if not node:
                    return None, 0
                if node_offset != len(left):
                    raise Exception(
                        "Invalid separator: Left side can't be fully matched: ", left
                    )
                separated.append(node)
                left = []
                offset += 1
                last_offset = offset
            else:
                left.append(self.token_list[start_idx + offset])
                offset += 1
        if len(separated) == 0:
            return None, 0
        node, node_offset = node_matcher.match(left, 0)
        if not node:
            return None, 0
        return (
            XLangASTNode(
                XLangASTNodeTypes.SEPARATOR,
                separated + [node],
                self.token_list[start_idx][0]["position"],
            ),
            last_offset + node_offset,
        )


@node_matcher.register(priority=60)
# 匹配 return xxx
class XLangReturn:
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        if start_idx + 1 >= len(self.token_list):
            return None, 0
        if not _is_identifier(self.token_list[start_idx], "return"):
            return None, 0
        guess, offset = node_matcher.match(self.token_list, start_idx + 1)
        if not guess:
            return None, 0
        return (
            XLangASTNode(
                XLangASTNodeTypes.RETURN,
                guess,
                self.token_list[start_idx][0]["position"],
            ),
            offset + 1,
        )


@node_matcher.register(priority=59)
class XLangTuple:
    # 匹配 xxx, xxx, ...
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        offset = 0

        left = []
        separated = []
        last_offset = 0
        while start_idx + offset < len(self.token_list):
            if _is_comma(self.token_list[start_idx + offset]):
                node, node_offset = node_matcher.match(left, 0)
                if not node:
                    return None, 0
                if node_offset != len(left):
                    raise Exception(
                        "Invalid tuple: Left side can't be fully matched: ", left
                    )
                separated.append(node)
                left = []
                offset += 1
                last_offset = offset
            else:
                left.append(self.token_list[start_idx + offset])
                offset += 1
        if len(separated) == 0:
            return None, 0
        node, node_offset = node_matcher.match(left, 0)
        if not node:
            return None, 0
        return (
            XLangASTNode(
                XLangASTNodeTypes.TUPLE,
                separated + [node],
                self.token_list[start_idx][0]["position"],
            ),
            last_offset + node_offset,
        )


@node_matcher.register(priority=40)
class XLangLet:
    # 匹配 xxx := xxx
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        if start_idx + 2 >= len(self.token_list):
            return None, 0
        if not _is_let(self.token_list[start_idx + 1]):
            return None, 0

        left = Gather(self.token_list[start_idx]).gather()

        right_guess, offset = node_matcher.match(
            self.token_list, start_idx + 2
        )  # 尝试匹配右边的表达式
        if not right_guess:
            return None, 0

        left_node, left_offset = node_matcher.match(left, 0)
        if not left_node:
            return None, 0
        if left_offset != len(left):
            raise Exception("Invalid let: Left side can't be fully matched: ", left)
        if (
            left_node.node_type != XLangASTNodeTypes.VARIABLE
            and left_node.node_type != XLangASTNodeTypes.STRING
        ):
            raise Exception(
                "Invalid let: Left side must be a variable or a string: ", left
            )
        right_node = right_guess
        return (
            XLangASTNode(
                XLangASTNodeTypes.LET,
                [left_node, right_node],
                self.token_list[start_idx][0]["position"],
            ),
            offset + 2,
        )


@node_matcher.register(priority=30)
class XLangAssign:
    # 匹配 xxx = xxx
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        # 向右搜索 = 符号
        offset = 0
        left_tokens = []
        while start_idx + offset < len(self.token_list):
            if _is_assign(self.token_list[start_idx + offset]):
                # 找到 = 符号
                break
            left_tokens.append(self.token_list[start_idx + offset])
            offset += 1

        if start_idx + offset >= len(self.token_list) or not _is_assign(
            self.token_list[start_idx + offset]
        ):
            return None, 0  # 没找到 = 符号

        # 对左侧进行解析
        left_node, left_offset = node_matcher.match(left_tokens, 0)
        if not left_node:
            return None, 0
        if left_offset != len(left_tokens):
            raise Exception(
                "Invalid assign: Left side can't be fully matched: ", left_tokens
            )

        # 对右侧进行解析
        right_guess, right_offset = node_matcher.match(
            self.token_list, start_idx + offset + 1
        )
        if not right_guess:
            return None, 0

        return (
            XLangASTNode(
                XLangASTNodeTypes.ASSIGN,
                [left_node, right_guess],
                self.token_list[start_idx][0]["position"],
            ),
            offset + right_offset + 1,  # +1 是因为 = 符号
        )


@node_matcher.register(priority=23)
class XLangNamedArgument:
    # 匹配 xxx => xxx
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        if start_idx + 2 >= len(self.token_list):
            return None, 0
        if not _is_symbol(self.token_list[start_idx + 1], "=>"):
            return None, 0

        left = Gather(self.token_list[start_idx]).gather()

        right_guess, offset = node_matcher.match(self.token_list, start_idx + 2)

        left_node, left_offset = node_matcher.match(left, 0)
        if not left_node:
            return None, 0
        if left_offset != len(left):
            raise Exception(
                "Invalid named argument: Left side can't be fully matched: ", left
            )
        if left_node.node_type == XLangASTNodeTypes.VARIABLE:
            left_node.node_type = XLangASTNodeTypes.STRING  # 将变量名转换为字符串
        right_node = right_guess
        return (
            XLangASTNode(
                XLangASTNodeTypes.NAMED_ARGUMENT,
                [left_node, right_node],
                self.token_list[start_idx][0]["position"],
            ),
            offset + 2,
        )


@node_matcher.register(priority=22)
class XLangKeyVal:
    # 匹配 xxx: xxx
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        if start_idx + 2 >= len(self.token_list):
            return None, 0
        if not _is_symbol(self.token_list[start_idx + 1], ":"):
            return None, 0

        left = Gather(self.token_list[start_idx]).gather()

        right_guess, offset = node_matcher.match(self.token_list, start_idx + 2)

        left_node, left_offset = node_matcher.match(left, 0)
        if not left_node:
            return None, 0
        if left_offset != len(left):
            raise Exception(
                "Invalid key value pair: Left side can't be fully matched: ", left
            )
        right_node = right_guess
        return (
            XLangASTNode(
                XLangASTNodeTypes.KEY_VAL,
                [left_node, right_node],
                self.token_list[start_idx][0]["position"],
            ),
            offset + 2,
        )


@node_matcher.register(priority=21)
class XLangWhile:
    # 匹配 while xxx xxx
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        if start_idx + 2 >= len(self.token_list):
            return None, 0
        if not _is_identifier(self.token_list[start_idx], "while"):
            return None, 0

        condition = Gather(self.token_list[start_idx + 1]).gather()
        condition, _ = node_matcher.match(condition, 0)
        if not condition:
            return None, 0

        body_guess, offset = node_matcher.match(self.token_list, start_idx + 2)
        if not body_guess:
            return None, 0

        return (
            XLangASTNode(
                XLangASTNodeTypes.WHILE,
                [condition, body_guess],
                self.token_list[start_idx][0]["position"],
            ),
            offset + 2,
        )


@node_matcher.register(priority=19)
class XLangIF:
    # 匹配 if xxx xxx else xxx 或者 if xxx xxx （没有else），右值猜测最大长度
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        if start_idx + 2 >= len(self.token_list):
            return None, 0
        if not _is_identifier(self.token_list[start_idx], "if"):
            return None, 0

        condition = Gather(self.token_list[start_idx + 1]).gather()
        true_condition = Gather(self.token_list[start_idx + 2]).gather()
        condition, _ = node_matcher.match(condition, 0)
        if not condition:
            return None, 0
        true_condition, _ = node_matcher.match(true_condition, 0)
        if not true_condition:
            return None, 0

        if start_idx + 3 < len(self.token_list) and _is_identifier(
            self.token_list[start_idx + 3], "else"
        ):
            false_node, false_offset = node_matcher.match(
                self.token_list, start_idx + 4
            )
            if not false_node:
                return None, 0
            return (
                XLangASTNode(
                    XLangASTNodeTypes.IF,
                    [condition, true_condition, false_node],
                    self.token_list[start_idx][0]["position"],
                ),
                4 + false_offset,
            )

        return (
            XLangASTNode(
                XLangASTNodeTypes.IF,
                [condition, true_condition],
                self.token_list[start_idx][0]["position"],
            ),
            3,
        )


@node_matcher.register(priority=20) 
class XLangControlFlow:
    """匹配break和continue"""

    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        if start_idx >= len(self.token_list):
            return None, 0

        # 检查是否为break关键字
        if _is_identifier(self.token_list[start_idx], "break"):
            right_tokens = self.token_list[start_idx + 1 :]

            right, offset = node_matcher.match(right_tokens, 0)
            if not right:
                return None, 0
            if offset != len(right_tokens):
                raise Exception(
                    "Invalid break: Right side can't be fully matched: ", right_tokens
                )

            return (
                XLangASTNode(
                    XLangASTNodeTypes.BREAK,
                    right,
                    self.token_list[start_idx][0]["position"],
                ),
                offset + 1,
            )
        # 检查是否为continue关键字
        if _is_identifier(self.token_list[start_idx], "continue"):
            right_tokens = self.token_list[start_idx + 1 :]

            right, offset = node_matcher.match(right_tokens, 0)
            if not right:
                return None, 0
            if offset != len(right_tokens):
                raise Exception(
                    "Invalid break: Right side can't be fully matched: ", right_tokens
                )

            return (
                XLangASTNode(
                    XLangASTNodeTypes.CONTINUE,
                    right,
                    self.token_list[start_idx][0]["position"],
                ),
                offset + 1,
            )

        return None, 0


@node_matcher.register(priority=14)
class XLangOr:
    # 逻辑运算符: or
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        # 从右向左搜索运算符
        offset = len(self.token_list) - start_idx - 1

        # 从末尾向左搜索第一个 && 或 || 运算符
        operation = None
        operation_pos = -1

        while offset >= 0:
            pos = start_idx + offset
            if _is_identifier(self.token_list[pos], "or"):
                operation = self.token_list[pos][0]["token"]
                operation_pos = pos
                break
            offset -= 1

        if operation is None:
            return None, 0  # 没有找到运算符

        # 左侧部分
        left_tokens = self.token_list[start_idx:operation_pos]
        # 右侧部分
        right_tokens = self.token_list[operation_pos + 1 :]

        # 解析左侧表达式
        left_node, left_offset = node_matcher.match(left_tokens, 0)
        if not left_node or left_offset != len(left_tokens):
            return None, 0

        # 解析右侧表达式
        right_node, right_offset = node_matcher.match(right_tokens, 0)
        if not right_node or right_offset != len(right_tokens):
            return None, 0

        # 构建操作节点
        return (
            XLangASTNode(
                XLangASTNodeTypes.OPERATION, [left_node, operation, right_node]
            ),
            len(self.token_list) - start_idx,  # 返回整个匹配长度
        )


@node_matcher.register(priority=13)
class XLangAnd:
    # 逻辑运算符: and
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        # 从右向左搜索运算符
        offset = len(self.token_list) - start_idx - 1

        # 从末尾向左搜索第一个 && 或 || 运算符
        operation = None
        operation_pos = -1

        while offset >= 0:
            pos = start_idx + offset
            if _is_identifier(self.token_list[pos], "and"):
                operation = self.token_list[pos][0]["token"]
                operation_pos = pos
                break
            offset -= 1

        if operation is None:
            return None, 0  # 没有找到运算符

        # 左侧部分
        left_tokens = self.token_list[start_idx:operation_pos]
        # 右侧部分
        right_tokens = self.token_list[operation_pos + 1 :]

        # 解析左侧表达式
        left_node, left_offset = node_matcher.match(left_tokens, 0)
        if not left_node or left_offset != len(left_tokens):
            return None, 0

        # 解析右侧表达式
        right_node, right_offset = node_matcher.match(right_tokens, 0)
        if not right_node or right_offset != len(right_tokens):
            return None, 0

        # 构建操作节点
        return (
            XLangASTNode(
                XLangASTNodeTypes.OPERATION, [left_node, operation, right_node]
            ),
            len(self.token_list) - start_idx,  # 返回整个匹配长度
        )


@node_matcher.register(priority=12)
class XLangNot:
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        if start_idx >= len(self.token_list):
            return None, 0
        if not _is_identifier(self.token_list[start_idx], "not"):
            return None, 0

        # 解析右侧表达式
        right_guess, right_offset = node_matcher.match(self.token_list, start_idx + 1)
        if not right_guess:
            return None, 0

        return (
            XLangASTNode(XLangASTNodeTypes.OPERATION, ["not", right_guess]),
            right_offset + 1,  # 返回整个匹配长度
        )


@node_matcher.register(priority=11)
class XLangOperatorLevel2:
    # 比较运算符: >, <, >=, <=, ==, !=
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        # 从右向左搜索运算符
        offset = len(self.token_list) - start_idx - 1

        # 从末尾向左搜索第一个比较运算符
        operation = None
        operation_pos = -1

        while offset >= 0:
            pos = start_idx + offset
            if (
                _is_symbol(self.token_list[pos], ">")
                or _is_symbol(self.token_list[pos], "<")
                or _is_symbol(self.token_list[pos], ">=")
                or _is_symbol(self.token_list[pos], "<=")
                or _is_symbol(self.token_list[pos], "==")
                or _is_symbol(self.token_list[pos], "!=")
            ):
                operation = self.token_list[pos][0]["token"]
                operation_pos = pos
                break
            offset -= 1

        if operation is None:
            return None, 0  # 没有找到运算符

        # 左侧部分
        left_tokens = self.token_list[start_idx:operation_pos]
        # 右侧部分
        right_tokens = self.token_list[operation_pos + 1 :]

        # 解析左侧表达式
        left_node, left_offset = node_matcher.match(left_tokens, 0)
        if not left_node or left_offset != len(left_tokens):
            return None, 0

        # 解析右侧表达式
        right_node, right_offset = node_matcher.match(right_tokens, 0)
        if not right_node or right_offset != len(right_tokens):
            return None, 0

        # 构建操作节点
        return (
            XLangASTNode(
                XLangASTNodeTypes.OPERATION, [left_node, operation, right_node]
            ),
            len(self.token_list) - start_idx,  # 返回整个匹配长度
        )


@node_matcher.register(priority=10)
class XLangOperatorLevel1:
    # +, -
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        # 从右向左搜索运算符
        offset = len(self.token_list) - start_idx - 1

        # 从末尾向左搜索第一个 + 或 - 运算符
        operation = None
        operation_pos = -1

        while offset >= 0:
            pos = start_idx + offset
            if _is_symbol(self.token_list[pos], "+") or _is_symbol(
                self.token_list[pos], "-"
            ):
                operation = self.token_list[pos][0]["token"]
                operation_pos = pos
                # 判断是否为一元运算符
                is_unary = False

                # 检查是否在表达式起始位置
                if operation_pos == start_idx:
                    is_unary = True
                # 检查前一个token是否为运算符或者左括号等，表明这是一个一元运算符
                elif operation_pos > start_idx:
                    prev_token = self.token_list[operation_pos - 1]
                    if (
                        len(prev_token) == 1
                        and prev_token[0]["type"] == XLangTokenType.TokenType_SYMBOL
                        and prev_token[0]["token"]
                        in [
                            "+",
                            "-",
                            "*",
                            "/",
                            "%",
                            "&&",
                            "||",
                            "==",
                            "!=",
                            "<",
                            ">",
                            "<=",
                            ">=",
                        ]
                    ):
                        is_unary = True

                # 如果是一元运算符，继续搜索，否则退出循环
                if is_unary and operation_pos > start_idx:
                    offset -= 1
                    continue
                break
            offset -= 1

        if operation is None:
            return None, 0  # 没有找到运算符

        # 左侧部分
        left_tokens = self.token_list[start_idx:operation_pos]
        # 右侧部分
        right_tokens = self.token_list[operation_pos + 1 :]

        # 特殊处理一元运算符（+x, -x）的情况
        if len(left_tokens) == 0 or (
            operation_pos > start_idx
            and self.token_list[operation_pos - 1][0]["type"]
            == XLangTokenType.TokenType_SYMBOL
            and self.token_list[operation_pos - 1][0]["token"]
            in [
                "+",
                "-",
                "*",
                "/",
                "%",
                "&&",
                "||",
                "==",
                "!=",
                "<",
                ">",
                "<=",
                ">=",
            ]
        ):
            # 解析右侧表达式
            right_node, right_offset = node_matcher.match(right_tokens, 0)
            if not right_node or right_offset != len(right_tokens):
                return None, 0

            return (
                XLangASTNode(
                    XLangASTNodeTypes.OPERATION,
                    [operation, right_node],
                    self.token_list[start_idx][0]["position"],
                ),
                len(self.token_list) - start_idx,
            )

        # 解析左侧表达式
        left_node, left_offset = node_matcher.match(left_tokens, 0)
        if not left_node or left_offset != len(left_tokens):
            return None, 0

        # 解析右侧表达式
        right_node, right_offset = node_matcher.match(right_tokens, 0)
        if not right_node or right_offset != len(right_tokens):
            return None, 0

        # 构建操作节点
        return (
            XLangASTNode(
                XLangASTNodeTypes.OPERATION, [left_node, operation, right_node]
            ),
            len(self.token_list) - start_idx,  # 返回整个匹配长度
        )


@node_matcher.register(priority=9)
class XLangOperatorLevel0:
    # *, /, %（更高优先级）
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        # 从右向左搜索运算符
        offset = len(self.token_list) - start_idx - 1

        # 从末尾向左搜索第一个 *、/ 或 % 运算符
        operation = None
        operation_pos = -1

        while offset >= 0:
            pos = start_idx + offset
            if (
                _is_symbol(self.token_list[pos], "*")
                or _is_symbol(self.token_list[pos], "/")
                or _is_symbol(self.token_list[pos], "%")
            ):
                operation = self.token_list[pos][0]["token"]
                operation_pos = pos
                break
            offset -= 1

        if operation is None:
            return None, 0  # 没有找到运算符

        # 左侧部分
        left_tokens = self.token_list[start_idx:operation_pos]
        # 右侧部分
        right_tokens = self.token_list[operation_pos + 1 :]

        # 解析左侧表达式
        left_node, left_offset = node_matcher.match(left_tokens, 0)
        if not left_node or left_offset != len(left_tokens):
            return None, 0

        # 解析右侧表达式
        right_node, right_offset = node_matcher.match(right_tokens, 0)
        if not right_node or right_offset != len(right_tokens):
            return None, 0

        # 构建操作节点
        return (
            XLangASTNode(
                XLangASTNodeTypes.OPERATION, [left_node, operation, right_node]
            ),
            len(self.token_list) - start_idx,  # 返回整个匹配长度
        )

@node_matcher.register(priority=4)
class XLangFunctionDef:
    # 匹配 (xxx) -> {xxx}
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        if start_idx + 2 >= len(self.token_list):
            return None, 0
        if (
            not _is_tuple(self.token_list[start_idx])
            or not _is_to(self.token_list[start_idx + 1])
        ):
            return None, 0

        left_node, left_offset = node_matcher.match(
            Gather(self.token_list[start_idx]).gather(), 0
        )
        if not left_node:
            return None, 0
        right_node = XLangASTParser(
            Gather(self.token_list[start_idx + 2]).gather()
        ).parse_body(start_idx=0)
        if not right_node:
            return None, 0
        return (
            XLangASTNode(
                XLangASTNodeTypes.FUNCTION_DEF,
                [left_node, right_node],
                self.token_list[start_idx][0]["position"],
            ),
            3,
        )


@node_matcher.register(priority=3)
class XLangModifier:
    # 匹配 modifier xxx
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        if start_idx + 1 >= len(self.token_list):
            return None, 0
        if len(self.token_list[start_idx]) == 1 and self.token_list[start_idx][0][
            "token"
        ] in ["copy", "ref", "deref", "keyof", "valueof", "selfof", "assert", "import", "wrap"]:
            node, offset = node_matcher.match(self.token_list, start_idx + 1)
            if node == None:
                return None, 0
            return (
                XLangASTNode(
                    XLangASTNodeTypes.MODIFY,
                    [self.token_list[start_idx][0]["token"], node],
                ),
                offset + 1,
            )
        return None, 0


@node_matcher.register(priority=2)
class XLangMemberAccess:
    """匹配成员访问操作：xxx[xxx] 和 xxx.xxx 和 xxx(xxx)"""

    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        # 从右向左搜索访问操作符
        offset = len(self.token_list) - start_idx - 1

        # 从末尾向左搜索第一个 [], . 或 () 操作
        access_type = None
        access_pos = -1

        while offset >= 0:
            pos = start_idx + offset

            if _is_pair(self.token_list[pos]):
                access_type = "[]"
                access_pos = pos
                break
            elif pos > start_idx and _is_symbol(self.token_list[pos], "."):
                access_type = "."
                access_pos = pos
                break
            elif _is_tuple(self.token_list[pos]):
                access_type = "()"
                access_pos = pos
                break

            offset -= 1

        if access_type is None:
            return None, 0  # 没有找到访问操作符

        # 左侧部分
        left_tokens = self.token_list[start_idx:access_pos]
        if len(left_tokens) == 0:
            return None, 0
        # 解析左侧表达式
        left_node, left_offset = node_matcher.match(left_tokens, 0)
        if not left_node or left_offset != len(left_tokens):
            return None, 0

        if access_type == "[]":
            # 处理索引访问
            index = Gather(_unwrap_pair(self.token_list[access_pos])).gather()
            index_node, index_offset = node_matcher.match(index, 0)
            if not index_node or index_offset != len(index):
                return None, 0

            return (
                XLangASTNode(
                    XLangASTNodeTypes.INDEX_OF,
                    [left_node, index_node],
                    self.token_list[start_idx][0]["position"],
                ),
                access_pos - start_idx + 1,
            )

        elif access_type == "()":
            # 处理函数调用
            args = Gather(self.token_list[access_pos]).gather()
            args_node, args_offset = node_matcher.match(args, 0)

            if not args_node:
                # 处理空参数情况
                args_node = XLangASTNode(
                    XLangASTNodeTypes.TUPLE,
                    [],
                    self.token_list[start_idx][0]["position"],
                )
            elif args_node.node_type != XLangASTNodeTypes.TUPLE:
                args_node = XLangASTNode(
                    XLangASTNodeTypes.TUPLE,
                    [args_node],
                    self.token_list[start_idx][0]["position"],
                )

            return (
                XLangASTNode(
                    XLangASTNodeTypes.FUNCTION_CALL,
                    [left_node, args_node],
                    self.token_list[start_idx][0]["position"],
                ),
                access_pos - start_idx + 1,
            )

        else:  # access_type == '.'
            # 处理属性访问
            if access_pos + 1 >= len(self.token_list):
                return None, 0

            right_token = self.token_list[access_pos + 1 :]
            right_node, right_offset = node_matcher.match(right_token, 0)
            if not right_node:
                return None, 0

            if right_node.node_type == XLangASTNodeTypes.VARIABLE:
                attr_name = XLangASTNode(
                    XLangASTNodeTypes.STRING,
                    right_node.children,
                    self.token_list[start_idx][0]["position"],
                )

            return (
                XLangASTNode(
                    XLangASTNodeTypes.GET_ATTR,
                    [left_node, attr_name],
                    self.token_list[start_idx][0]["position"],
                ),
                access_pos - start_idx + 1 + right_offset,
            )


@node_matcher.register(priority=1)
class XLangVariable:
    # 匹配变量
    def __init__(self, token_list):
        self.token_list = token_list

    def match(self, start_idx):
        if _is_tuple(self.token_list[start_idx]) or _is_pair(self.token_list[start_idx]):
            unwarped = _unwrap_tuple(self.token_list[start_idx])
            if len(unwarped) == 0:
                return (
                    XLangASTNode(
                        XLangASTNodeTypes.TUPLE,
                        [],
                        self.token_list[start_idx][0]["position"],
                    ),
                    1,
                )
            node, offset = node_matcher.match(Gather(unwarped).gather(), 0)
            if not node:
                return None, 0
            return node, 1
        if _is_body(self.token_list[start_idx]):
            return (
                XLangASTNode(
                    XLangASTNodeTypes.BODY,
                    XLangASTParser(
                        Gather(_unwrap_body(self.token_list[start_idx])).gather()
                    ).parse(),
                    self.token_list[start_idx][0]["position"],
                ),
                1,
            )
        if _is_string(self.token_list[start_idx]):
            return (
                XLangASTNode(
                    XLangASTNodeTypes.STRING,
                    _concat(self.token_list[start_idx]),
                    self.token_list[start_idx][0]["position"],
                ),
                1,
            )
        if _is_number(self.token_list[start_idx]):
            return (
                XLangASTNode(
                    XLangASTNodeTypes.NUMBER,
                    _concat(self.token_list[start_idx]),
                    self.token_list[start_idx][0]["position"],
                ),
                1,
            )
        if _is_identifier(self.token_list[start_idx], "true"):
            return (
                XLangASTNode(
                    XLangASTNodeTypes.BOOLEN,
                    True,
                    self.token_list[start_idx][0]["position"],
                ),
                1,
            )
        if _is_identifier(self.token_list[start_idx], "false"):
            return (
                XLangASTNode(
                    XLangASTNodeTypes.BOOLEN,
                    False,
                    self.token_list[start_idx][0]["position"],
                ),
                1,
            )
        if _is_identifier(self.token_list[start_idx], "null"):
            return (
                XLangASTNode(
                    XLangASTNodeTypes.NULL,
                    None,
                    self.token_list[start_idx][0]["position"],
                ),
                1,
            )
        return (
            XLangASTNode(
                XLangASTNodeTypes.VARIABLE,
                _concat(self.token_list[start_idx]),
                self.token_list[start_idx][0]["position"],
            ),
            1,
        )


class XLangASTParser:
    def __init__(self, token_list):
        self.token_list = token_list
        self.offset = 0

    def parse(self) -> list:  # 返回一个list，每个元素是一个XLangASTNode
        ret = []
        while self.offset < len(self.token_list):
            node, offset = node_matcher.match(self.token_list, self.offset)
            if node:
                ret.append(node)
                self.offset += offset
            else:
                self.offset += 1
        return ret

    def parse_body(self, start_idx=0) -> XLangASTNode:
        if len(self.token_list) == 0:
            return XLangASTNode(
                XLangASTNodeTypes.SEPARATOR,  # 用于表示没有body的情况，仅仅是一组表达式
                [XLangASTNode(XLangASTNodeTypes.NULL, None, 0)],
                0,
            )
        return XLangASTNode(
            XLangASTNodeTypes.SEPARATOR,
            self.parse(),
            self.token_list[start_idx][0]["position"],
        )
    def parse_without_body(self, start_idx=0) -> XLangASTNode:
        if len(self.token_list) == 0:
            return XLangASTNode(
                XLangASTNodeTypes.SEPARATOR, # 用于表示没有body的情况，仅仅是一组表达式
                [XLangASTNode(XLangASTNodeTypes.NULL, None, 0)],
                0,
            )
        return XLangASTNode(
            XLangASTNodeTypes.SEPARATOR, # 用于表示没有body的情况，仅仅是一组表达式
            self.parse(),
            self.token_list[start_idx][0]["position"],
        )
