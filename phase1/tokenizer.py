import re 
from lark import Lark
from lark.lexer import Token

LALR_PARSER = "lalr"
TYPES_NOT_TO_REPRESENT = ('OPERATOR', 'PUNCTUATION', 'KEYWORD')
UNDEFINED_TOKEN = "UNDEFINED_TOKEN"

grammar = """
    start : (T_INTLITERAL | T_BOOLEANLITERAL | T_STRINGLITERAL | OPERATOR
            | KEYWORD | PUNCTUATION | T_DOUBLELITERAL 
            | T_ID | INLINE_COMMENT | MULTILINE_COMMENT | UNDEFINED_TOKEN)*
    
    T_DOUBLELITERAL.2 : /(\d)+\.(\d)*((E|e)(\+|-)?(\d)+)?/
    
    KEYWORD.2 : /void\\b/ | /int\\b/ | /double\\b/ | /bool\\b/ | /string\\b/ 
            | /class\\b/ | /interface\\b/ | /null\\b/ | /this\\b/ | /extends\\b/ 
            | /implements\\b/ | /for\\b/ | /while\\b/ | /if\\b/ | /else\\b/ | /return\\b/ 
            | /break\\b/ | /continue\\b/ | /new\\b/ | /NewArray\\b/ | /Print\\b/ | /ReadInteger\\b/ 
            | /ReadLine\\b/ | /dtoi\\b/ | /itod\\b/ | /btoi\\b/ | /itob\\b/ | /private\\b/ 
            | /protected\\b/ | /public\\b/ | /import\\b/ 
    
    T_INTLITERAL : /0(x|X)([a-f]|[A-F]|[0-9])+/ | /[0-9]+/
    
    T_BOOLEANLITERAL.2 : /true\\b/ | /false\\b/
    
    OPERATOR : "+" | "-" | "*" | "/" | "%"
            | "<" | "<=" | ">" | ">=" | "=" | "==" | "!=" 
            | "&&" | "||" | "!" 
    
    PUNCTUATION : ";" | "," | "." | "[" | "]" | "(" | ")" | "{" | "}"
    
    T_ID : /([a-zA-Z])((\d)|[_a-zA-Z])*/
    
    INLINE_COMMENT : /\/\/.*/
    
    MULTILINE_COMMENT : /\/\*(\*(?!\/)|[^*])*\*\//
    
    UNDEFINED_TOKEN.0 : /([.]|_)+/
    %import common.WS -> WHITESPACE
    %import common.ESCAPED_STRING -> T_STRINGLITERAL
    %ignore WHITESPACE
    %ignore INLINE_COMMENT
    %ignore MULTILINE_COMMENT
"""

class UndefinedToken(Exception):
    pass

def prettify_token(token: Token, types_not_to_represent=TYPES_NOT_TO_REPRESENT):
    if token.type == UNDEFINED_TOKEN:
        raise UndefinedToken

    if token.type in types_not_to_represent:
        return token.value

    return f"{token.type} {token.value}"

def tokenize(inputfile,lines):

    text = preprocessor(inputfile,lines)
    parser = Lark(grammar, parser=LALR_PARSER)
    result = parser.parse(text)
    prettified_tokens = []
    for token in result.children:
        try:
            prettified_tokens.append(prettify_token(token))
        except UndefinedToken:
            prettified_tokens.append(UNDEFINED_TOKEN)
            break

    return '\n'.join(prettified_tokens)

def extract_macros(line,macroDict):
    m = re.match(r"(?P<define>define)(\s+)(?P<phrase>\w+)(\s+)(?P<content>[^\n]+)", line)
    if(m == None):
        return False
    # print("Macro: ",m.group('define'))
    # print("Phrase: ",m.group('phrase'))
    # print("Content: ",m.group('content'))
    macroDict[m.group('phrase')] = m.group('content')
    return True
    
def replaceMacros(line,macroDict):

    string_matches = re.finditer("\"[^\"|^\n]*\"",line)
    for key in macroDict:
        value = macroDict[key]
        p = re.compile("\\b" + key + "\\b")
        macro_matches = re.finditer(p,line)
        for macro in macro_matches:
            is_inside = False
            for s_match in string_matches:
                if(s_match.start()<= macro.start() and s_match.end() >= macro.end()):
                    is_inside = True
                    break
            if(not(is_inside)):
                line = line[:macro.start()] + value + line[macro.end():]

    return line

def preprocessor(inputfile,lines):
    
    macroDict = {}
    macroLines = []

    for line in lines:
            if(not(extract_macros(line,macroDict))):
                macroLines.append(line)
    # todo change Macros to exactly what they should look like.
    finalResult = []
    for line in macroLines:
        finalResult.append(replaceMacros(line,macroDict))

    file_name = inputfile.split('.')[0] + '.pre'
    with open("pre/" + file_name, 'w') as f:
        for line in finalResult:
            f.write(line)

    with open("pre/" + file_name, 'r') as f:
        return f.read()

