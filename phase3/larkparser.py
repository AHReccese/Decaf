from lark import Lark
from lark.exceptions import UnexpectedToken
from utils import multi_line_input

LALR_PARSER = "lalr"

grammar = """
    start : (decl)+
    decl : variable_decl | function_decl | class_decl | interface_decl
    variable_decl : variable ";"
    variable : type IDENT 
    type : TYPE | IDENT | type "[]" -> array_type
    function_decl : type IDENT "("formals")" stmt_block  | "void" IDENT "("formals")" stmt_block 
    formals : variable (","variable)* |  
    class_decl : "class" IDENT ("extends" IDENT)?  ("implements" IDENT (","IDENT)*)?  "{"(field)*"}" 
    field : access_mode variable_decl | access_mode function_decl
    access_mode : "private" | "protected" | "public" | 
    interface_decl : "interface" IDENT "{"(prototype)*"}" 
    prototype : type IDENT "(" formals ")" ";" | "void" IDENT "(" formals ")" ";" 
    stmt_block : "{" (variable_decl)*  (stmt)* "}" 
    stmt :  (expr)? ";" | ifstmt  | whilestmt | forstmt | breakstmt | continuestmt | returnstmt | printstmt | stmt_block 
    ifstmt : "if" "(" expr ")" stmt ("else" stmt)? 
    whilestmt : "while" "(" expr ")" stmt 
    forstmt : "for" "(" (expr)? ";" expr ";" (expr)? ")" stmt 
    returnstmt : "return" (expr)? ";" 
    breakstmt : "break" ";" 
    continuestmt : "continue" ";"
    printstmt : "Print" "(" expr (","expr)* ")" ";" 
    expr : lvalue "=" expr -> assignment | exprprio8
    exprprio8 : exprprio8 "||" exprprio7 -> or_expr | exprprio7
    exprprio7 : exprprio7 "&&" exprprio6 -> and_expr| exprprio6
    exprprio6 : exprprio6 "==" exprprio5 -> equal_expr | exprprio6 "!=" exprprio5 -> not_equal_expr| exprprio5
    exprprio5 : exprprio5 "<" exprprio4 -> lt_expr| exprprio5 "<=" exprprio4 -> lte_expr | exprprio5 ">" exprprio4 -> gt_expr | exprprio5 ">=" exprprio4 -> gte_expr | exprprio4
    exprprio4 : exprprio4 "+" exprprio3 -> add | exprprio4 "-" exprprio3 -> sub | exprprio3
    exprprio3 : exprprio3 "*" exprprio2 -> mult | exprprio3 "/" exprprio2 -> divide | exprprio3 "%" exprprio2 | exprprio2
    exprprio2 : "-" exprprio2 -> negate | "!" exprprio2 -> not_expr| exprprio1
    exprprio1 : constant | read_integer "(" ")" -> read_integer_func | "ReadLine" "(" ")" -> read_line_func | "new" IDENT | "NewArray" "(" expr "," type ")" -> new_array | "(" expr ")" -> expr_in_parentheses | lvalue | call | "this" | "itod" "(" expr ")" -> itod_func | "dtoi" "(" expr ")" -> dtoi_func| "itob" "(" expr ")" -> itob_func | "btoi" "(" expr ")" -> btoi_func
    lvalue : IDENT -> ident_lvalue |  exprprio1 "." IDENT | exprprio1 ".length" -> access_array_length | exprprio1 "[" expr "]" -> access_array
    call : IDENT  "(" actuals ")" -> global_func_call|  exprprio1  "."  IDENT  "(" actuals ")" | exprprio1 ".length()" -> access_array_length
    actuals :  expr ("," expr)* |  
    constant : INT | DOUBLE | BOOL | STRING | "null"
    read_integer : "ReadInteger"
    read_line : "ReadLine"
    DOUBLE.2 : /(\d)+\.(\d)*((E|e)(\+|-)?(\d)+)?/
    INT : /0(x|X)([a-f]|[A-F]|[0-9])+/ | /[0-9]+/
    BOOL.2 : /true\\b/ | /false\\b/
    STRING : /"[^"\\n]*"/
    TYPE: "int" | "double" | "bool" | "string"
    IDENT : /\\b(?!(?:int|void|double|bool|string|class|interface|null|this|extends|implements|for|while|if|else|return|break|continue|new|NewArray|Print|ReadInteger|ReadLine|dtoi|itod|btoi|itob|private|protected|public)\\b)([a-zA-Z])((\d)|[_a-zA-Z])*\\b/
    INLINE_COMMENT : "//" /[^\\n]*/ "\\n"
    MULTILINE_COMMENT : "/*" /.*?/ "*/"
    %import common.WS -> WHITESPACE
    %ignore WHITESPACE
    %ignore INLINE_COMMENT
    %ignore MULTILINE_COMMENT
"""


def parse(text):
    parser = Lark(grammar, parser=LALR_PARSER)
    try:
        result = parser.parse(text)
        print(result.pretty())
    except UnexpectedToken:
        return "Syntax Error"
    return "OK"


if __name__ == "__main__":
    text = multi_line_input()
    print(parse(text))
