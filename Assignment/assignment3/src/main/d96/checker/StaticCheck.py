"""
 * @author nhphung
"""
from AST import *
from Visitor import *
from StaticError import *

class MType:
    def __init__(self, partype, rettype):
        self.partype = partype
        self.rettype = rettype


class Symbol:
    def __init__(self, name, mtype, value=None):
        self.name = name
        self.mtype = mtype
        self.value = value


class ExpUtils:
    @staticmethod
    def isNotConstOperand(exprType):
        return type(exprType) in [NewExpr, ArrayCell]

    @staticmethod
    def isNotIntFloatType(exprType):
        return type(exprType) not in [IntType, FloatType]

    @staticmethod
    def isNotIntBoolType(exprType):
        return type(exprType) not in [IntType, BoolType]

    @staticmethod
    def isNotAccess(exprType):
        return type(exprType) not in [CallExpr, FieldAccess, CallStmt]


class StaticChecker(BaseVisitor):

    global_envi = [
        Symbol("getInt", MType([], IntType())),
        Symbol("putIntLn", MType([IntType()], VoidType())),
    ]

    def __init__(self, ast):
        self.ast = ast
        self.global_env = {}
        self.scope = 0
        # Stack for storing parent class of each class
        self.parent = []

    def check(self):
        return self.visit(self.ast, StaticChecker.global_envi)

    def visitProgram(self, ast, c):
        # decl: List[ClassDecl]
        c = self.global_env
        flag = False
        for x in ast.decl:
            if x.classname.name == "Program":
                for y in x.memlist:
                    if type(y) is MethodDecl:
                        if y.name.name == "main":
                            flag = True
            self.visit(x, c)
        if flag == False:
            raise NoEntryPoint()

    def visitClassDecl(self, ast: ClassDecl, c):
        """
        classname: Id
        memlist: List[MemDecl]
        parentname: Id = None
        """
        class_name = ast.classname.name
        if c.get(class_name) is not None:
            raise Redeclared(Class(), class_name)
        if ast.parentname is not None:
            parent_name = ast.parentname.name
            if c.get(parent_name) is None:
                raise Undeclared(Class(), parent_name)
            self.parent += [parent_name]
        else:
            self.parent += [None]
        c[class_name] = {}
        for x in ast.memlist:
            self.visit(x, (c[class_name], c))

    def visitAttributeDecl(self, ast: AttributeDecl, c):
        """
        kind: SIKind  # Instance or Static
        decl: StoreDecl  # VarDecl for mutable or ConstDecl for immutable
        """
        # Type of c: (c[class_name], c)
        (inner_dict, outer_dict) = c
        if type(ast.kind) is Instance:
            self.visit(ast.decl, ("instance", False, [], inner_dict, outer_dict))
        if type(ast.kind) is Static:
            self.visit(ast.decl, ("static", False, [], inner_dict, outer_dict))

    def visitVarDecl(self, ast: VarDecl, c):
        """
        variable: Id
        varType: Type
        varInit: Expr = None  # None if there is no initial
        """
        (kind, inBlock, symbol_stack, inner_env, outer_env) = c  # kind = 'instance' & inner_env = inner_dict (c[class_name] = {})
        var_name = ast.variable.name
        if inBlock == False:
            if inner_env.get(var_name) is not None:
                raise Redeclared(Attribute(), var_name)
        var_type = self.visit(ast.varType, outer_env)

        if (ast.varInit is not None) and not(type(ast.varInit) is NullLiteral):
            value = self.visit(ast.varInit, (symbol_stack, inner_env, outer_env, False))
            # Check if value is a variable -> Var a: Int = Self.b;
            if value[0] in ["instance", "static"]:
                if ExpUtils.isNotAccess(ast.varInit):
                    raise Undeclared(Identifier(), ast.varInit.name)
            
            # If we have an array declaration -> Var a: Array[Int, 3] = Array(1, 2, 3);
            # print("value[2]: " + str(value[2]) + "\n")
            # print("var_type: " + str(type(var_type)) + "\n")
            if type(var_type) is ArrayType and type(value[2]) is ArrayType:
                if var_type.size != value[2].size:
                    raise TypeMismatchInStatement(ast)
                var_ele_type = var_type.eleType
                value_ele_type = value[2].eleType
                # print("var_ele_type: " + str(type(var_ele_type)) + "\n")
                # print("value_ele_type: " + str(type(value_ele_type)) + "\n")
                if not(type(var_ele_type) is type(value_ele_type)):
                    # Check array element type coercion --> Case: Float / Int
                    if not(type(var_ele_type) is FloatType and type(value_ele_type) is IntType):
                        raise TypeMismatchInStatement(ast)
            
            # Else: Check if value is a primitive type
            # print("value[2]: " + str(type(value[2])) + "\n") # --> NullLiteral
            # print("var_type: " + str(type(var_type)) + "\n") # --> ClassType
            if not(type(value[2]) is type(var_type)):
                if not(type(var_type) is FloatType and type(value[2]) is IntType):
                    raise TypeMismatchInStatement(ast)

        # c[class_name][var_name] = ('mutable', var_type, kind)
        if inBlock == False:
            inner_env[var_name] = (kind, "mutable", var_type)

    def visitConstDecl(self, ast: ConstDecl, c):
        """
        constant: Id
        constType: Type
        value: Expr = None # None if there is no initial
        """
        (kind, inBlock, symbol_stack, inner_env, outer_env) = c
        const_name = ast.constant.name
        if inBlock == False:
            if inner_env.get(const_name) is not None:
                raise Redeclared(Attribute(), const_name)
        # Val a: Int = a[1] / New A(); --> Illegal Constant Expr
        if ast.value is None or ExpUtils.isNotConstOperand(ast.value):
            raise IllegalConstantExpression(ast.value)

        value = self.visit(ast.value, (symbol_stack, inner_env, outer_env, True))
        # Check if value is a variable --> Val a: Int = Self.b;
        if value[0] in ["instance", "static"]:
            if ExpUtils.isNotAccess(ast.value):
                raise Undeclared(Identifier(), ast.value.name)
        if value[1] == "mutable":
            raise IllegalConstantExpression(ast.value)

        const_type = self.visit(ast.constType, outer_env)
        # If we have a constant array declaration --> Val a: Array[Int, 3] = Array(1, 2, 3);
        if type(const_type) is ArrayType and type(value[2]) is ArrayType:
            if const_type.size != value[2].size:
                raise TypeMismatchInConstant(ast)
            const_ele_type = const_type.eleType
            value_ele_type = value[2].eleType
            if not(type(const_ele_type) is type(value_ele_type)):
                # Check array element type coercion
                if not(type(const_ele_type) is FloatType and type(value_ele_type) is IntType):
                    raise TypeMismatchInConstant(ast)

        # Else: other primitive type declaration
        # print("value[2]: " + str(type(value[2])) + "\n")
        # print("const_type: " + str(type(const_type)) + "\n")
        if not(type(value[2]) is type(const_type)):
            # Check primitive type coercion
            if not(type(const_type) is FloatType and type(value[2]) is IntType):
                raise TypeMismatchInConstant(ast)

        if inBlock == False:
            inner_env[const_name] = (kind, "immutable", const_type)

    def visitMethodDecl(self, ast: MethodDecl, c):
        """
        kind: SIKind
        name: Id
        param: List[VarDecl]
        body: Block
        """
        (inner_env, outer_env) = c
        if type(ast.kind) is Instance:
            kind = "instance"
        if type(ast.kind) is Static:
            kind = "static"
        method_name = ast.name.name
        if inner_env.get(method_name) is not None:
            raise Redeclared(Method(), method_name)

        symbol_stack = []  # Structure: [(name, 'immutable', rettype)]
        scope_stack = [] # Keep the scope
        paramTypeLst = []
        for x in ast.param:
            var_name = x.variable.name
            var_type = x.varType
            for y in symbol_stack:
                # y = (name, 'immutable', rettype)
                if y[0] == var_name:
                    raise Redeclared(Parameter(), var_name)
            symbol_stack += [(var_name, "mutable", var_type)]
            paramTypeLst += [var_type]
        
        inner_env[method_name] = [kind, "method", None, paramTypeLst]
        self.visit(ast.body, (symbol_stack, scope_stack, False, inner_env, outer_env))

    def visitBlock(self, ast: Block, c):
        # inst: List[Inst]
        (symbol_stack, scope_stack, inLoop, inner_env, outer_env) = c
        scope_stack.append(self.scope)
        for x in ast.inst:
            # VarDecl in block
            if type(x) is VarDecl:
                var_name = x.variable.name
                var_type = self.visit(x.varType, outer_env)
                for y in symbol_stack[scope_stack[-1]:]:
                    if y[0] == var_name:
                        raise Redeclared(Variable(), var_name)
                self.visit(x, ("instance", True, symbol_stack, inner_env, outer_env))
                symbol_stack += [(var_name, "mutable", var_type)]
            # ConstDecl in block
            elif type(x) is ConstDecl:
                const_name = x.constant.name
                const_type = self.visit(x.constType, outer_env)
                for y in symbol_stack[scope_stack[-1]:]:
                    if y[0] == const_name:
                        raise Redeclared(Constant(), const_name)
                self.visit(x, ("instance", True, symbol_stack, inner_env, outer_env))
                symbol_stack += [(const_name, "immutable", const_type)]
            # Others: Stmt
            else:
                if type(x) is Block:
                    self.scope += len(symbol_stack)
                    self.visit(x, (symbol_stack, scope_stack, inLoop, inner_env, outer_env))
                else:
                    self.visit(x, (symbol_stack, inLoop, inner_env, outer_env, False))
        # Finish checking the block
        symbol_stack = symbol_stack[:scope_stack[-1]]
        scope_stack.pop()

    def visitId(self, ast: Id, c):
        # name: str
        (symbol_stack, inner_env, outer_env, const_decl_flag) = c
        for x in symbol_stack:
            if x[0] == ast.name:
                return x # (name, mutability, rettype)
        if inner_env.get(ast.name) is not None:
            return inner_env[ast.name] # (kind, mutability, rettype) / (kind, mutability, rettype, paramTypeLst)
        raise Undeclared(Identifier(), ast.name)

    def visitAssign(self, ast, c):
        """
        lhs: Expr
        exp: Expr
        """
        (symbol_stack, inLoop, inner_env, outer_env, const_decl_flag) = c
        lhs = self.visit(ast.lhs, (symbol_stack, inner_env, outer_env, const_decl_flag))
        expr = self.visit(ast.exp, (symbol_stack, inner_env, outer_env, const_decl_flag))

        if lhs[0] in ["instance", "static"]: # Attribute
            if ExpUtils.isNotAccess(ast.lhs):
                raise Undeclared(Identifier(), ast.lhs.name)
            if lhs[1] == "immutable":
                raise CannotAssignToConstant(ast)
        else: # VarDecl/ConstDecl inside Block
            if lhs[1] == "immutable":
                raise CannotAssignToConstant(ast)

        if expr[0] in ["instance", "static"]: # RHS is Attribute
            if ExpUtils.isNotAccess(ast.exp):
                raise Undeclared(Identifier(), ast.exp.name)

        lhs_type = lhs[2]
        expr_type = expr[2]
        if type(lhs_type) is VoidType:
            raise TypeMismatchInStatement(ast)

        if type(lhs_type) is ArrayType and type(expr_type) is ArrayType:
            if lhs_type.size != expr_type.size:
                raise TypeMismatchInStatement(ast)
            lhs_eleType = lhs_type.eleType
            expr_eleType = expr_type.eleType
            # Check array element type coercion
            if not(type(lhs_eleType) is type(expr_eleType)):
                if not(type(lhs_eleType) is FloatType and type(expr_eleType) is IntType):
                    raise TypeMismatchInStatement(ast)

        # print("lhs_type: " + str(type(lhs_type)) + "\n")
        # print("expr_type: " + str(type(expr_type)) + "\n")
        if not(type(lhs_type) is type(expr_type)):
            # Check primitive type coercion
            if type(lhs_type) is ArrayType:
                lhs_eleType = lhs_type.eleType
                if not(type(lhs_eleType) is type(expr_type)):
                    # print("lhs_eleType: " + str(type(lhs_eleType)))
                    # print("expr_type: " + str(type(expr_type)))
                    if not(type(lhs_eleType) is FloatType and type(expr_type) is IntType):
                        raise TypeMismatchInStatement(ast)
            
            elif not(type(lhs_type) is FloatType and expr_type is IntType):
                # print("lhs_type2: " + str(type(lhs_type)))
                # print("expr_type2: " + str(expr_type))
                raise TypeMismatchInStatement(ast)
            
    def visitIf(self, ast: If, c):
        """
        expr: Expr
        thenStmt: Stmt
        elseStmt: Stmt = None  # None if there is no else branch
        """
        (symbol_stack, inLoop, inner_env, outer_env, const_decl_flag) = c
        if_expr = self.visit(ast.expr, (symbol_stack, inner_env, outer_env, const_decl_flag))
        # If if_Expr is an Attribute, it needs CallExpr 
        if if_expr[0] in ["instance", "static"]:
            if ExpUtils.isNotAccess(ast.expr):
                raise Undeclared(Identifier(), ast.expr.name)
        if type(if_expr[2]) is not BoolType:
            raise TypeMismatchInStatement(ast)
        self.visit(ast.thenStmt, (symbol_stack, inLoop, inner_env))
        self.visit(ast.elseStmt, (symbol_stack, inLoop, inner_env))

    def visitFor(self, ast: For, c):
        """
        id: Id
        expr1: Expr
        expr2: Expr
        loop: Stmt
        expr3: Expr = None
        """
        (symbol_stack, inLoop, inner_env, outer_env, const_decl_flag) = c
        idType = self.visit(ast.id, (symbol_stack, inner_env))
        expr1Type = self.visit(ast.expr1, (symbol_stack, inner_env, outer_env, const_decl_flag))
        expr2Type = self.visit(ast.expr2, (symbol_stack, inner_env, outer_env, const_decl_flag))
        if ast.expr3 is not None:
            expr3Type = self.visit(ast.expr3, (symbol_stack, inner_env, outer_env, const_decl_flag))
            if expr3Type[0] in ["instance", "static"]:
                if ExpUtils.isNotAccess(ast.expr3):
                    raise Undeclared(Identifier(), ast.expr3.name)
                if not(type(expr3Type[2] is IntType)):  # The type of three expression <expr1>, <expr2>, <expr3> must be in integer
                    raise TypeMismatchInStatement(ast)

        if idType[0] in ["instance", "static"]:
            if ExpUtils.isNotAccess(ast.id):
                raise Undeclared(Identifier(), ast.id.name)
        if idType[1] == "immutable":
            raise CannotAssignToConstant(ast.expr1)
        if expr1Type[0] in ["instance", "static"]:
            if ExpUtils.isNotAccess(ast.expr1):
                raise Undeclared(Identifier(), ast.expr1.name)
        if expr2Type[0] in ["instance", "static"]:
            if ExpUtils.isNotAccess(ast.expr2):
                raise Undeclared(Identifier(), ast.expr2.name)
        # The type of a scalar variable, expression 1 and expression 2 in a for statement must be integer.
        if not(type(idType[2]) is IntType) or not(type(expr1Type[2]) is IntType) or not(type(expr2Type[2]) is IntType):
            raise TypeMismatchInStatement(ast)

        # Visit statements
        self.visit(ast.loop, (symbol_stack, True, inner_env, outer_env))

    def visitBreak(self, ast, c):
        (symbol_stack, inLoop, inner_env, outer_env, const_decl_flag) = c
        if not inLoop:
            raise MustInLoop(ast)

    def visitContinue(self, ast, c):
        (symbol_stack, inLoop, inner_env, outer_env, const_decl_flag) = c
        if not inLoop:
            raise MustInLoop(ast)

    def visitReturn(self, ast, c):
        # expr: Expr = None
        (symbol_stack, inLoop, inner_env, outer_env, const_decl_flag) = c
        if ast.expr is not None:
            return_type = self.visit(ast.expr, (symbol_stack, inner_env, outer_env, const_decl_flag))
            if return_type[0] in ["instance", "static"]: # Return Attribute
                if ExpUtils.isNotAccess(ast.expr):
                    raise Undeclared(Identifier(), ast.expr.name)
        current_class = list(outer_env)[-1]
        current_method = list(outer_env[current_class])[-1]
        method_rettype = outer_env[current_class][current_method][2]
        if method_rettype is None:
            if ast.expr is None:
                outer_env[current_class][current_method][2] = VoidType()
            else:
                outer_env[current_class][current_method][2] = return_type[2]
        else:
            if not(method_rettype is return_type[2]):
                raise TypeMismatchInStatement(ast)

    def visitCallStmt(self, ast, c):
        """
        obj: Expr
        method: Id
        param: List[Expr]
        """
        (symbol_stack, inLoop, inner_env, outer_env, const_decl_flag) = c
        isDolla = False
        if ast.method.name[0] == "$":
            isDolla = True
        if type(ast.obj) is SelfLiteral:
            current_class = list(outer_env)[-1]
            method = self.getInfoAccess(ast.method, (Method(), current_class, outer_env))
            if method[0] == "static":
                raise IllegalMemberAccess(ast)
        else:
            if isDolla:
                if outer_env.get(ast.obj.name) is not None:
                    class_name = ast.obj.name
                else:
                    raise Undeclared(Class(), ast.obj.name)
            else:
                class_name = self.visit(ast.obj, (symbol_stack, inner_env, outer_env, const_decl_flag))
            # Case 1: x.b();
            if type(class_name) is tuple:
                if not(type(class_name[2]) is ClassType):
                    raise TypeMismatchInExpression(ast)
                method = self.getInfoAccess(ast.method, (Method(), class_name[2].classname.name, outer_env))
                if method[0] == "static":
                    raise IllegalMemberAccess(ast)
                if method[1] != "method":
                    raise TypeMismatchInExpression(ast)

            # Case 2: E.b();
            if type(class_name) is str:
                method = self.getInfoAccess(ast.method, (Method(), class_name, outer_env))
                if method[0] == "instance":
                    raise IllegalMemberAccess(ast)
                if method[1] != "method":
                    raise TypeMismatchInExpression(ast)

        arg = list(map(lambda x: self.visit(x, (symbol_stack, inner_env, outer_env, const_decl_flag)), ast.param))
        if len(arg) != len(method[3]):
            raise TypeMismatchInExpression(ast)

        for i in range(len(arg)):
            arg_type = arg[i][2]
            param_type = method[3][i]
            if not(type(arg_type) is type(param_type)):
                if not(type(param_type) is FloatType and type(arg_type) is IntType):
                    raise TypeMismatchInStatement(ast)

    def visitBinaryOp(self, ast: BinaryOp, c):
        """
        op: str
        left: Expr
        right: Expr
        """
        # Because array element has been changed from literal to expr --> a = b + c[1]; --> Illegal Constant Expression
        if ExpUtils.isNotConstOperand(ast.left) or ExpUtils.isNotConstOperand(ast.right):
            raise IllegalConstantExpression(ast)
        (symbol_stack, inner_env, outer_env, const_decl_flag) = c
        lhs = self.visit(ast.left, (symbol_stack, inner_env, outer_env, const_decl_flag))
        rhs = self.visit(ast.right, (symbol_stack, inner_env, outer_env, const_decl_flag))
        if lhs[0] in ["instance", "static"]:
            if ExpUtils.isNotAccess(ast.left):
                raise Undeclared(Identifier(), ast.left.name)
        if rhs[0] in ["instance", "static"]:
            if ExpUtils.isNotAccess(ast.right):
                raise Undeclared(Identifier(), ast.right.name)
        if const_decl_flag:
            if lhs[1] == "mutable" or rhs[1] == "mutable":
                raise IllegalConstantExpression(ast)
        op = str(ast.op)
        # -------------------Arithmetic operators-------------------
        if op in ["+", "-", "*", "/"]:
            if ExpUtils.isNotIntFloatType(lhs[2]) or ExpUtils.isNotIntFloatType(rhs[2]):
                raise TypeMismatchInExpression(ast)
            elif type(lhs[2]) is FloatType or type(rhs[2]) is FloatType:
                return (None, None, FloatType())
            # print("lhs[2]: " + str(lhs[2]) + "\n")
            # print("rhs[2]: " + str(rhs[2]) + "\n")
            return (None, None, IntType())
        elif op in ["%"]:
            if not(type(lhs[2]) is IntType) or not(type(rhs[2]) is IntType):
                raise TypeMismatchInExpression(ast)
            return (None, None, IntType())
        # -------------------Boolean operators-------------------
        elif op in ["&&", "||"]:
            if type(lhs[2]) is BoolType and type(rhs[2]) is BoolType:
                return (None, None, BoolType())
            raise TypeMismatchInExpression(ast)
        # -------------------String operators-------------------
        elif op in ["+."]:
            if type(lhs[2]) is StringType and type(rhs[2]) is StringType:
                return (None, None, StringType())
            raise TypeMismatchInExpression(ast)
        # -------------------Relational operators-------------------
        elif op in ["==", "!="]:
            if ExpUtils.isNotIntBoolType(lhs[2]) or ExpUtils.isNotIntBoolType(rhs[2]):
                raise TypeMismatchInExpression(ast)
        elif op in ["<", ">", "<=", ">="]:
            if ExpUtils.isNotIntFloatType(lhs[2]) or ExpUtils.isNotIntFloatType(rhs[2]):
                raise TypeMismatchInExpression(ast)
            elif type(lhs[2]) is FloatType or type(rhs[2]) is FloatType:
                return (None, None, FloatType())
            return (None, None, IntType())

    def visitUnaryOp(self, ast: UnaryOp, c):
        """
        op: str
        body: Expr
        """
        (symbol_stack, inner_env, outer_env, const_decl_flag) = c
        expr = self.visit(ast.body, (symbol_stack, inner_env, outer_env, const_decl_flag))
        op = str(ast.op)
        if (op == "-" and ExpUtils.isNotIntFloatType(expr[2])) or (op == "!" and not(type(expr[2]) is BoolType)):
            raise TypeMismatchInExpression(ast)
        return (None, None, expr[2])

    def visitCallExpr(self, ast, c):
        """
        obj: Expr
        method: Id
        param: List[Expr]
        """
        (symbol_stack, inner_env, outer_env, const_decl_flag) = c
        isDolla = False
        if ast.method.name[0] == "$":
            isDolla = True
        if type(ast.obj) is SelfLiteral:
            current_class = list(outer_env)[-1]
            method = self.getInfoAccess(ast.method, (Method(), current_class, outer_env))
            if method[0] == "static":
                raise IllegalMemberAccess(ast)
        else:
            if isDolla: # Class name
                if outer_env.get(ast.obj.name) is not None:
                    class_name = ast.obj.name
                else:
                    raise Undeclared(Class(), ast.obj.name)
            else: # Object
                class_name = self.visit(ast.obj, (symbol_stack, inner_env, outer_env, const_decl_flag))

            # Case 1: x.b()
            if type(class_name) is tuple:
                if not(type(class_name[2]) is ClassType):
                    raise TypeMismatchInExpression(ast)
                method = self.getInfoAccess(ast.method, (Method(), class_name[2].classname.name, outer_env))
                if method[0] == "static":
                    raise IllegalMemberAccess(ast)
                if method[1] != "method":
                    raise TypeMismatchInExpression(ast)

            # Case 2: E.b()
            if type(class_name) is str:
                method = self.getInfoAccess(ast.method, (Method(), class_name, outer_env))
                if method[0] == "instance":
                    raise IllegalMemberAccess(ast)
                if method[1] != "method":
                    raise TypeMismatchInExpression(ast)

        arg = list(map(lambda x: self.visit(x, (symbol_stack, inner_env, outer_env, const_decl_flag)), ast.param))
        if len(arg) != len(method[3]):
            raise TypeMismatchInExpression(ast)

        for i in range(len(arg)):
            arg_type = arg[i][2]
            param_type = method[3][i]
            if not(type(arg_type) is type(param_type)):
                if not(type(param_type) is FloatType and type(arg_type) is IntType):
                    raise TypeMismatchInExpression(ast)
        
        # print("method[2]: " + str(method[2]) + "\n")
        return (None, None, method[2])

    def getInfoAccess(self, ast, c):
        # env[method_name] = [kind, "method", None, paramTypeLst]
        kind, class_name, env = c
            
        # Case 1: If class E really has b()
        if env[class_name].get(ast.name) is not None:
            return env[class_name][ast.name]  # (kind, mutability, rettype) / [kind, "method", None, paramTypeLst]
        
        # Case 2: If class E is inherited from another class A and class A has b(), not class E
        # Step 1: Get the index of class E in the dictionary
        index = list(env).index(class_name)
        # Step 2: Access to the stack parent by the above index
        if self.parent[index] is not None:
            parent_name = self.parent[index]
            # Step 3: Check if parent class has b()
            if env[parent_name].get(ast.name) is not None:
                return env[parent_name][ast.name]
        
        raise Undeclared(kind, ast.name)

    def visitNewExpr(self, ast, c):
        """
        classname: Id
        param: List[Expr]
        """
        (symbol_stack, inner_env, outer_env, const_decl_flag) = c
        class_name = ast.classname.name
        if outer_env.get(class_name) is None:
            raise Undeclared(Class(), ast.classname.name)
        if len(ast.param) != 0:
            if outer_env[class_name].get("Constructor") is not None:
                # Make sure that Constructor in env is a method, not a variable
                if outer_env[class_name]["Constructor"][1] == "method" and outer_env[class_name]["Constructor"][0] == "instance":
                    # constructor: (kind, "method", None, param)
                    constructor = outer_env[class_name]["Constructor"]
            else:
                raise Undeclared(Method(), "Constructor")
            
            arg = list(map(lambda x: self.visit(x, (symbol_stack, inner_env, outer_env, const_decl_flag)), ast.param))
            if len(arg) != len(constructor[3]):
                raise TypeMismatchInExpression(ast)

            for i in range(len(arg)):
                arg_type = arg[i][2]
                param_type = constructor[3][i]
                if not(type(arg_type) is type(param_type)):
                    if not(type(param_type) is FloatType and type(arg_type) is IntType):
                        raise TypeMismatchInExpression(ast)
        
        return (None, None, ClassType(ast.classname))

    def visitArrayCell(self, ast, c):
        """
        arr: Expr
        idx: List[Expr]
        """
        (symbol_stack, inner_env, outer_env, const_decl_flag) = c
        arrType = self.visit(ast.arr, (symbol_stack, inner_env, outer_env, const_decl_flag))
        for x in ast.idx:
            idxType = self.visit(x, (symbol_stack, inner_env, outer_env, const_decl_flag))
            if not(type(idxType[2]) is IntType) or not(type(arrType[2]) is ArrayType):
                raise TypeMismatchInExpression(ast)
        # print("arrType[2]: " + str(arrType[2]))
        return (None, None, arrType[2])

    def visitFieldAccess(self, ast, c):
        """
        obj: Expr
        fieldname: Id
        """
        (symbol_stack, inner_env, outer_env, const_decl_flag) = c
        isDolla = False
        if ast.fieldname.name[0] == "$":
            isDolla = True
        if type(ast.obj) is SelfLiteral:    
            current_class = list(outer_env)[-1]
            field_name = self.getInfoAccess(ast.fieldname, (Attribute(), current_class, outer_env))
            if field_name[0] == "static":
                raise IllegalMemberAccess(ast)
        else:
            if isDolla:
                if outer_env.get(ast.obj.name) is not None:
                    class_name = ast.obj.name
                else:
                    raise Undeclared(Class(), ast.obj.name)
            else:
                class_name = self.visit(ast.obj, (symbol_stack, inner_env, outer_env, const_decl_flag))
            
            # Case 1: x.b
            if type(class_name) is tuple:
                if not(type(class_name[2]) is ClassType):
                    raise TypeMismatchInExpression(ast)
                field_name = self.getInfoAccess(ast.fieldname, (Attribute(), class_name[2].classname.name, outer_env))
                if field_name[0] == "static":
                    raise IllegalMemberAccess(ast)
                if field_name[1] == "method":
                    raise TypeMismatchInExpression(ast)

            # Case 2: E.b
            if type(class_name) is str:
                field_name = self.getInfoAccess(ast.fieldname, (Attribute(), class_name, outer_env))
                if field_name[0] == "instance":
                    raise IllegalMemberAccess(ast)
                if field_name[1] == "method":
                    raise TypeMismatchInExpression(ast)
        
        return field_name

    def visitIntLiteral(self, ast:IntLiteral, c):
        return (None, None, IntType())

    def visitFloatLiteral(self, ast, c):
        return (None, None, FloatType())

    def visitBooleanLiteral(self, ast, c):
        return (None, None, BoolType())

    def visitStringLiteral(self, ast, c):
        return (None, None, StringType())

    def visitNullLiteral(self, ast, c):
        return (None, None, NullLiteral())

    def visitSelfLiteral(self, ast, c):
        return (None, None, SelfLiteral())

    def visitArrayLiteral(self, ast, c):
        # value: List[Expr]
        (symbol_stack, inner_env, outer_env, const_decl_flag) = c
        valueLst = list(map(lambda x: self.visit(x, (symbol_stack, inner_env, outer_env, const_decl_flag)), ast.value))
        first_ele_type = valueLst[0][2]
        for ele_type in valueLst:
            if not(type(ele_type[2]) is type(first_ele_type)):
                raise IllegalArrayLiteral(ast)
        return (None, None, ArrayType(len(valueLst), first_ele_type))

    def visitIntType(self, ast, c):
        return IntType()

    def visitFloatType(self, ast, c):
        return FloatType()

    def visitBoolType(self, ast, c):
        return BoolType()

    def visitStringType(self, ast, c):
        return StringType()

    def visitArrayType(self, ast, c):
        return ast

    def visitClassType(self, ast, c):
        # classname: Id
        # Type of c: outer_env
        if c.get(ast.classname.name) is not None:
            return ast
        raise Undeclared(Class(), ast.classname.name)