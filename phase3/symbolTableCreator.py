from copy import copy
from dataclasses import dataclass
from larkparser import grammar
from lark.visitors import Interpreter
from lark import Lark, Token, Tree
from utils import multi_line_input, read_input_file
from semantic_error import SemanticError


@dataclass
class SymbolTableObject:
    label: str = None
    name: str = None
    value: str = None
    type: str = None
    frameOffset: int = None
    base_tree:Tree = None
    is_access_array:bool = False

global_functions = {}
function_name_to_arguments = {}


class SymbolTableCreator(Interpreter):
    def __init__(self):
        self.scope = ["global"]
        self.formal_var_offset = 24
        self.scopes_in_count = 0
        self.local_var_offset = 0
        self.str_const_count = 0

    def start(self, tree):
        for child in tree.children:
            self.visit(child)

    def decl(self, tree):
        for declaration in tree.children:
            if declaration.data in ("variable_decl", "function_decl"):
                self.visit(declaration)

    def function_decl(self, tree):
        isvoid = len(tree.children) == 3
        ident, formals, stmt_block = None, None, None
        if (isvoid):
            func_type = "void"
            ident = tree.children[0].value
            formals = tree.children[1]
            stmt_block = tree.children[2]
        else:
            func_type = tree.children[0].children[0].value
            ident = tree.children[1].value
            formals = tree.children[2]
            stmt_block = tree.children[3]

        self.scope.append(ident)
        label = "_".join(self.scope)
        tree.symbolObject = SymbolTableObject(label=label, name=ident, type=func_type,base_tree=tree)
        global_functions[ident] = tree.symbolObject
        formals.scope_variables = {}
        self.formal_var_offset = 24
        self.visit(formals)
        function_name_to_arguments[ident] = formals.symbolObjects
        tree.formal_vars_size = self.formal_var_offset - 24
        tree.symbolObject.formal_vars_size = tree.formal_vars_size
        stmt_block.scope_variables =  formals.scope_variables.copy()
        self.local_var_offset = 0
        self.visit(stmt_block)
        tree.scope_variables = stmt_block.scope_variables
        tree.local_vars_size = -self.local_var_offset
        self.scope.pop()

    def formals(self, tree):
        self.scope.append("formals")
        variables = tree.children
        tree.symbolObjects = []
        for var in variables:
            self.visit(var)
            variableSymbolObj: SymbolTableObject = var.symbolObject
            variableSymbolObj.frameOffset = self.formal_var_offset
            self.formal_var_offset += 8
            tree.scope_variables[variableSymbolObj.name] = variableSymbolObj
            tree.symbolObjects.append(variableSymbolObj)

        self.scope.pop()

    def variable(self, tree):
        self.visit(tree.children[0])
        var_type = tree.children[0].meta_type
        ident = tree.children[1].value
        label = "_".join(self.scope + [ident])
        tree.symbolObject = SymbolTableObject(type=var_type, name=ident, label=label)

    def type(self,tree):
        tree.meta_type = tree.children[0].value

    def array_type(self,tree):
        tree.meta_type = "array_"+tree.children[0].children[0].value

    def variable_decl(self, tree):
        variable = tree.children[0]
        self.visit(variable)

    def stmt_block(self, tree):
        self.scope.append(str(self.scopes_in_count))
        self.scopes_in_count += 1
        for child in tree.children:
            if child.data == "variable_decl":
                self.visit(child)
                variableSymbolObj: SymbolTableObject = child.children[0].symbolObject
                variableSymbolObj.frameOffset = self.local_var_offset
                self.local_var_offset -= 8
                tree.scope_variables[variableSymbolObj.name] = variableSymbolObj
            elif child.data == "stmt":
                child.scope_variables = tree.scope_variables.copy()
                self.visit(child)
            if hasattr(child, 'function_return_symbolObject'):
                tree.function_return_symbolObject = child.function_return_symbolObject
        self.scope.pop()

    def stmt(self, tree):
        if (len(tree.children) == 0):
            return
        child = tree.children[0]
        child.scope_variables = tree.scope_variables
        self.visit(child)
        if child.data == 'returnstmt':
            tree.function_return_symbolObject = child.meta_symbolObject

    def returnstmt(self,tree):
        if (len(tree.children) == 0):
            return
        child = tree.children[0]
        child.scope_variables = tree.scope_variables
        self.visit(child)
        tree.meta_symbolObject = child.meta_symbolObject

    def printstmt(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def expr(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def exprprio8(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def read_integer_func(self, tree):
        tree.meta_symbolObject = SymbolTableObject(type='int')

    def itod_func(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
        tree.meta_symbolObject = SymbolTableObject(type='double')

    def dtoi_func(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
        tree.meta_symbolObject = SymbolTableObject(type='int')

    def itob_func(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
        tree.meta_symbolObject = SymbolTableObject(type='bool')

    def btoi_func(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
        tree.meta_symbolObject = SymbolTableObject(type='int')

    def read_line_func(self, tree):
        tree.meta_symbolObject = SymbolTableObject(type='string')

    def exprprio1(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def access_array_length(self,tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = copy(child.meta_symbolObject)
            tree.meta_symbolObject.type = "int"

    def exprprio2(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def exprprio3(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def exprprio4(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def exprprio5(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def exprprio6(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def exprprio7(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def or_expr(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def and_expr(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def equal_expr(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
        tree.meta_symbolObject = SymbolTableObject(type="bool")

    def not_equal_expr(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
        tree.meta_symbolObject = SymbolTableObject(type="bool")

    def lt_expr(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
        tree.meta_symbolObject = SymbolTableObject(type="bool")

    def gt_expr(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
        tree.meta_symbolObject = SymbolTableObject(type="bool")

    def lte_expr(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
        tree.meta_symbolObject = SymbolTableObject(type="bool")

    def gte_expr(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
        tree.meta_symbolObject = SymbolTableObject(type="bool")

    def ifstmt(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)

    def whilestmt(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)

    def forstmt(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)

    def breakstmt(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)

    def add(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject
    def negate(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def not_expr(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def sub(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def mult(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def divide(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def new_array(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
        self.visit(tree.children[0])
        child_type = tree.children[1]
        self.visit(child_type)
        tree.meta_symbolObject = SymbolTableObject(type=f"array_{child_type.meta_type}")

    def access_array(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
        tree.meta_symbolObject = copy(tree.children[0].meta_symbolObject)
        tree.meta_symbolObject.type = tree.meta_symbolObject.type.replace("array_","")
        tree.meta_symbolObject.is_access_array = True

        tree.index_symbolObject = tree.children[1].meta_symbolObject

    def expr_in_parentheses(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject

    def assignment(self, tree):
        for child in tree.children:
            child.scope_variables = tree.scope_variables
        self.visit(tree.children[0])
        tree.meta_symbolObject = tree.children[0].meta_symbolObject
        self.visit(tree.children[1])

    def constant(self, tree):
        token: Token = tree.children[0]
        constvalue = token.value
        label = ""
        if token.type == "INT":
            constvalue = int(constvalue)
        elif token.type == "STRING":
            label = f"const_str_{self.str_const_count}"
            self.str_const_count += 1
        elif token.type == "BOOL":
            if constvalue == "true":
                constvalue = 1
            else:
                constvalue = 0
        tree.meta_symbolObject = SymbolTableObject(value=constvalue, type=token.type.lower(), label=label)

    def ident_lvalue(self, tree):
        varName = tree.children[0].value
        if varName not in tree.scope_variables:
            raise SemanticError("Invalid Scope")
        tree.meta_symbolObject = tree.scope_variables[varName]

    def global_func_call(self,tree):
        func_name = tree.children[0].value
        tree.meta_symbolObject = SymbolTableObject(name=func_name)
        actuals = tree.children[1]
        actuals.scope_variables = tree.scope_variables
        self.visit(actuals)
        tree.symbolObjects = actuals.symbolObjects

    def actuals(self,tree):
        tree.symbolObjects = []
        for child in tree.children:
            child.scope_variables = tree.scope_variables
            self.visit(child)
            tree.meta_symbolObject = child.meta_symbolObject
            tree.symbolObjects.append(child.meta_symbolObject)


if __name__ == "__main__":
    text = read_input_file("tests/testcases/t001-io1.d")
    parser = Lark(grammar, parser="lalr")
    parse_tree = parser.parse(text)
    print(parse_tree.pretty())
    SymbolTableCreator().visit(parse_tree)
