from lark import Lark
from lark.exceptions import UnexpectedToken
from utils import multi_line_input


LALR_PARSER = "lalr"

grammar = """
    start : (macro)* (decl)+
    macro: "import" STRING
    decl : variable_decl | function_decl | class_decl | interface_decl
    variable_decl : variable ";"
    variable : type IDENT 
    type : "int" | "double" | "bool" | "string" | IDENT | type bracket
    bracket: /\\[\\s*\\]/  
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
    printstmt : "print" "(" expr (","expr)* ")" ";" 
    expr : lvalue "=" expr | constant | lvalue | "this" | call | "(" expr ")" | expr "+" expr | expr "-" expr 
            | expr "*" expr | expr "/" expr | expr "%" expr | "-" expr | expr "<" expr | expr "<=" expr  
            | expr ">" expr| expr ">=" expr | expr "==" expr | expr "!=" expr | expr "&&" expr | expr "||" expr
            | "!" expr | "ReadInteger" "(" ")" |   "readLine" "(" ")" | "new" IDENT | "NewArray" "(" expr "," type ")" 
            | "itod" "(" expr ")" | "dtoi" "(" expr ")" | "itob" "(" expr ")" | "btoi" "(" expr ")"
    lvalue : IDENT | expr "." IDENT | expr "[" expr "]" 
    call : IDENT  "(" actuals ")" | expr "." IDENT "(" actuals ")" 
    actuals :  expr ("," expr)* |  
    constant : INT | DOUBLE | BOOL | STRING | "null"
    
    DOUBLE.2 : /(\d)+\.(\d)*((E|e)(\+|-)?(\d)+)?/
    INT : /0(x|X)([a-f]|[A-F]|[0-9])+/ | /[0-9]+/
    BOOL.2 : /true\\b/ | /false\\b/
    STRING : /"[^"\\n]*"/
    IDENT : /\\b(?!(int|void|double|bool|string|class|interface|null|this|extends|implements|for|while|if|else|return|break|continue|new|NewArray|Print|ReadInteger|ReadLine|dtoi|itod|btoi|itob|private|protected|public|import)\\b)([a-zA-Z])((\d)|[_a-zA-Z])*\\b/
    
    INLINE_COMMENT : /\/\/.*/
    MULTILINE_COMMENT : /\/\*(\*(?!\/)|[^*])*\*\//
    %import common.WS -> WHITESPACE
    %ignore WHITESPACE
    %ignore INLINE_COMMENT
    %ignore MULTILINE_COMMENT
"""


def parse(text):
    parser = Lark(grammar, parser=LALR_PARSER)
    try:
        _ = parser.parse(text)
    except Exception:
        return "Syntax Error"

    return "OK"


if __name__ == "__main__":
    text = multi_line_input()
    print(parse(text))
