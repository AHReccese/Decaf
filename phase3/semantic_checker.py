from lark.visitors import Interpreter
from symbolTableCreator import function_name_to_arguments, global_functions
from semantic_error import SemanticError


class SemanticChecker(Interpreter):
    def assignment(self, tree):
        if  tree.children[0].meta_symbolObject.type != tree.children[1].meta_symbolObject.type:
            raise SemanticError("Invalid type for assignment")

    def function_decl(self, tree):
        self.visit_children(tree)
        isvoid = len(tree.children) == 3
        if (isvoid):
            func_type = "void"
            stmt_block = tree.children[2]
        else:
            func_type = tree.children[0].children[0].value
            stmt_block = tree.children[3]
        if hasattr(stmt_block, 'function_return_symbolObject'):
            tree.function_return_symbolObject = stmt_block.function_return_symbolObject
            if func_type != tree.function_return_symbolObject.type:
                raise SemanticError("Invalid return type")

    def stmt_block(self,tree):
        self.visit_children(tree)
        for child in tree.children:
            if hasattr(child, 'function_return_symbolObject'):
                tree.function_return_symbolObject = child.function_return_symbolObject

    def stmt(self,tree):
        self.visit_children(tree)
        child = tree.children[0]
        if child.data == 'returnstmt':
            tree.function_return_symbolObject = child.meta_symbolObject

    def returnstmt(self,tree):
        self.visit_children(tree)
        tree.meta_symbolObject = tree.children[0].meta_symbolObject


    def expr(self, tree):
        self.visit_children(tree)
        tree.meta_symbolObject = tree.children[0].meta_symbolObject

    def exprprio8(self, tree):
        self.visit_children(tree)
        tree.meta_symbolObject = tree.children[0].meta_symbolObject


    def exprprio1(self, tree):
        self.visit_children(tree)
        tree.meta_symbolObject = tree.children[0].meta_symbolObject

    def exprprio2(self, tree):
        self.visit_children(tree)
        tree.meta_symbolObject = tree.children[0].meta_symbolObject


    def exprprio3(self, tree):
        self.visit_children(tree)
        tree.meta_symbolObject = tree.children[0].meta_symbolObject

    def exprprio4(self, tree):
        self.visit_children(tree)
        tree.meta_symbolObject = tree.children[0].meta_symbolObject


    def exprprio5(self, tree):
        self.visit_children(tree)
        tree.meta_symbolObject = tree.children[0].meta_symbolObject


    def exprprio6(self, tree):
        self.visit_children(tree)
        tree.meta_symbolObject = tree.children[0].meta_symbolObject


    def exprprio7(self, tree):
        self.visit_children(tree)
        tree.meta_symbolObject = tree.children[0].meta_symbolObject

    def add(self, tree):
        self.__check_operators_type(tree)

    def sub(self, tree):
        self.__check_operators_type(tree)

    def mult(self, tree):
        self.__check_operators_type(tree)

    def divide(self, tree):
        self.__check_operators_type(tree)

    def or_expr(self, tree):
        self.__check_operators_type(tree)

    def and_expr(self, tree):
        self.__check_operators_type(tree)

    def equal_expr(self, tree):
        self.__check_operators_type(tree)

    def not_equal_expr(self, tree):
        self.__check_operators_type(tree)

    def lt_expr(self, tree):
        self.__check_operators_type(tree)

    def gt_expr(self, tree):
        self.__check_operators_type(tree)

    def lte_expr(self, tree):
        self.__check_operators_type(tree)

    def gte_expr(self, tree):
        self.__check_operators_type(tree)

    def gte_expr(self, tree):
        self.__check_operators_type(tree)

    def gte_expr(self, tree):
        self.__check_operators_type(tree)
        
    def __check_operators_type(self, tree):
        assert len(tree.children) == 2
        if tree.children[0].meta_symbolObject.type != tree.children[1].meta_symbolObject.type:
            raise SemanticError("Invalid type for operation")

    def global_func_call(self, tree):
        func_name = tree.meta_symbolObject.name
        tree.meta_symbolObject = global_functions[func_name]
        for actual, formal in zip(tree.symbolObjects, function_name_to_arguments[func_name]):
            if actual.type != formal.type:
                raise SemanticError("Invalid type for function call formals")
    
    def access_array(self, tree):
        if tree.index_symbolObject.type != 'int':
            raise SemanticError("Invalid access array index type")
