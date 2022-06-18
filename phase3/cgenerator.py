from lark import Lark, Tree
from lark.visitors import Interpreter
from lib.lib import add_readInteger, add_print, add_itod, add_dtoi, add_readLine, add_string_concat, add_itob, add_new_array, add_access_array, add_strcmp, add_array_cp
from larkparser import grammar
from symbolTableCreator import SymbolTableCreator, SymbolTableObject, global_functions
from semantic_checker import SemanticChecker, SemanticError
from utils import write_results, read_input_file


class cgenerator(Interpreter):
    def __init__(self):
        self.bool_eval_branch_label_count = 0
        self.if_lbl_cnt = 0
        self.loop_lbl_cnt = 0
        self.str_lbl_cnt = 0

    def start(self, tree):
        code = ".text\nj main\n"
        code += ''.join(self.visit_children(tree))
        code += add_readInteger()
        code += add_print()
        code += add_itod()
        code += add_dtoi()
        code += add_readLine()
        code += add_string_concat()
        code += add_itob()
        code += add_new_array()
        code += add_access_array()
        code += add_strcmp()
        code += add_array_cp()
        return code

    def decl(self, tree):
        code = ""
        for declaration in tree.children:
            if declaration.data in ("variable_decl", "function_decl"):
                code += self.visit(declaration)
        return code

    def function_decl(self, tree):
        code = ""
        isvoid = len(tree.children) == 3
        stmt_block, formals = None, None
        if (isvoid):
            stmt_block = tree.children[2]
            formals = tree.children[1]
        else:
            stmt_block = tree.children[3]
            formals = tree.children[2]
        code += ".text\n"
        code += tree.symbolObject.label + ":\n"
        if tree.symbolObject.name == "main":
            code += "main:\n"
        code += self.visit(formals)
        local_vars_size = tree.local_vars_size
        formal_vars_size = tree.formal_vars_size
        stack_size = local_vars_size + 16
        code += ".text\n"
        code += self.increase_stack_size(stack_size)
        code += f"   sw $ra,{local_vars_size + 8}($sp)\n"
        code += f"   sw $fp,{local_vars_size}($sp)\n"
        code += f"   addu $fp,$sp,{local_vars_size - 8}\n"
        code += self.visit(stmt_block)
        code += f"   lw $ra,{local_vars_size + 8}($sp)\n"
        code += f"   lw $fp,{local_vars_size}($sp)\n"
        code += self.decrease_stack_size(stack_size)
        if tree.symbolObject.name == "main":
            code += "   li $v0,10\n"
            code += "   syscall\n"
        else:
            code += "   jr $ra\n"
        return code

    def formals(self, tree):
        code = ""
        return code

    def variable_decl(self, tree):
        code = ""
        variable = tree.children[0]
        code += self.visit(variable)
        return code

    def variable(self, tree):
        code = ""
        return code

    def stmt_block(self, tree):
        code = ""
        variable_decls = filter(lambda x: x.data == "variable_decl", tree.children)
        stmts = filter(lambda x: x.data == "stmt", tree.children)
        code += '.data\n'
        code += '.align 2\n'
        for variable_decl in variable_decls:
            code += self.visit(variable_decl)
        code += '.text\n'
        for stmt in stmts:
            code += self.visit(stmt)
        return code

    def stmt(self, tree):
        code = ""
        for child in tree.children:
            code += self.visit(child)
        return code


    def returnstmt(self, tree):
        code = ""
        if (len(tree.children) == 0):
            return code
        expr = tree.children[0]
        code += self.visit(expr)
        symbolObject = expr.meta_symbolObject
        if symbolObject.type == "double":
            code += "   l.d $f0, 0($sp)\n"
            code += "   add $sp, $sp, 8\n"
        else:
            code += "   lw $v0, 0($sp)\n"
            code += "   add $sp, $sp, 8\n"
        return code

    def ident_lvalue(self, tree):
        code = "#ident_lavalue\n.text\n"
        symbolObject = tree.meta_symbolObject
        code += f"   lw $t0, {symbolObject.frameOffset}($fp)\n"
        code += "   sub $sp, $sp, 8\n"
        code += "   sw $t0, 0($sp)\n"
        return code

    def expr(self, tree):
        code = "".join(self.visit_children(tree))
        tree.meta_symbolObject = tree.children[0].meta_symbolObject
        return code

    def exprprio8(self, tree):
        code = "".join(self.visit_children(tree))
        tree.meta_symbolObject = tree.children[0].meta_symbolObject
        return code

    def exprprio1(self, tree):
        code = "".join(self.visit_children(tree))
        tree.meta_symbolObject = tree.children[0].meta_symbolObject
        return code

    def exprprio2(self, tree):
        code = "".join(self.visit_children(tree))
        tree.meta_symbolObject = tree.children[0].meta_symbolObject
        return code

    def exprprio3(self, tree):
        code = "".join(self.visit_children(tree))
        tree.meta_symbolObject = tree.children[0].meta_symbolObject
        return code

    def exprprio4(self, tree):
        code = "".join(self.visit_children(tree))
        tree.meta_symbolObject = tree.children[0].meta_symbolObject
        return code

    def exprprio5(self, tree):
        code = "".join(self.visit_children(tree))
        tree.meta_symbolObject = tree.children[0].meta_symbolObject
        return code

    def exprprio6(self, tree):
        code = "".join(self.visit_children(tree))
        tree.meta_symbolObject = tree.children[0].meta_symbolObject
        return code

    def exprprio7(self, tree):
        code = "".join(self.visit_children(tree))
        tree.meta_symbolObject = tree.children[0].meta_symbolObject
        return code

    def ifstmt(self, tree):
        code = ""
        if_label = self.if_lbl_cnt
        self.if_lbl_cnt += 1
        code += self.visit(tree.children[0])
        code += f"""
            .text
                lw $a0, 0($sp)
                addi $sp, $sp, 8
                beq $a0, 0, start_else_{if_label}
            """
        code += self.visit(tree.children[1])
        code += f"j end_if_{if_label}\n"
        code += f"start_else_{if_label}:\n"
        code += "" if len(tree.children) == 2 else self.visit(tree.children[2])
        code += f"end_if_{if_label}:\n"
        return code


    def access_array_length(self,tree):
        code = ".text\n"
        code += self.visit(tree.children[0])
        code += "   lw $t0 ,0($sp)\n"
        code += "   lw $t1,-8($t0)\n"
        code += "   sw $t1, 0($sp)\n"
        return code

    def whilestmt(self, tree):
        code = ""
        label = self.loop_lbl_cnt
        self.loop_lbl_cnt += 1
        code += f"start_loop_{label}:\n"
        code += self.visit(tree.children[0])
        code += f"""
                    lw $a0, 0($sp)
                    addi $sp, $sp, 8
                    beq $a0, 0, end_loop_{label}
                """
        code += self.visit(tree.children[1])
        code += f"j start_loop_{label}\n"
        code += f"end_loop_{label}:\n"
        return code

    def forstmt(self, tree):
        code = ""
        increment = ""
        evaluate = ""
        initiate = ""
        if tree.children[0].data == "assignment":
            initiate += self.visit(tree.children[0])
            evaluate += self.visit(tree.children[1])
        else:
            evaluate += self.visit(tree.children[0])
        if tree.children[-2].data == "assignment":
            increment += self.visit(tree.children[-2])
        label = self.loop_lbl_cnt
        self.loop_lbl_cnt += 1
        code += initiate
        code += f"start_loop_{label}:\n"
        code += evaluate
        code += f"""
            lw $a0, 0($sp)
            addi $sp, $sp, 8
            beq $a0, 0, end_loop_{label}
            """
        code += self.visit(tree.children[-1])
        code += increment
        code += f"j start_loop_{label}\n"
        code += f"end_loop_{label}:\n"
        return code
    
    def breakstmt(self, tree):
        label = self.loop_lbl_cnt - 1
        return f"j end_loop_{label}\n"

    def printstmt(self, tree):
        code = ""
        for expr in tree.children:
            code += self.visit(expr)
            code += self.__print_expr(expr.meta_symbolObject)
        code += "   jal print_newline_char\n"
        return code


    def __print_expr(self, symbolObject):
        code = ""
        if symbolObject.type == "int":
            code += "   jal lib_print_int\n"
        elif (symbolObject.type == "double"):
            code += "   jal lib_print_double\n"
        elif symbolObject.type == "string":
            code += "   jal lib_print_string\n"
        elif symbolObject.type == "bool":
            code += "   jal lib_print_bool\n"
        return code

    def constant(self, tree):
        code = ''
        symbolObject = tree.meta_symbolObject
        if (symbolObject.type == 'double'):
            dval = symbolObject.value
            if dval[-1] == '.':
                dval += '0'
            if '.e' in dval:
                index = dval.find('.e') + 1
                dval = dval[:index] + '0' + dval[index:]
            code += '.text\n'
            code += '   li.d $f0, {}\n'.format(dval)
            code += '   sub $sp, $sp, 8\n'
            code += '   s.d $f0, 0($sp)\n\n'
        elif (symbolObject.type == 'int' or symbolObject.type == 'bool'):
            code += '.text\n'
            code += f"   li $t0, {symbolObject.value}\n"
            code += "   sub $sp, $sp, 8\n"
            code += "   sw $t0, 0($sp)\n"
        elif (symbolObject.type == "string"):
            code += ".data\n"
            code += f"   {symbolObject.label}: .asciiz {symbolObject.value}\n"
            code += ".text\n"
            code += f"   la $t0,{symbolObject.label}\n"
            code += "   sub $sp, $sp, 8\n"
            code += "   sw $t0, 0($sp)\n"

        return code

    def read_integer_func(self, tree):
        code = ""
        code += "   jal lib_ReadInteger\n"
        return code

    def read_line_func(self, tree):
        code = "\tjal lib_ReadLine\n"
        return code

    def read_integer(self, tree):
        return ""

    def itod_func(self, tree):
        code = ""
        code += "".join(self.visit_children(tree))
        code += "   jal lib_itod\n"
        return code

    def dtoi_func(self, tree):
        code = ""
        code += "".join(self.visit_children(tree))
        code += "   jal lib_dtoi\n"
        return code

    def itob_func(self, tree):
        code = ""
        code += "".join(self.visit_children(tree))
        code += "   jal lib_itob\n"
        return code

    def btoi_func(self, tree):
        code = ""
        code += "".join(self.visit_children(tree))
        return code

    def assignment(self, tree):
        code = ""
        symbolObject = tree.meta_symbolObject
        code += self.visit(tree.children[1])
        code += '.text\n'
        if(symbolObject.is_access_array):
            code += self.visit(tree.children[0].children[1])
            code += "   lw $t0,0($sp)\n"
            code += "   add $sp, $sp, 8\n"
            code += "   sll $t0,$t0,3\n"
            code += f"  lw $t1,{symbolObject.frameOffset}($fp)\n"
            code += "   add $t1,$t1,$t0\n"
            if tree.children[1].meta_symbolObject.type == "double":
                code += "   l.d $f0, 0($sp)\n"
                code += "   add $sp, $sp, 8\n"
                code += f"   s.d $f0, 0($t1)\n"
            else:
                code += "   lw $t0, 0($sp)\n"
                code += "   add $sp, $sp, 8\n"
                code += f"   sw $t0, 0($t1)\n"
        else:
            if symbolObject.type == "double":
                code += "   l.d $f0, 0($sp)\n"
                code += "   add $sp, $sp, 8\n"
                code += f"   s.d $f0, {symbolObject.frameOffset}($fp)\n"
            else:
                code += "   lw $t0, 0($sp)\n"
                code += "   add $sp, $sp, 8\n"
                code += f"   sw $t0, {symbolObject.frameOffset}($fp)\n"
        return code

    def negate(self, tree):
        code = ".text\n"
        code += self.visit(tree.children[0])
        if(tree.meta_symbolObject.type == "double"):
            code += '   l.d $f0, 0($sp)\n'
            code += '   neg.d $f1,$f0\n'
            code += '   s.d $f1, 0($sp)\n'
        else:
            code += '   lw $t0, 0($sp)\n'
            code += '   neg $t1,$t0\n'
            code += '   sw $t1,0($sp)\n'
        return code


    def add(self, tree):
        code = ""
        childType = tree.children[0].meta_symbolObject.type
        code += "".join(self.visit_children(tree))
        code += '.text\n'
        if childType == "double" :
            code += '   l.d $f0, 0($sp)\n'
            code += '   l.d $f2, 8($sp)\n'
            code += '   add.d $f4, $f2, $f0\n'
            code += '   s.d $f4, 8($sp)\n'
            code += '   addi $sp, $sp, 8\n\n'
        elif childType == "int":
            code += '   lw $t0, 0($sp)\n'
            code += '   lw $t1, 8($sp)\n'
            code += '   add $t2, $t1, $t0\n'
            code += '   sw $t2, 8($sp)\n'
            code += '   addi $sp, $sp, 8\n'
        elif childType == "string":
            label = self.str_lbl_cnt
            self.str_lbl_cnt += 1
            code += f"""
                .data
                str_{label}:
                .space 200
            """
            code += f"""
                .text
                lw $a0, 8($sp)
                la $a1, str_{label}
                jal lib_strcopier
                lw $a0, 0($sp)
                or $a1, $v0, $zero
                jal lib_strcopier
                la $t0, str_{label}
                sw $t0, 8($sp)
                addi $sp, $sp, 8
            """
        elif childType == "array_double":
            code += """
                .text
                jal lib_array_cp_double
            """
        elif "array" in childType:
            code += """
                .text
                jal lib_array_cp
            """
        return code

    def sub(self, tree):
        code = ""
        childType = tree.children[0].meta_symbolObject.type
        code += "".join(self.visit_children(tree))
        code += '.text\n'
        if childType == "double" :
            code += '   l.d $f0, 0($sp)\n'
            code += '   l.d $f2, 8($sp)\n'
            code += '   sub.d $f4, $f2, $f0\n'
            code += '   s.d $f4, 8($sp)\n'
            code += '   addi $sp, $sp, 8\n\n'
        else:
            code += '   lw $t0, 0($sp)\n'
            code += '   lw $t1, 8($sp)\n'
            code += '   sub $t2, $t1, $t0\n'
            code += '   sw $t2, 8($sp)\n'
            code += '   addi $sp, $sp, 8\n'
        return code

    def mult(self, tree):
        code = ""
        childType = tree.children[0].meta_symbolObject.type
        code += "".join(self.visit_children(tree))
        code += '.text\n'
        if childType == "double" :
            code += '   l.d $f0, 0($sp)\n'
            code += '   l.d $f2, 8($sp)\n'
            code += '   mul.d $f4, $f2, $f0\n'
            code += '   s.d $f4, 8($sp)\n'
            code += '   addi $sp, $sp, 8\n\n'
        else:
            code += '   lw $t0, 0($sp)\n'
            code += '   lw $t1, 8($sp)\n'
            code += '   mul $t2, $t1, $t0\n'
            code += '   sw $t2, 8($sp)\n'
            code += '   addi $sp, $sp, 8\n'
        return code

    def divide(self, tree):
        code = ""
        childType = tree.children[0].meta_symbolObject.type
        code += "".join(self.visit_children(tree))
        code += '.text\n'
        if childType == "double":
            code += '   l.d $f0, 0($sp)\n'
            code += '   l.d $f2, 8($sp)\n'
            code += '   div.d $f4, $f2, $f0\n'
            code += '   s.d $f4, 8($sp)\n'
            code += '   addi $sp, $sp, 8\n\n'
        else:
            code += '   lw $t0, 0($sp)\n'
            code += '   lw $t1, 8($sp)\n'
            code += '   div $t2, $t1, $t0\n'
            code += '   sw $t2, 8($sp)\n'
            code += '   addi $sp, $sp, 8\n'
        return code

    def or_expr(self, tree):
        code = ""
        code += "".join(self.visit_children(tree))
        code += '.text\n'
        code += '   lw $t0, 0($sp)\n'
        code += '   lw $t1, 8($sp)\n'
        code += '   or $t2, $t1, $t0\n'
        code += '   sw $t2, 8($sp)\n'
        code += '   addi $sp, $sp, 8\n'
        return code

    def and_expr(self, tree):
        code = ""
        code += "".join(self.visit_children(tree))
        code += '.text\n'
        code += '   lw $t0, 0($sp)\n'
        code += '   lw $t1, 8($sp)\n'
        code += '   and $t2, $t1, $t0\n'
        code += '   sw $t2, 8($sp)\n'
        code += '   addi $sp, $sp, 8\n'
        return code


    def equal_expr(self, tree):
        childType = tree.children[0].meta_symbolObject.type
        if childType == "string":
            code = "".join(self.visit_children(tree))
            code += """
            .text
                jal lib_strcmp    
            """
        else:
            code = f"""
{self.sub(tree)}
.text
    lw $t0, 0($sp)
    li $t1, 1
    beqz $t0,bool_expr_eval_true_{self.bool_eval_branch_label_count}
    li $t1, 0
    bool_expr_eval_true_{self.bool_eval_branch_label_count}:
    sw $t1, 0($sp)
            """
        self.bool_eval_branch_label_count +=1
        return code



    def not_equal_expr(self, tree):
        childType = tree.children[0].meta_symbolObject.type
        if childType == "string":
            code = "".join(self.visit_children(tree))
            code += """
            .text
                jal lib_strcmp
                lw $t0, 0($sp)
                li $t1, 1
                xor $t0, $t0, $t1
                sw $t0, 0($sp)  
            """
        else:
            code = ""
            code += self.sub(tree)
            code += '.text\n'
            code += '   lw $t0, 0($sp)\n'
            code += '   li $t1, 1\n'
            code += f'   bnez $t0,bool_expr_eval_true_{self.bool_eval_branch_label_count}\n'
            code += '   li $t1, 0\n'
            code += f'   bool_expr_eval_true_{self.bool_eval_branch_label_count}:\n'
            code += '   sw $t1, 0($sp)\n'
            self.bool_eval_branch_label_count +=1
        return code


    def lt_expr(self, tree):
        code = ""
        code += self.sub(tree)
        code += '.text\n'
        code += '   lw $t0, 0($sp)\n'
        code += '   li $t1, 1\n'
        code += f'   bltz $t0,bool_expr_eval_true_{self.bool_eval_branch_label_count}\n'
        code += '   li $t1, 0\n'
        code += f'   bool_expr_eval_true_{self.bool_eval_branch_label_count}:\n'
        code += '   sw $t1, 0($sp)\n'
        self.bool_eval_branch_label_count +=1
        return code

    def gt_expr(self, tree):
        code = ""
        code += self.sub(tree)
        code += '.text\n'
        code += '   lw $t0, 0($sp)\n'
        code += '   li $t1, 1\n'
        code += f'   bgtz $t0,bool_expr_eval_true_{self.bool_eval_branch_label_count}\n'
        code += '   li $t1, 0\n'
        code += f'   bool_expr_eval_true_{self.bool_eval_branch_label_count}:\n'
        code += '   sw $t1, 0($sp)\n'
        self.bool_eval_branch_label_count +=1
        return code


    def lte_expr(self, tree):
        code = ""
        code += self.sub(tree)
        code += '.text\n'
        code += '   lw $t0, 0($sp)\n'
        code += '   li $t1, 1\n'
        code += f'   blez $t0,bool_expr_eval_true_{self.bool_eval_branch_label_count}\n'
        code += '   li $t1, 0\n'
        code += f'   bool_expr_eval_true_{self.bool_eval_branch_label_count}:\n'
        code += '   sw $t1, 0($sp)\n'
        self.bool_eval_branch_label_count +=1
        return code


    def gte_expr(self, tree):
        code = ""
        code += self.sub(tree)
        code += '.text\n'
        code += '   lw $t0, 0($sp)\n'
        code += '   li $t1, 1\n'
        code += f'   bgez $t0,bool_expr_eval_true_{self.bool_eval_branch_label_count}\n'
        code += '   li $t1, 0\n'
        code += f'   bool_expr_eval_true_{self.bool_eval_branch_label_count}:\n'
        code += '   sw $t1, 0($sp)\n'
        self.bool_eval_branch_label_count +=1
        return code

    def not_expr(self,tree):
        code = ".text\n"
        code += self.visit(tree.children[0])
        code += '   lw $t0, 0($sp)\n'
        code += '   li $t1,1\n'
        code += f'   beqz $t0,bool_expr_eval_true_{self.bool_eval_branch_label_count}\n'
        code += '    li $t1,0\n'
        code += f'   bool_expr_eval_true_{self.bool_eval_branch_label_count}:\n'
        code += '   sw $t1, 0($sp)\n'
        return code

    def global_func_call(self, tree):
        code = ""
        tree.meta_symbolObject = global_functions[tree.meta_symbolObject.name]
        funcSymbolObject: SymbolTableObject = tree.meta_symbolObject
        funcDeclTree:Tree = funcSymbolObject.base_tree
        code += self.visit(tree.children[1])
        code += f"  jal {funcSymbolObject.label}\n"
        code += self.decrease_stack_size(funcDeclTree.formal_vars_size)
        if funcSymbolObject.type == "double":
            code += "   sub $sp, $sp, 8\n"
            code += "   s.d $f0, 0($sp)\n"
        else:
            code += "   sub $sp, $sp, 8\n"
            code += "   sw $v0, 0($sp)\n"
        return code

    def actuals(self,tree):
        code = "#push arguments\n"
        for expr in reversed(tree.children):
            code += self.visit(expr)
        return code

    def new_array(self, tree):
        code = ""
        code += "".join(self.visit_children(tree))
        code += """
                .text
                jal lib_new_array
                """
        return code

    def type(self,tree):
        return ""

    def array_type(self,tree):
        return ""

    def access_array(self, tree):
        childType = tree.children[0].meta_symbolObject.type
        code = ""
        code += "".join(self.visit_children(tree))
        if childType == "array_double":
            code += """
                .text
                jal lib_access_array_double
                """
        else:
            code += """
                .text
                jal lib_access_array
                """
        return code

    def expr_in_parentheses(self, tree):
        return "".join(self.visit(tree.children[0]))

    def increase_stack_size(self, size):
        if (size % 4 != 0):
            raise Exception("size should be multiple of 4")
        if (size % 8 != 0):
            size += 4
        code = ""
        code += f"   subu $sp,$sp,{size}\n"
        return code

    def decrease_stack_size(self, size):
        if (size % 4 != 0):
            raise Exception("size should be multiple of 4\n")
        if (size % 8 != 0):
            size += 4
        code = ""
        code += f"   addu $sp,$sp,{size}\n"
        return code


def generate_code(decaf_code):
    parser = Lark(grammar, parser="lalr")
    parse_tree = parser.parse(decaf_code)
    #print(parse_tree.pretty())
    try:
        SymbolTableCreator().visit(parse_tree)
        SemanticChecker().visit(parse_tree)
        code = cgenerator().visit(parse_tree)
    except SemanticError:
        code = """
.text
    .globl main

main:
    la $a0 , errorMsg
    addi $v0 , $zero, 4
    syscall
    jr $ra

.data
    errorMsg: .asciiz "Semantic Error"
        """
    # print(parse_tree.pretty())
    return code


if __name__ == "__main__":
    text = read_input_file("preTests/test1.in")
    code = generate_code(text)
    write_results("preTests/test1.s", code)
