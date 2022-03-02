from unittest import result
from D96Visitor import D96Visitor
from D96Parser import D96Parser
from AST import *

class ASTGeneration(D96Visitor):
    def checkStatic(self, attriname):
        if attriname[0] == "$":
            return True
        return False

    # program: classdecl+ EOF;
    def visitProgram(self, ctx: D96Parser.ProgramContext):
        res = []
        for x in ctx.classdecl():
            res += [self.visit(x)]
        return Program(res)

    # classdecl: Class ID (COLON ID)? LP member* RP;
    def visitClassdecl(self, ctx: D96Parser.ClassdeclContext):
        name = ctx.ID(0).getText()
        if ctx.COLON():
            parentname = Id(ctx.ID(1).getText())
        else:
            parentname = None
        memList = []
        for x in ctx.member():
            res = self.visitMember(x, name)
            if isinstance(res, list):
                memList.extend(res)
            else:
                memList += [res]
        name = Id(name)
        return ClassDecl(name, memList, parentname)

    # member: attr | constructor | destructor | method;
    def visitMember(self, ctx:D96Parser.MemberContext, classname: str):
        if ctx.method():
            return self.visitMethod(ctx.method(), classname)
        return self.visit(ctx.getChild(0))

    # vardecl_: AttriType iden idenlist* COLON typ SEMI;
    def visitVardecl_(self, ctx: D96Parser.Vardecl_Context):
        res = [] # -> [(Id, flag)]
        ans = []
        
        attriname = self.visit(ctx.iden())
        res += [(Id(attriname), self.checkStatic(attriname))]
        for x in ctx.idenlist():
            attriname = self.visit(x)
            res += [(Id(attriname), self.checkStatic(attriname))]

        vartype = self.visit(ctx.typ())
        if type(vartype) == ClassType:
            check_class = True
        else:
            check_class = False

        if ctx.AttriType().getText() == "Val":
            for x in res:
                if x[1] == True:
                    if check_class:
                        ans += [AttributeDecl(Static(), ConstDecl(x[0], vartype, NullLiteral()))]
                    else:
                        ans += [AttributeDecl(Static(), ConstDecl(x[0], vartype))]
                else:
                    if check_class:
                        ans += [AttributeDecl(Instance(), ConstDecl(x[0], vartype, NullLiteral()))]
                    else:
                        ans += [AttributeDecl(Instance(), ConstDecl(x[0], vartype))]
        else:
            for x in res:
                if x[1] == True:
                    if check_class:
                        ans += [AttributeDecl(Static(), VarDecl(x[0], vartype, NullLiteral()))]
                    else:
                        ans += [AttributeDecl(Static(), VarDecl(x[0], vartype))]
                else:
                    if check_class:
                        ans += [AttributeDecl(Instance(), VarDecl(x[0], vartype, NullLiteral()))]
                    else:
                        ans += [AttributeDecl(Instance(), VarDecl(x[0], vartype))]
        return ans

    # iden: DollaID | ID;
    def visitIden(self, ctx: D96Parser.IdenContext):
        return ctx.getChild(0).getText()

    # idenlist: COMMA (DollaID | ID);
    def visitIdenlist(self, ctx: D96Parser.IdenlistContext):
        return ctx.getChild(1).getText()

    # vardeclass: AttriType (DollaID | ID) varlist expr SEMI;
    # varlist: COMMA (DollaID | ID) varlist expr COMMA
    #        | COLON typ ASSIGN;
    def visitVardeclass(self, ctx: D96Parser.VardeclassContext):
        res = []
        exprlist = []
        ans = []
        if ctx.AttriType().getText() == 'Val':
            check_val = True
        else:
            check_val = False
        if ctx.ID():
            res += [(Id(ctx.ID().getText()), False)]
        else:
            res += [(Id(ctx.DollaID().getText()), True)]
        exprlist += [self.visit(ctx.expr())]

        ctx = ctx.varlist()
        while ctx.typ() is None:
            if ctx.ID():
                res += [(Id(ctx.ID().getText()), False)]
            else:
                res += [(Id(ctx.DollaID().getText()), True)]
            exprlist += [self.visit(ctx.expr())]
            ctx = ctx.varlist()

        vartype = self.visit(ctx.typ())
        exprlist = exprlist[::-1]
        if check_val:
            for id, x in enumerate(res):
                if x[1] == True:
                    ans += [AttributeDecl(Static(), ConstDecl(x[0], vartype, exprlist[id]))]
                else:
                    ans += [AttributeDecl(Instance(), ConstDecl(x[0], vartype, exprlist[id]))]
        else:
            for id, x in enumerate(res):
                if x[1] == True:
                    ans += [AttributeDecl(Static(), VarDecl(x[0], vartype, exprlist[id]))]
                else:
                    ans += [AttributeDecl(Instance(), VarDecl(x[0], vartype, exprlist[id]))]
        return ans

    # primi: BOOLEAN | INT | FLOAT | STRING;
    def visitPrimi(self, ctx: D96Parser.PrimiContext):
        if ctx.BOOLEAN():
            return BoolType()
        elif ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        return StringType()

    # typ: primi | arrtype | ID;
    def visitTyp(self, ctx: D96Parser.TypContext):
        if ctx.primi():
            return self.visit(ctx.primi())
        elif ctx.arrtype():
            return self.visit(ctx.arrtype())
        return ClassType(Id(ctx.ID().getText()))

    # arrtype: Array LS (primi | arrtype) COMMA INTLIT_ARR RS;
    def visitArrtype(self, ctx: D96Parser.ArrtypeContext):
        if ctx.primi():
            eleType = self.visit(ctx.primi())
        else:
            eleType = self.visit(ctx.arrtype())
        int_arr_text = ctx.INTLIT_ARR().getText()
        if int_arr_text[0] == '0':
            if int_arr_text[1] in ['b', 'B']:
                size = int(int_arr_text, 2)
            elif int_arr_text[1] in ['x', 'X']:
                size = int(int_arr_text, 16)
            else:
                size = int(int_arr_text, 8)
        else:
            size = int(int_arr_text, 10)
        return ArrayType(size, eleType)

    # constructor: Constructor LB paramlist? RB blockstate;
    def visitConstructor(self, ctx: D96Parser.ConstructorContext):
        if ctx.paramlist():
            param = self.visit(ctx.paramlist())
        else:
            param = []
        block = self.visit(ctx.blockstate())
        return MethodDecl(Instance(), Id("Constructor"), param, block)

    # destructor: Destructor LB RB blockstate;
    def visitDestructor(self, ctx: D96Parser.DestructorContext):
        block = self.visit(ctx.blockstate())
        return MethodDecl(Instance(), Id("Destructor"), [], block)

    # method: (DollaID | ID) LB paramlist? RB blockstate;
    def visitMethod(self, ctx: D96Parser.MethodContext, classname: str):
        if ctx.paramlist():
            param = self.visit(ctx.paramlist())
        else:
            param = []
        if ctx.DollaID():
            kind = Static()
            name = Id(ctx.DollaID().getText())
        else:
            kind = Instance()
            name = ctx.ID().getText()
            if name == 'main' and len(param) == 0 and classname == 'Program':
                kind = Static()
            name = Id(name)
        block = self.visit(ctx.blockstate())
        return MethodDecl(kind, name, param, block)

    # paramlist: param (SEMI param)*;
    # x, y : Int ; z : Float -> [VarDecl(Id(x), IntType), VarDecl(Id(y), IntType), VarDecl(Id(z), Float)]
    def visitParamlist(self, ctx: D96Parser.ParamlistContext):
        res = []
        for x in ctx.param():
            res += self.visit(x)
        return res

    # param: idlist COLON typ;
    # Var x, y: Int -> [VarDecl(Id(x), IntType), VarDecl(Id(y), IntType)]
    def visitParam(self, ctx: D96Parser.ParamContext):
        varType = self.visit(ctx.typ())
        idList = self.visit(ctx.idlist())
        res = []
        for x in idList:
            res += [VarDecl(x, varType)]
        return res

    # idlist: ID (COMMA ID)*;
    # x, y, z -> [Id(x), Id(y), Id(z)]
    def visitIdlist(self, ctx: D96Parser.IdlistContext):
        res = []
        for x in ctx.ID():
            res += [Id(x.getText())]
        return res

    # blockstate: LP blockstmt? RP;
    def visitBlockstate(self, ctx: D96Parser.BlockstateContext):
        if ctx.blockstmt():
            return self.visit(ctx.blockstmt())
        return Block([])

    # stmt: assignstmt | foreachstmt | ifstmt | breakstmt | continuestmt | returnstmt | instancestmt | invocastmt | blockstate;
    def visitStmt(self, ctx: D96Parser.StmtContext):
        return self.visit(ctx.getChild(0))

    # varstmt_decl_: AttriType idlist COLON typ SEMI;
    def visitVarstmt_decl_(self, ctx: D96Parser.Varstmt_decl_Context):
        ids = self.visit(ctx.idlist())
        ans = []
        
        vartype = self.visit(ctx.typ())
        if type(vartype) == ClassType:
            check_class = True
        else:
            check_class = False

        if ctx.AttriType().getText() == "Val":
            for x in ids:
                if check_class:
                    ans += [ConstDecl(x, vartype, NullLiteral())]
                else:
                    ans += [ConstDecl(x, vartype)]
        else:
            for x in ids:
                if check_class:
                    ans += [VarDecl(x, vartype, NullLiteral())]
                else:
                    ans += [VarDecl(x, vartype)]
        return ans

    # varstmt_declass: AttriType ID varstmt_list expr SEMI;
    # varstmt_list: COMMA ID varstmt_list expr COMMA
    #        	  | COLON typ ASSIGN;
    def visitVarstmt_declass(self, ctx: D96Parser.Varstmt_declassContext):
        res = [Id(ctx.ID().getText())]
        exprlist = [self.visit(ctx.expr())]
        ans = []
        if ctx.AttriType().getText() == 'Val':
            check_val = True
        else:
            check_val = False

        ctx = ctx.varstmt_list()
        while ctx.typ() is None:
            res += [Id(ctx.ID().getText())]
            exprlist += [self.visit(ctx.expr())]
            ctx = ctx.varstmt_list()

        vartype = self.visit(ctx.typ())
        exprlist = exprlist[::-1]
        if check_val:
            for id, x in enumerate(res):
                ans += [ConstDecl(x, vartype, exprlist[id])]
        else:
            for id, x in enumerate(res):
                ans += [VarDecl(x, vartype, exprlist[id])]
        return ans

    # assignstmt: assign_body SEMI;
    def visitAssignstmt(self, ctx: D96Parser.AssignstmtContext):
        return self.visit(ctx.assign_body())

    # assign_body: assign_lhs ASSIGN expr;
    def visitAssign_body(self, ctx: D96Parser.Assign_bodyContext):
        lhs = self.visit(ctx.assign_lhs())
        rhs = self.visit(ctx.expr())
        return Assign(lhs, rhs)

    # assign_lhs: element_expr | scalar_var;
    def visitAssign_lhs(self, ctx: D96Parser.Assign_lhsContext):
        if ctx.element_expr():
            return self.visit(ctx.element_expr())
        return self.visit(ctx.scalar_var())

    # ifstmt: If LB expr RB blockstate (Elseif LB expr RB blockstate)* (Else blockstate)?;
    def visitIfstmt(self, ctx: D96Parser.IfstmtContext):
        num_blockstmt = len(ctx.blockstate())
        arr_blockstmt = list(range(num_blockstmt)) # [0 .. n-1]
        arr_blockstmt = arr_blockstmt[::-1] # [n-1 .. 0]
        if_expr = self.visit(ctx.expr(0))
        if_stmt = self.visit(ctx.blockstate(0))
        else_stmt = None

        # Case 1: If & Else or only If 
        if (num_blockstmt == 1) or (num_blockstmt == 2 and ctx.Else()):
            if ctx.Else():
                else_stmt = self.visit(ctx.blockstate(1))
            return If(if_expr, if_stmt, else_stmt)

        # Case 2: If & Elseif
        elif not ctx.Else():
            if_stmt = None
            for i in arr_blockstmt:
                elseif_expr = self.visit(ctx.expr(i))
                elseif_stmt = self.visit(ctx.blockstate(i))
                if_stmt = If(elseif_expr, elseif_stmt, if_stmt)
            return if_stmt

        # Case 3: If, Elseif & Else
        else_block = None
        elseif_expr = None
        elseif_stmt = None
        for i in arr_blockstmt:
            if i == (num_blockstmt - 1):
                else_stmt = self.visit(ctx.blockstate(i))
            elseif_stmt = self.visit(ctx.blockstate(i - 1))
            elseif_expr = self.visit(ctx.expr(i - 1))
            else_stmt = If(elseif_expr, elseif_stmt, else_stmt)
            if i == 2:
                break
        else_block = else_stmt
        return If(if_expr, if_stmt, else_block)

    # foreachstmt: Foreach LB scalar_var In expr DOUBLEDOT expr (By expr)? RB LP blockstmt RP;
    def visitForeachstmt(self, ctx: D96Parser.ForeachstmtContext):
        id = self.visit(ctx.scalar_var())
        expr1 = self.visit(ctx.expr(0))
        expr2 = self.visit(ctx.expr(1))
        expr3 = IntLiteral(1)
        if ctx.By():
            expr3 = self.visit(ctx.expr(2))
        loop = self.visit(ctx.blockstmt())
        return For(id, expr1, expr2, loop, expr3)

    # breakstmt: Break SEMI;
    def visitBreakstmt(self, ctx: D96Parser.BreakstmtContext):
        return Break()

    # continuestmt: Continue SEMI;
    def visitContinuestmt(self, ctx: D96Parser.ContinuestmtContext):
        return Continue()

    # returnstmt: Return expr? SEMI;
    def visitReturnstmt(self, ctx: D96Parser.ReturnstmtContext):
        expression = None
        if ctx.expr():
            expression = self.visit(ctx.expr())
        return Return(expression)

    # scalar_var: scalar_helper INSTANTAC ID
    # 		    | ID STATICAC DollaID
    # 		    | ID;
    def visitScalar_var(self, ctx: D96Parser.Scalar_varContext):
        if ctx.INSTANTAC():
            obj = self.visit(ctx.scalar_helper())
            method = Id(ctx.ID().getText())
            return FieldAccess(obj, method)
        elif ctx.STATICAC():
            obj = Id(ctx.ID().getText())
            method = Id(ctx.DollaID().getText())
            return FieldAccess(obj, method)
        return Id(ctx.ID().getText())

    # scalar_helper: scalar_helper INSTANTAC ID arg?
    # 			   | invocast_helper
    # 			   | Self
    # 			   | ID;
    def visitScalar_helper(self, ctx: D96Parser.Scalar_helperContext):
        if ctx.INSTANTAC():
            obj = self.visit(ctx.scalar_helper())
            method = Id(ctx.ID().getText())
            if ctx.arg():
                param = self.visit(ctx.arg())
                return CallExpr(obj, method, param)
            else:
                return FieldAccess(obj, method)
        elif ctx.Self():
            return SelfLiteral()
        elif ctx.ID():
            return Id(ctx.ID().getText())
        return self.visit(ctx.invocast_helper())

    # instance_helper: New ID arg
    # 			     | instance_helper INSTANTAC ID arg?
    # 			     | instance_helper index_operators
    # 			     | invocast_helper
    #                | LB instance_helper RB
    # 			     | Self
    # 			     | ID;
    def visitInstance_helper(self, ctx: D96Parser.Instance_helperContext):
        if ctx.New():
            name = Id(ctx.ID().getText())
            param = self.visit(ctx.arg())
            return NewExpr(name, param)
        elif ctx.INSTANTAC():
            obj = self.visit(ctx.instance_helper())
            method = Id(ctx.ID().getText())
            if ctx.arg():
                param = self.visit(ctx.arg())
                return CallExpr(obj, method, param)
            else:
                return FieldAccess(obj, method)
        elif ctx.getChildCount() == 2:
            arr = self.visit(ctx.instance_helper())
            idx = self.visit(ctx.index_operators())
            return ArrayCell(arr, idx)
        elif ctx.invocast_helper():
            return self.visit(ctx.invocast_helper())
        elif ctx.LB():
            return self.visit(ctx.instance_helper())
        elif ctx.Self():
            return SelfLiteral()
        return Id(ctx.ID().getText())

    # invocast_helper: ID STATICAC DollaID arg?;
    def visitInvocast_helper(self, ctx: D96Parser.Invocast_helperContext):
        obj = Id(ctx.ID().getText())
        method = Id(ctx.DollaID().getText())
        if ctx.arg():
            param = self.visit(ctx.arg())
            return CallExpr(obj, method, param)
        return FieldAccess(obj, method)

    # instancestmt: instance_helper INSTANTAC ID arg SEMI;
    def visitInstancestmt(self, ctx: D96Parser.InstancestmtContext):
        obj = self.visit(ctx.instance_helper())
        method = Id(ctx.ID().getText())
        param = self.visit(ctx.arg())
        return CallStmt(obj, method, param)

    # invocastmt: ID STATICAC DollaID arg SEMI;
    def visitInvocastmt(self, ctx: D96Parser.InvocastmtContext):
        obj = Id(ctx.ID().getText())
        method = Id(ctx.DollaID().getText())
        param = self.visit(ctx.arg())
        return CallStmt(obj, method, param)

    # arg: LB exprlist? RB;
    def visitArg(self, ctx: D96Parser.ArgContext):
        if ctx.exprlist():
            return self.visit(ctx.exprlist())
        return []

    # blockstmt: statement+;
    # Block([Return(a), VarDecl(Id(x), IntType)])
    def visitBlockstmt(self, ctx: D96Parser.BlockstmtContext):
        res = []
        for x in ctx.statement():
            result = self.visit(x)
            if isinstance(result, list):
                res.extend(result)
            else:
                res += [result]
        return Block(res)

    # statement: varstmt | stmt;
    def visitStatement(self, ctx: D96Parser.StatementContext):
        if ctx.varstmt():
            return self.visit(ctx.varstmt())
        return self.visit(ctx.stmt())

    # literal: INTLIT_ARR | INTLIT | FLOATLIT | BOOLLIT | STRLIT | index_arrlit | multi_arrlit;
    def visitLiteral(self, ctx: D96Parser.LiteralContext):
        if ctx.INTLIT_ARR():
            int_arr_text = ctx.INTLIT_ARR().getText()
            if int_arr_text[0] == '0':
                if int_arr_text[1] in ['b', 'B']:
                    return IntLiteral(int(int_arr_text, 2))
                elif int_arr_text[1] in ['x', 'X']:
                    return IntLiteral(int(int_arr_text, 16))
                else:
                    return IntLiteral(int(int_arr_text, 8))
            return IntLiteral(int(int_arr_text, 10)) 
        elif ctx.INTLIT():
            int_text = ctx.INTLIT().getText()
            if int_text[0] == '0' and len(int_text) > 1:
                if int_text[1] in ['b', 'B']:
                    return IntLiteral(int(int_text, 2))
                elif int_text[1] in ['x', 'X']:
                    return IntLiteral(int(int_text, 16))
                else:
                    return IntLiteral(int(int_text, 8))
            return IntLiteral(int(int_text, 10))
        elif ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        elif ctx.BOOLLIT():
            return BooleanLiteral(ctx.BOOLLIT().getText() == "True")
        elif ctx.STRLIT():
            return StringLiteral(ctx.STRLIT().getText())
        elif ctx.index_arrlit():
            return self.visit(ctx.index_arrlit())
        return self.visit(ctx.multi_arrlit())

    # index_arrlit: Array arg;
    # Array(1, 2, 3) -> [1, 2, 3]
    def visitIndex_arrlit(self, ctx: D96Parser.Index_arrlitContext):
        value = self.visit(ctx.arg())
        return ArrayLiteral(value)

    # exprlist: expr (COMMA expr)*;
    # a = a + 1, b = a + 2 -> [AssignStmt(), AssignStmt()]
    def visitExprlist(self, ctx: D96Parser.ExprlistContext):
        res = []
        for x in ctx.expr():
            res += [self.visit(x)]
        return res

    # multi_arrlit: Array LB index_arrlit+ RB;
    # Array(Array(1, 2, 3), Array(4, 5, 6)) -> [[1, 2, 3], [4, 5, 6]]
    def visitMulti_arrlit(self, ctx: D96Parser.Multi_arrlitContext):
        res = []
        for x in ctx.index_arrlit():
            res += self.visit(x)
        return ArrayLiteral(res)

    # operands: literal | Self | Null | ID;
    def visitOperands(self, ctx: D96Parser.OperandsContext):
        if ctx.Self():
            return SelfLiteral()
        elif ctx.Null():
            return NullLiteral()
        elif ctx.ID():
            return Id(ctx.ID().getText())
        return self.visit(ctx.literal())

    # element_expr: scalar_var index_operators;
    # a[1][2] -> ArrayCell(a, [1, 2])
    def visitElement_expr(self, ctx: D96Parser.Element_exprContext):
        arr = self.visit(ctx.scalar_var())
        idx = self.visit(ctx.index_operators())
        return ArrayCell(arr, idx)

    # index_operators: (LS expr RS)+;
    def visitIndex_operators(self, ctx: D96Parser.Index_operatorsContext):
        res = []
        for x in ctx.expr():
            res += [self.visit(x)]
        return res

    # expr: expr1 (STRCONCATE | COMPARESTR) expr1 | expr1;
    def visitExpr(self, ctx: D96Parser.ExprContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr1(0))
        op = ctx.getChild(1).getText()
        lhs = self.visit(ctx.expr1(0))
        rhs = self.visit(ctx.expr1(1))
        return BinaryOp(op, lhs, rhs)

    # expr1: expr2 (EQUAL | NOTEQUAL | SMALLER | GREATER | SMALLEREQUAL | GREATEREQUAL) expr2 | expr2;
    def visitExpr1(self, ctx: D96Parser.Expr1Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr2(0))
        op = ctx.getChild(1).getText()
        lhs = self.visit(ctx.expr2(0))
        rhs = self.visit(ctx.expr2(1))
        return BinaryOp(op, lhs, rhs)

    # expr2: expr2 (LOGICALAND | LOGICALOR) expr3 | expr3;
    def visitExpr2(self, ctx: D96Parser.Expr2Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr3())
        op = ctx.getChild(1).getText()
        lhs = self.visit(ctx.expr2())
        rhs = self.visit(ctx.expr3())
        return BinaryOp(op, lhs, rhs)

    # expr3: expr3 (ADDITION | SUBTRACTION) expr4 | expr4;
    def visitExpr3(self, ctx: D96Parser.Expr3Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr4())
        op = ctx.getChild(1).getText()
        lhs = self.visit(ctx.expr3())
        rhs = self.visit(ctx.expr4())
        return BinaryOp(op, lhs, rhs)

    # expr4: expr4 (MULTIPLICATION | DIVISION | MODULO) expr5 | expr5;
    def visitExpr4(self, ctx: D96Parser.Expr4Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr5())
        op = ctx.getChild(1).getText()
        lhs = self.visit(ctx.expr4())
        rhs = self.visit(ctx.expr5())
        return BinaryOp(op, lhs, rhs)

    # expr5: LOGICALNOT expr5 | expr6;
    def visitExpr5(self, ctx: D96Parser.Expr5Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr6())
        op = ctx.LOGICALNOT().getText()
        body = self.visit(ctx.expr5())
        return UnaryOp(op, body)

    # expr6: SUBTRACTION expr6 | expr7;
    def visitExpr6(self, ctx: D96Parser.Expr6Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr7())
        op = ctx.SUBTRACTION().getText()
        body = self.visit(ctx.expr6())
        return UnaryOp(op, body)

    # expr7: expr7 LS expr7 RS | expr8;
    def visitExpr7(self, ctx: D96Parser.Expr7Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr8())
        indexlist = []
        indexlist += [self.visit(ctx.expr7(1))]
        ctx = ctx.expr7(0)
        while ctx.LS():
            indexlist += [self.visit(ctx.expr7(1))]
            ctx = ctx.expr7(0)
        arr = self.visit(ctx)
        indexlist = indexlist[::-1]
        return ArrayCell(arr, indexlist)

    # expr8: expr8 INSTANTAC ID arg? | expr9;
    def visitExpr8(self, ctx: D96Parser.Expr8Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr9())
        obj = self.visit(ctx.expr8())
        method = Id(ctx.ID().getText())
        if ctx.arg():
            param = self.visit(ctx.arg())
            return CallExpr(obj, method, param)
        return FieldAccess(obj, method)

    # expr9: ID STATICAC DollaID arg? | expr10;
    def visitExpr9(self, ctx: D96Parser.Expr9Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr10())
        obj = Id(ctx.ID().getText())
        method = Id(ctx.DollaID().getText())
        if ctx.arg():
            param = self.visit(ctx.arg())
            return CallExpr(obj, method, param)
        return FieldAccess(obj, method)

    # expr10: New ID arg | expr11;
    def visitExpr10(self, ctx: D96Parser.Expr10Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr11())
        classname = Id(ctx.ID().getText())
        param = self.visit(ctx.arg())
        return NewExpr(classname, param)

    # expr11: operands | LB expr RB;
    def visitExpr11(self, ctx: D96Parser.Expr11Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.operands())
        return self.visit(ctx.expr())