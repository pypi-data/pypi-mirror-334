from .lexer import XLangTokenizer
from .ast import Gather, XLangASTParser


def build_ast(doc):
    tokenizer = XLangTokenizer()
    tokens = tokenizer.parse(doc)
    gather = Gather(tokens)
    gathered = gather.gather()
    parser = XLangASTParser(gathered)
    ast = parser.parse_without_body()
    return ast
