import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):
    def test_program_structure1(self):
        input = """Class Program {}"""
        expect = "Program([ClassDecl(Id(Program),[])])"
        self.assertTrue(TestAST.test(input, expect, 301))

    def test_program_structure2(self):
        input = """Class _program123 {}"""
        expect = "Program([ClassDecl(Id(_program123),[])])"
        self.assertTrue(TestAST.test(input, expect, 302))

    def test_program_structure3(self):
        input = """Class Program {
            main(){}
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([]))])])"
        self.assertTrue(TestAST.test(input, expect, 303))

    def test_program_structure4(self):
        input = """Class _program123 {
            main(a: Int){}
        }"""
        expect = "Program([ClassDecl(Id(_program123),[MethodDecl(Id(main),Instance,[param(Id(a),IntType)],Block([]))])])"
        self.assertTrue(TestAST.test(input, expect, 304))

    def test_program_structure5(self):
        input = """Class Program {
            main(a : Int) {}
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Instance,[param(Id(a),IntType)],Block([]))])])"
        self.assertTrue(TestAST.test(input, expect, 305))

    def test_program_structure6(self):
        input = """Class _Continue {
            main() {}
        }"""
        expect = "Program([ClassDecl(Id(_Continue),[MethodDecl(Id(main),Instance,[],Block([]))])])"
        self.assertTrue(TestAST.test(input, expect, 306))

    def test_program_structure7(self):
        input = """Class Program {} Class _program {} Class program {}"""
        expect = "Program([ClassDecl(Id(Program),[]),ClassDecl(Id(_program),[]),ClassDecl(Id(program),[])])"
        self.assertTrue(TestAST.test(input, expect, 307))

    def test_program_structure8(self):
        input = """Class Program {
            _main() {}
            main() {}
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(_main),Instance,[],Block([])),MethodDecl(Id(main),Static,[],Block([]))])])"
        self.assertTrue(TestAST.test(input, expect, 308))

    def test_program_structure9(self):
        input = """Class Program {
            main() {
                Val a: Array[Array[Int, 10], 0x15];
                Return;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([ConstDecl(Id(a),ArrayType(21,ArrayType(10,IntType)),None),Return()]))])])"
        self.assertTrue(TestAST.test(input, expect, 309))

    def test_attr_declaration1(self):
        input = """Class Shape {
            Var num: Array[Int, 2] = Array(1, 2 + 3);
        }"""
        expect = "Program([ClassDecl(Id(Shape),[AttributeDecl(Instance,VarDecl(Id(num),ArrayType(2,IntType),[IntLit(1),BinaryOp(+,IntLit(2),IntLit(3))]))])])"
        self.assertTrue(TestAST.test(input, expect, 310))

    def test_attr_declaration2(self):
        input = """Class Shape {
            Val $num: Array[Int, 2] = Array(0123 + 0456, 1_234);
        }"""
        expect = "Program([ClassDecl(Id(Shape),[AttributeDecl(Static,ConstDecl(Id($num),ArrayType(2,IntType),[BinaryOp(+,IntLit(83),IntLit(302)),IntLit(1234)]))])])"
        self.assertTrue(TestAST.test(input, expect, 311))

    def test_method_declaration1(self):
        input = """Class Shape {
            Var num1, num2: Int = 1, 2;
            GetFunc(a, b: Int ; c: Float) {
                Var num3: Int = a;
                Val num4, num5: Int = a,b;
            }
        }"""
        expect = "Program([ClassDecl(Id(Shape),[AttributeDecl(Instance,VarDecl(Id(num1),IntType,IntLit(1))),AttributeDecl(Instance,VarDecl(Id(num2),IntType,IntLit(2))),MethodDecl(Id(GetFunc),Instance,[param(Id(a),IntType),param(Id(b),IntType),param(Id(c),FloatType)],Block([VarDecl(Id(num3),IntType,Id(a)),ConstDecl(Id(num4),IntType,Id(a)),ConstDecl(Id(num5),IntType,Id(b))]))])])"
        self.assertTrue(TestAST.test(input, expect, 312))
    
    def test_method_declaration2(self):
        input = """Class Shape {
            Var num1, num2: Int = 1, 0b10;
            GetFunc(a, b: Int; c: Float) {
                Var num3: Int = a;
                Val num4: Int = b;
            }
        }"""
        expect = "Program([ClassDecl(Id(Shape),[AttributeDecl(Instance,VarDecl(Id(num1),IntType,IntLit(1))),AttributeDecl(Instance,VarDecl(Id(num2),IntType,IntLit(2))),MethodDecl(Id(GetFunc),Instance,[param(Id(a),IntType),param(Id(b),IntType),param(Id(c),FloatType)],Block([VarDecl(Id(num3),IntType,Id(a)),ConstDecl(Id(num4),IntType,Id(b))]))])])"
        self.assertTrue(TestAST.test(input, expect, 313))

    def test_attr_var_decl1(self):
        input = """Class Shape {
            Var num1: Int = True;
            Val $num2: Boolean = 1;
            main() {
                Var num3: Array[Int, 2] = Array("abc", 2);
            }
        }"""
        expect = "Program([ClassDecl(Id(Shape),[AttributeDecl(Instance,VarDecl(Id(num1),IntType,BooleanLit(True))),AttributeDecl(Static,ConstDecl(Id($num2),BoolType,IntLit(1))),MethodDecl(Id(main),Instance,[],Block([VarDecl(Id(num3),ArrayType(2,IntType),[StringLit(abc),IntLit(2)])]))])])"
        self.assertTrue(TestAST.test(input, expect, 314))

    def test_attr_var_decl2(self):
        input = """Class Program {
            Var $a: Int = 0b1111;
            Var b: Float = 5.5e3;
            main() {
                Var res: Int = a + b;
                Out.printInt(res);
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[AttributeDecl(Static,VarDecl(Id($a),IntType,IntLit(15))),AttributeDecl(Instance,VarDecl(Id(b),FloatType,FloatLit(5500.0))),MethodDecl(Id(main),Static,[],Block([VarDecl(Id(res),IntType,BinaryOp(+,Id(a),Id(b))),Call(Id(Out),Id(printInt),[Id(res)])]))])])"
        self.assertTrue(TestAST.test(input, expect, 315))

    def test_attr_var_decl3(self):
        input = """Class Program {
            Var a: Int = 1;
            main() {
                Var b: Int = 2;
                Var res: Int = a + b;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[AttributeDecl(Instance,VarDecl(Id(a),IntType,IntLit(1))),MethodDecl(Id(main),Static,[],Block([VarDecl(Id(b),IntType,IntLit(2)),VarDecl(Id(res),IntType,BinaryOp(+,Id(a),Id(b)))]))])])"
        self.assertTrue(TestAST.test(input, expect, 316))

    def test_attr_var_decl4(self):
        input = """Class Program {
            Var ab: String = "";
            Val $bc: String = "a1b2";
            main() {
                Var a: String = "abcdef";
                Val b: String = "123456";
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[AttributeDecl(Instance,VarDecl(Id(ab),StringType,StringLit())),AttributeDecl(Static,ConstDecl(Id($bc),StringType,StringLit(a1b2))),MethodDecl(Id(main),Static,[],Block([VarDecl(Id(a),StringType,StringLit(abcdef)),ConstDecl(Id(b),StringType,StringLit(123456))]))])])"
        self.assertTrue(TestAST.test(input, expect, 317))

    def test_attr_var_decl5(self):
        input = """Class Program1 {
            Val a: Int = Self.function(1, str1 +. str2);
        }"""
        expect = "Program([ClassDecl(Id(Program1),[AttributeDecl(Instance,ConstDecl(Id(a),IntType,CallExpr(Self(),Id(function),[IntLit(1),BinaryOp(+.,Id(str1),Id(str2))])))])])"
        self.assertTrue(TestAST.test(input, expect, 318))

    def test_constructor_destructor1(self):
        input = """Class Shape {
            Constructor() {
                Return;
            }
            Destructor() {}
        }
        """
        expect = "Program([ClassDecl(Id(Shape),[MethodDecl(Id(Constructor),Instance,[],Block([Return()])),MethodDecl(Id(Destructor),Instance,[],Block([]))])])"
        self.assertTrue(TestAST.test(input, expect, 319))

    def test_constructor_destructor2(self):
        input = """Class Shape {
            Constructor() {}
            Destructor() {}
        }"""
        expect = "Program([ClassDecl(Id(Shape),[MethodDecl(Id(Constructor),Instance,[],Block([])),MethodDecl(Id(Destructor),Instance,[],Block([]))])])"
        self.assertTrue(TestAST.test(input, expect, 320))

    def test_constructor_destructor3(self):
        input = """Class Shape {
            Constructor() {
                Return;
            }
            Destructor() {
                Return;
            }
        }"""
        expect = "Program([ClassDecl(Id(Shape),[MethodDecl(Id(Constructor),Instance,[],Block([Return()])),MethodDecl(Id(Destructor),Instance,[],Block([Return()]))])])"
        self.assertTrue(TestAST.test(input, expect, 321))

    def test_constructor_destructor4(self):
        input = """Class Shape {
            Constructor(length, width: Int; area: Float) {
                Self.length = length;
                Self.width = width;
                Return;
            }
            Destructor() {}
        }"""
        expect = "Program([ClassDecl(Id(Shape),[MethodDecl(Id(Constructor),Instance,[param(Id(length),IntType),param(Id(width),IntType),param(Id(area),FloatType)],Block([AssignStmt(FieldAccess(Self(),Id(length)),Id(length)),AssignStmt(FieldAccess(Self(),Id(width)),Id(width)),Return()])),MethodDecl(Id(Destructor),Instance,[],Block([]))])])"
        self.assertTrue(TestAST.test(input, expect, 322))

    def test_constructor_destructor5(self):
        input = """Class Shape {
            Constructor() {
                Var a: Int = 10;
                Return;
            }
            Destructor() {}
        }"""
        expect = "Program([ClassDecl(Id(Shape),[MethodDecl(Id(Constructor),Instance,[],Block([VarDecl(Id(a),IntType,IntLit(10)),Return()])),MethodDecl(Id(Destructor),Instance,[],Block([]))])])"
        self.assertTrue(TestAST.test(input, expect, 323))

    def test_constructor_destructor6(self):
        input = """Class Program {
            Destructor() {
                Self.call();
            }
            main() {
                Self.a();
                Return;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(Destructor),Instance,[],Block([Call(Self(),Id(call),[])])),MethodDecl(Id(main),Static,[],Block([Call(Self(),Id(a),[]),Return()]))])])"
        self.assertTrue(TestAST.test(input, expect, 324))

    def test_indexed_arr1(self):
        input = """Class Program {
            main() {
                Val a : Array[Int, 1] = Array(1);
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([ConstDecl(Id(a),ArrayType(1,IntType),[IntLit(1)])]))])])"
        self.assertTrue(TestAST.test(input, expect, 325))

    def test_indexed_arr2(self):
        input = """Class Program {
            main() {
                Val a : Array[Int, 0xAB];
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([ConstDecl(Id(a),ArrayType(171,IntType),None)]))])])"
        self.assertTrue(TestAST.test(input, expect, 326))

    def test_multi_arr1(self):
        input = """Class Program {
            main() {
                a = Array(Array("A"), Array("B"), Array("C"));
                Self.a[0] = 1;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([AssignStmt(Id(a),[[StringLit(A)],[StringLit(B)],[StringLit(C)]]),AssignStmt(ArrayCell(FieldAccess(Self(),Id(a)),[IntLit(0)]),IntLit(1))]))])])"
        self.assertTrue(TestAST.test(input, expect, 327))

    def test_multi_arr2(self):
        input = """Class Program {
            main() {
                Var arr: Array[Array[Int, 3], 3] = Array(Array("Volve", "22", "18"), 
                                                         Array("Saab", "5", "2"), 
                                                         Array("Land Rover", "17", "15"));
                Out.printStr(arr[1][1]);
                arr[1][2] = "33";
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(arr),ArrayType(3,ArrayType(3,IntType)),[[StringLit(Volve),StringLit(22),StringLit(18)],[StringLit(Saab),StringLit(5),StringLit(2)],[StringLit(Land Rover),StringLit(17),StringLit(15)]]),Call(Id(Out),Id(printStr),[ArrayCell(Id(arr),[IntLit(1),IntLit(1)])]),AssignStmt(ArrayCell(Id(arr),[IntLit(1),IntLit(2)]),StringLit(33))]))])])"
        self.assertTrue(TestAST.test(input, expect, 328))

    def test_multi_arr3(self):
        input = """Class Program {
            main() {
                Var arr: Array[Int, 3] = Array(1, 2 + 2, True);
                arr[3] = 3;
                Out.printStr(arr);
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(arr),ArrayType(3,IntType),[IntLit(1),BinaryOp(+,IntLit(2),IntLit(2)),BooleanLit(True)]),AssignStmt(ArrayCell(Id(arr),[IntLit(3)]),IntLit(3)),Call(Id(Out),Id(printStr),[Id(arr)])]))])])"
        self.assertTrue(TestAST.test(input, expect, 329))

    def test_var_decl_stmt1(self):
        input = """Class Program {
            main() {
                Val num: Array[Int, 1];
            }
            {
                Var num1: Array[Float, 2] = Array(1.5, 2.5);
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([ConstDecl(Id(num),ArrayType(1,IntType),None)])),AttributeDecl(Instance,VarDecl(Id(num1),ArrayType(2,FloatType),[FloatLit(1.5),FloatLit(2.5)]))])])"
        self.assertTrue(TestAST.test(input, expect, 330))

    def test_var_decl_stmt2(self):
        input = """Class Program {
            main() {
                Var num: Array[Float, 2] = Array(1.5, 2.e+5);
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(num),ArrayType(2,FloatType),[FloatLit(1.5),FloatLit(200000.0)])]))])])"
        self.assertTrue(TestAST.test(input, expect, 331))

    def test_var_decl_stmt3(self):
        input = """Class Shape {
            methodA(){
                Var a: Int;
            }
        }"""
        expect = "Program([ClassDecl(Id(Shape),[MethodDecl(Id(methodA),Instance,[],Block([VarDecl(Id(a),IntType)]))])])"
        self.assertTrue(TestAST.test(input, expect, 332))

    def test_var_decl_stmt4(self):
        input = """Class Program {
            main() {
                Var a: Int = -1;
                Val b: Float = -1.5;
                Var c: Boolean;
                c = True;
                c = !c;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(a),IntType,UnaryOp(-,IntLit(1))),ConstDecl(Id(b),FloatType,UnaryOp(-,FloatLit(1.5))),VarDecl(Id(c),BoolType),AssignStmt(Id(c),BooleanLit(True)),AssignStmt(Id(c),UnaryOp(!,Id(c)))]))])])"
        self.assertTrue(TestAST.test(input, expect, 333))

    def test_direct_func(self):
        input = """Class Program {
            getName() {
                Var b: Float = 7E-10;
            }
            main() {
                If (a >= b) {
                    Var a: Int = 0;
                    a = a + 3;
                }
                Elseif (b <= c) {
                    Self.getName(a >= b);
                }
                Else {
                    c = Self.a;
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(getName),Instance,[],Block([VarDecl(Id(b),FloatType,FloatLit(7e-10))])),MethodDecl(Id(main),Static,[],Block([If(BinaryOp(>=,Id(a),Id(b)),Block([VarDecl(Id(a),IntType,IntLit(0)),AssignStmt(Id(a),BinaryOp(+,Id(a),IntLit(3)))]),If(BinaryOp(<=,Id(b),Id(c)),Block([Call(Self(),Id(getName),[BinaryOp(>=,Id(a),Id(b))])]),Block([AssignStmt(Id(c),FieldAccess(Self(),Id(a)))])))]))])])"
        self.assertTrue(TestAST.test(input, expect, 334))

    def test_instance_access1(self):
        input = """Class Program {
            main() {
                Shape.width.val = 5;
                a = a::$c;
                a = Shape.width.val;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([AssignStmt(FieldAccess(FieldAccess(Id(Shape),Id(width)),Id(val)),IntLit(5)),AssignStmt(Id(a),FieldAccess(Id(a),Id($c))),AssignStmt(Id(a),FieldAccess(FieldAccess(Id(Shape),Id(width)),Id(val)))]))])])"
        self.assertTrue(TestAST.test(input, expect, 335))

    def test_instance_access2(self):
        input = """Class Program {
            main() {
                Shape.width = Self._width;
                Shape.area = Shape.length * Self._width;
                Var d: Int = Shape.area;
                Out.printInt(d);
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([AssignStmt(FieldAccess(Id(Shape),Id(width)),FieldAccess(Self(),Id(_width))),AssignStmt(FieldAccess(Id(Shape),Id(area)),BinaryOp(*,FieldAccess(Id(Shape),Id(length)),FieldAccess(Self(),Id(_width)))),VarDecl(Id(d),IntType,FieldAccess(Id(Shape),Id(area))),Call(Id(Out),Id(printInt),[Id(d)])]))])])"
        self.assertTrue(TestAST.test(input, expect, 336))

    def test_instance_access3(self):
        input = """Class Program {
            main() {
                a = (1 + 2).b;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([AssignStmt(Id(a),FieldAccess(BinaryOp(+,IntLit(1),IntLit(2)),Id(b)))]))])])"
        self.assertTrue(TestAST.test(input, expect, 337))

    def test_static_access2(self):
        input = """Class Program {
            main() {
                Shape.width = 10;
                a = Shape::$length;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([AssignStmt(FieldAccess(Id(Shape),Id(width)),IntLit(10)),AssignStmt(Id(a),FieldAccess(Id(Shape),Id($length)))]))])])"
        self.assertTrue(TestAST.test(input, expect, 338))

    def test_static_access3(self):
        input = """Class Program {
            foo() {
                Program.x.y.z();
                (x.y[1][2][3]).foo();
                Shape::$area.calculate();
                (Shape::$w.s[1][0b10]).eval();
            }
            main() {
                Shape::$width = 10;
                a = Shape::$area;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(foo),Instance,[],Block([Call(FieldAccess(FieldAccess(Id(Program),Id(x)),Id(y)),Id(z),[]),Call(ArrayCell(FieldAccess(Id(x),Id(y)),[IntLit(1),IntLit(2),IntLit(3)]),Id(foo),[]),Call(FieldAccess(Id(Shape),Id($area)),Id(calculate),[]),Call(ArrayCell(FieldAccess(FieldAccess(Id(Shape),Id($w)),Id(s)),[IntLit(1),IntLit(2)]),Id(eval),[])])),MethodDecl(Id(main),Static,[],Block([AssignStmt(FieldAccess(Id(Shape),Id($width)),IntLit(10)),AssignStmt(Id(a),FieldAccess(Id(Shape),Id($area)))]))])])"
        self.assertTrue(TestAST.test(input, expect, 339))

    def test_static_access4(self):
        input = """Class Example {
            Val $a: Int = 0;
            Var b: Int = 1;
            $getA(){
                Return New X().Y();
                ## Return $a; ##
            }
        }
        Class Program {
            main() {
                Var res1: Int = Example::$getA() + Example.b;
                Var res2: Int = Example.b + Example::$getA();
                Out.printInt(res1 + res2);
            }
        }"""
        expect = "Program([ClassDecl(Id(Example),[AttributeDecl(Static,ConstDecl(Id($a),IntType,IntLit(0))),AttributeDecl(Instance,VarDecl(Id(b),IntType,IntLit(1))),MethodDecl(Id($getA),Static,[],Block([Return(CallExpr(NewExpr(Id(X),[]),Id(Y),[]))]))]),ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(res1),IntType,BinaryOp(+,CallExpr(Id(Example),Id($getA),[]),FieldAccess(Id(Example),Id(b)))),VarDecl(Id(res2),IntType,BinaryOp(+,FieldAccess(Id(Example),Id(b)),CallExpr(Id(Example),Id($getA),[]))),Call(Id(Out),Id(printInt),[BinaryOp(+,Id(res1),Id(res2))])]))])])"
        self.assertTrue(TestAST.test(input, expect, 340))

    def test_static_access5(self):
        input = """Class Program {
            Var $a: String = "Hello World";
            main() {
                Var b: Int = 100000000;
                b.c.d = Program::$a() + 1;
                Return (b - Program::$a + Self.what - Program::$a());
            }
        }
        """
        expect = "Program([ClassDecl(Id(Program),[AttributeDecl(Static,VarDecl(Id($a),StringType,StringLit(Hello World))),MethodDecl(Id(main),Static,[],Block([VarDecl(Id(b),IntType,IntLit(100000000)),AssignStmt(FieldAccess(FieldAccess(Id(b),Id(c)),Id(d)),BinaryOp(+,CallExpr(Id(Program),Id($a),[]),IntLit(1))),Return(BinaryOp(-,BinaryOp(+,BinaryOp(-,Id(b),FieldAccess(Id(Program),Id($a))),FieldAccess(Self(),Id(what))),CallExpr(Id(Program),Id($a),[])))]))])])"
        self.assertTrue(TestAST.test(input, expect, 341))

    def test_operator1(self):
        input = """Class Program {
            main() {
                a = g != ((b * c / d % e) > f);
                b = ((abc +. def) ==. ghi).upper();
                c = 1 || True && False;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([AssignStmt(Id(a),BinaryOp(!=,Id(g),BinaryOp(>,BinaryOp(%,BinaryOp(/,BinaryOp(*,Id(b),Id(c)),Id(d)),Id(e)),Id(f)))),AssignStmt(Id(b),CallExpr(BinaryOp(==.,BinaryOp(+.,Id(abc),Id(def)),Id(ghi)),Id(upper),[])),AssignStmt(Id(c),BinaryOp(&&,BinaryOp(||,IntLit(1),BooleanLit(True)),BooleanLit(False)))]))])])"
        self.assertTrue(TestAST.test(input, expect, 342))

    def test_operator2(self):
        input = """Class Program {
            main() {
                a = -1 + -2 + -3;
                b = str1 +. str2.str3;
                c = !True;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([AssignStmt(Id(a),BinaryOp(+,BinaryOp(+,UnaryOp(-,IntLit(1)),UnaryOp(-,IntLit(2))),UnaryOp(-,IntLit(3)))),AssignStmt(Id(b),BinaryOp(+.,Id(str1),FieldAccess(Id(str2),Id(str3)))),AssignStmt(Id(c),UnaryOp(!,BooleanLit(True)))]))])])"
        self.assertTrue(TestAST.test(input, expect, 343))

    def test_operator3(self):
        input = """Class Program {
            main() {
                a = a[a.b] + c[a::$b];
                d = True && False && True || False ==. e;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([AssignStmt(Id(a),BinaryOp(+,ArrayCell(Id(a),[FieldAccess(Id(a),Id(b))]),ArrayCell(Id(c),[FieldAccess(Id(a),Id($b))]))),AssignStmt(Id(d),BinaryOp(==.,BinaryOp(||,BinaryOp(&&,BinaryOp(&&,BooleanLit(True),BooleanLit(False)),BooleanLit(True)),BooleanLit(False)),Id(e)))]))])])"
        self.assertTrue(TestAST.test(input, expect, 344))

    def test_operator4(self):
        input = """Class Program {
            Var a: Float = a.b().c;
        }"""
        expect = "Program([ClassDecl(Id(Program),[AttributeDecl(Instance,VarDecl(Id(a),FloatType,FieldAccess(CallExpr(Id(a),Id(b),[]),Id(c))))])])"
        self.assertTrue(TestAST.test(input, expect, 345))

    def test_operator5(self):
        input = """Class Program {
            Var $a: String = a::$b.c();
        }"""
        expect = "Program([ClassDecl(Id(Program),[AttributeDecl(Static,VarDecl(Id($a),StringType,CallExpr(FieldAccess(Id(a),Id($b)),Id(c),[])))])])"
        self.assertTrue(TestAST.test(input, expect, 346))

    def test_operator6(self):
        input = """Class Program {
            main() {
                _New::$abc();
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([Call(Id(_New),Id($abc),[])]))])])"
        self.assertTrue(TestAST.test(input, expect, 347))

    def test_operator7(self):
        input = """Class Program {
            main() {
                a = _New::$abc;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([AssignStmt(Id(a),FieldAccess(Id(_New),Id($abc)))]))])])"
        self.assertTrue(TestAST.test(input, expect, 348))

    def test_operator8(self):
        input = """Class Program {
            main() {
                Val a : Int = a[1] + b[2]; 
                a = New X();
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([ConstDecl(Id(a),IntType,BinaryOp(+,ArrayCell(Id(a),[IntLit(1)]),ArrayCell(Id(b),[IntLit(2)]))),AssignStmt(Id(a),NewExpr(Id(X),[]))]))])])"
        self.assertTrue(TestAST.test(input, expect, 349))

    def test_operator9(self):
        input = """Class Program {
            main() {
                a = New b().c;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([AssignStmt(Id(a),FieldAccess(NewExpr(Id(b),[]),Id(c)))]))])])"
        self.assertTrue(TestAST.test(input, expect, 350))

    def test_operator10(self):
        input = """Class Shape {
            Var length, width: Int;
            Constructor(_length, _width: Int){
                Self.length = _length;
                Self.width = _width;
            }
        }
        Class Program {
            main() {
                Var obj1: Shape = New Shape(1, 4);
                Val obj2: Shape;
            }
        }"""
        expect = "Program([ClassDecl(Id(Shape),[AttributeDecl(Instance,VarDecl(Id(length),IntType)),AttributeDecl(Instance,VarDecl(Id(width),IntType)),MethodDecl(Id(Constructor),Instance,[param(Id(_length),IntType),param(Id(_width),IntType)],Block([AssignStmt(FieldAccess(Self(),Id(length)),Id(_length)),AssignStmt(FieldAccess(Self(),Id(width)),Id(_width))]))]),ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(obj1),ClassType(Id(Shape)),NewExpr(Id(Shape),[IntLit(1),IntLit(4)])),ConstDecl(Id(obj2),ClassType(Id(Shape)),NullLiteral())]))])])"
        self.assertTrue(TestAST.test(input, expect, 351))

    def test_assign_stmt1(self):
        input = """Class Program {
            Var $a: Array[Int, 3] = Array(1, 2, 3);
            main(){
                a[1] = 4;
                Var b: Int = 10;
                Val c: Float = 1_234.567;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[AttributeDecl(Static,VarDecl(Id($a),ArrayType(3,IntType),[IntLit(1),IntLit(2),IntLit(3)])),MethodDecl(Id(main),Static,[],Block([AssignStmt(ArrayCell(Id(a),[IntLit(1)]),IntLit(4)),VarDecl(Id(b),IntType,IntLit(10)),ConstDecl(Id(c),FloatType,FloatLit(1234.567))]))])])"
        self.assertTrue(TestAST.test(input, expect, 352))

    def test_assign_stmt2(self):
        input = """Class Program {
            main() {
                _123::$_456 = 1 + 2;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([AssignStmt(FieldAccess(Id(_123),Id($_456)),BinaryOp(+,IntLit(1),IntLit(2)))]))])])"
        self.assertTrue(TestAST.test(input, expect, 353))

    def test_assign_stmt3(self):
        input = """Class Program {
            main() {
                a::$b.c(e).f = a::$b.c() - a.b().c;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([AssignStmt(FieldAccess(CallExpr(FieldAccess(Id(a),Id($b)),Id(c),[Id(e)]),Id(f)),BinaryOp(-,CallExpr(FieldAccess(Id(a),Id($b)),Id(c),[]),FieldAccess(CallExpr(Id(a),Id(b),[]),Id(c))))]))])])"
        self.assertTrue(TestAST.test(input, expect, 354))

    def test_assign_stmt4(self):
        input = """Class Shape {
            $methodA(){
                Return Shape::$A;
            }
        }
        Class Program {
            main() {
                Var a: Int = Shape::$methodA();
                Out.printInt(a);
            }
        }"""
        expect = "Program([ClassDecl(Id(Shape),[MethodDecl(Id($methodA),Static,[],Block([Return(FieldAccess(Id(Shape),Id($A)))]))]),ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(a),IntType,CallExpr(Id(Shape),Id($methodA),[])),Call(Id(Out),Id(printInt),[Id(a)])]))])])"
        self.assertTrue(TestAST.test(input, expect, 355))

    def test_assign_stmt5(self):
        input = """Class _program {
            Var $a: Int = 0b10;
            $methodA() {
                Return _program::$a;
            }
        }
        Class Program {
            Var $c: _program;
            main() {
                Var b: Int;
                b = _program::$methodA();
                Out.printInt(b);
            }
        }"""
        expect = "Program([ClassDecl(Id(_program),[AttributeDecl(Static,VarDecl(Id($a),IntType,IntLit(2))),MethodDecl(Id($methodA),Static,[],Block([Return(FieldAccess(Id(_program),Id($a)))]))]),ClassDecl(Id(Program),[AttributeDecl(Static,VarDecl(Id($c),ClassType(Id(_program)),NullLiteral())),MethodDecl(Id(main),Static,[],Block([VarDecl(Id(b),IntType),AssignStmt(Id(b),CallExpr(Id(_program),Id($methodA),[])),Call(Id(Out),Id(printInt),[Id(b)])]))])])"
        self.assertTrue(TestAST.test(input, expect, 356))

    def test_assign_stmt7(self):
        input = """Class Program {
            main() {
                a = _1a2b3c::$d();
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([AssignStmt(Id(a),CallExpr(Id(_1a2b3c),Id($d),[]))]))])])"
        self.assertTrue(TestAST.test(input, expect, 357))

    def test_if_stmt1(self):
        input = """Class Program {
            Var a, b: Int;
            main(){
                If ((a > 0) && (b > 0)) {
                    ## Do Something ##
                    Out.printLn("Hello");
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[AttributeDecl(Instance,VarDecl(Id(a),IntType)),AttributeDecl(Instance,VarDecl(Id(b),IntType)),MethodDecl(Id(main),Static,[],Block([If(BinaryOp(&&,BinaryOp(>,Id(a),IntLit(0)),BinaryOp(>,Id(b),IntLit(0))),Block([Call(Id(Out),Id(printLn),[StringLit(Hello)])]))]))])])"
        self.assertTrue(TestAST.test(input, expect, 358))

    def test_if_stmt2(self):
        input = """Class Program {
            main() {
                Var a, b: Int = 1, 2;
                If (a < b) {
                    Out.printLn("a is smaller than b");
                }
                Else {
                    Out.printLn("a is not smaller than b");
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(a),IntType,IntLit(1)),VarDecl(Id(b),IntType,IntLit(2)),If(BinaryOp(<,Id(a),Id(b)),Block([Call(Id(Out),Id(printLn),[StringLit(a is smaller than b)])]),Block([Call(Id(Out),Id(printLn),[StringLit(a is not smaller than b)])]))]))])])"
        self.assertTrue(TestAST.test(input, expect, 359))

    def test_if_stmt3(self):
        input = """Class Program {
            main() {
                Var a: Int = 1;
                Var b: Float = 2.0;
                If (a < b) {
                    Out.printLn("a is smaller than b");
                }
                Elseif (a == b) {
                    Out.printLn("a is equal to b");
                }
                Else {
                    Out.printLn("a is greater than b");
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(a),IntType,IntLit(1)),VarDecl(Id(b),FloatType,FloatLit(2.0)),If(BinaryOp(<,Id(a),Id(b)),Block([Call(Id(Out),Id(printLn),[StringLit(a is smaller than b)])]),If(BinaryOp(==,Id(a),Id(b)),Block([Call(Id(Out),Id(printLn),[StringLit(a is equal to b)])]),Block([Call(Id(Out),Id(printLn),[StringLit(a is greater than b)])])))]))])])"
        self.assertTrue(TestAST.test(input, expect, 360))

    def test_if_stmt4(self):
        input = """Class Program {
            main() {
                If ((a > b) && (b > c)) {
                    Out.printLn("1");
                }
                If ((a > b) && (b < c)) {
                    Out.printLn("2");
                }
                If ((a < b) && (b > c)) {
                    Out.printLn("3");
                }
                If ((a < b) && (b < c)) {
                    Out.printLn("4");
                }
                Else {
                    Out.printLn("5");
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([If(BinaryOp(&&,BinaryOp(>,Id(a),Id(b)),BinaryOp(>,Id(b),Id(c))),Block([Call(Id(Out),Id(printLn),[StringLit(1)])])),If(BinaryOp(&&,BinaryOp(>,Id(a),Id(b)),BinaryOp(<,Id(b),Id(c))),Block([Call(Id(Out),Id(printLn),[StringLit(2)])])),If(BinaryOp(&&,BinaryOp(<,Id(a),Id(b)),BinaryOp(>,Id(b),Id(c))),Block([Call(Id(Out),Id(printLn),[StringLit(3)])])),If(BinaryOp(&&,BinaryOp(<,Id(a),Id(b)),BinaryOp(<,Id(b),Id(c))),Block([Call(Id(Out),Id(printLn),[StringLit(4)])]),Block([Call(Id(Out),Id(printLn),[StringLit(5)])]))]))])])"
        self.assertTrue(TestAST.test(input, expect, 361))

    def test_if_stmt5(self):
        input = """Class Program {
            main() {
                If (a == 1) {
                    System.HelloWorld();
                }
                Else {
                    System.HelloVietNam();
                }
                Return;
            }
        }
        """
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([If(BinaryOp(==,Id(a),IntLit(1)),Block([Call(Id(System),Id(HelloWorld),[])]),Block([Call(Id(System),Id(HelloVietNam),[])])),Return()]))])])"
        self.assertTrue(TestAST.test(input, expect, 362))

    def test_foreach_stmt1(self):
        input = """Class Program {
            main() {
                Foreach (i In 1 .. 100 By 2) {
                    Out.printInt(i);
                    If (i % 2 == 0) {
                        Break;
                    }
                    Elseif (i % 3 == 1) {
                        Continue;
                    }
                }
                Foreach (x In 5 .. 2) {
                    Out.printInt(arr[x]);
                    If (x % 5 == 0) {
                        Return Program::$a;
                    }
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(Id(i),IntLit(1),IntLit(100),IntLit(2),Block([Call(Id(Out),Id(printInt),[Id(i)]),If(BinaryOp(==,BinaryOp(%,Id(i),IntLit(2)),IntLit(0)),Block([Break]),If(BinaryOp(==,BinaryOp(%,Id(i),IntLit(3)),IntLit(1)),Block([Continue])))])]),For(Id(x),IntLit(5),IntLit(2),IntLit(1),Block([Call(Id(Out),Id(printInt),[ArrayCell(Id(arr),[Id(x)])]),If(BinaryOp(==,BinaryOp(%,Id(x),IntLit(5)),IntLit(0)),Block([Return(FieldAccess(Id(Program),Id($a)))]))])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 363))

    def test_foreach_stmt2(self):
        input = """Class Program {
            main() {
                Foreach(Self.i In n-100 .. n+0b1 By 0xAF) {
                    Out.printLn(0X123ABC);
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(FieldAccess(Self(),Id(i)),BinaryOp(-,Id(n),IntLit(100)),BinaryOp(+,Id(n),IntLit(1)),IntLit(175),Block([Call(Id(Out),Id(printLn),[IntLit(1194684)])])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 364))

    def test_foreach_stmt3(self):
        input = """Class Program {
            main() {
                Foreach(i In True .. False By a[0]) {
                    a[1] = i;
                    Out.printInt(a[i]);
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(Id(i),BooleanLit(True),BooleanLit(False),ArrayCell(Id(a),[IntLit(0)]),Block([AssignStmt(ArrayCell(Id(a),[IntLit(1)]),Id(i)),Call(Id(Out),Id(printInt),[ArrayCell(Id(a),[Id(i)])])])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 365))

    def test_foreach_stmt4(self):
        input = """Class Program {
            main() {
                Foreach(x In 100 .. 1 By True) {
                    a[i] = x;
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(Id(x),IntLit(100),IntLit(1),BooleanLit(True),Block([AssignStmt(ArrayCell(Id(a),[Id(i)]),Id(x))])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 366))

    def test_foreach_stmt5(self):
        input = """Class Program {
            main() {
                Foreach(i In a .. b By c) {
                    Out.printLn(a);
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(Id(i),Id(a),Id(b),Id(c),Block([Call(Id(Out),Id(printLn),[Id(a)])])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 367))

    def test_foreach_stmt6(self):
        input = """Class Program {
            main() {
                Foreach (i In 1 .. 10 By 2) {
                    Out.printInt(i);
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(Id(i),IntLit(1),IntLit(10),IntLit(2),Block([Call(Id(Out),Id(printInt),[Id(i)])])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 368))

    def test_break_stmt1(self):
        input = """Class Program {
            main() {
                Break;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([Break]))])])"
        self.assertTrue(TestAST.test(input, expect, 369))

    def test_break_stmt2(self):
        input = """Class Program {
            main() {
                Foreach(i In 1 .. 100 By 101) {
                    If (i == 5) {
                        Break;
                    }
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(Id(i),IntLit(1),IntLit(100),IntLit(101),Block([If(BinaryOp(==,Id(i),IntLit(5)),Block([Break]))])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 370))

    def test_continue_stmt1(self):
        input = """Class Program {
            main() {
                Continue;
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([Continue]))])])"
        self.assertTrue(TestAST.test(input, expect, 371))

    def test_continue_stmt2(self):
        input = """Class Program {
            main() {
                Foreach(x In 5 .. 2) {
                    If (x == 3) {
                        Continue;
                    }
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(Id(x),IntLit(5),IntLit(2),IntLit(1),Block([If(BinaryOp(==,Id(x),IntLit(3)),Block([Continue]))])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 372))

    def test_method_invocation_stmt1(self):
        input = """Class Program {
            main() {
                Shape::$getNumOfShape();
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([Call(Id(Shape),Id($getNumOfShape),[])]))])])"
        self.assertTrue(TestAST.test(input, expect, 373))

    def test_scalar_var1(self):
        input = """Class Program {
            main() {
                Foreach (Self.func In 1 .. 10) {
                    Out.println("abc");
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(FieldAccess(Self(),Id(func)),IntLit(1),IntLit(10),IntLit(1),Block([Call(Id(Out),Id(println),[StringLit(abc)])])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 374))

    def test_scalar_var2(self):
        input = """Class Program {
            main() {
                Foreach (a._val In 1 .. 10) {
                    Out.println("abc");
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(FieldAccess(Id(a),Id(_val)),IntLit(1),IntLit(10),IntLit(1),Block([Call(Id(Out),Id(println),[StringLit(abc)])])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 375))

    def test_scalar_var3(self):
        input = """Class Program {
            main() {
                Foreach(Self.a.b In 1 .. 10 By 2) {
                    a = Self.a.b._val;
                    b = Program.d;
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(FieldAccess(FieldAccess(Self(),Id(a)),Id(b)),IntLit(1),IntLit(10),IntLit(2),Block([AssignStmt(Id(a),FieldAccess(FieldAccess(FieldAccess(Self(),Id(a)),Id(b)),Id(_val))),AssignStmt(Id(b),FieldAccess(Id(Program),Id(d)))])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 376))

    def test_scalar_var4(self):
        input = """Class Program {
            main() {
                Foreach (Self.a.b._val In 1 .. 10) {
                    Out.println("abc");
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(FieldAccess(FieldAccess(FieldAccess(Self(),Id(a)),Id(b)),Id(_val)),IntLit(1),IntLit(10),IntLit(1),Block([Call(Id(Out),Id(println),[StringLit(abc)])])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 377))

    def test_scalar_var5(self):
        input = """Class Program {
            main() {
                Foreach (Self.func().b._val In 1 .. 10 By 3) {
                    Out.println("abc");
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(FieldAccess(FieldAccess(CallExpr(Self(),Id(func),[]),Id(b)),Id(_val)),IntLit(1),IntLit(10),IntLit(3),Block([Call(Id(Out),Id(println),[StringLit(abc)])])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 378))

    def test_scalar_var6(self):
        input = """Class Program {
            main() {
                Foreach (a::$b In 1 .. 10) {
                    Out.println("abc");
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(FieldAccess(Id(a),Id($b)),IntLit(1),IntLit(10),IntLit(1),Block([Call(Id(Out),Id(println),[StringLit(abc)])])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 379))

    def test_scalar_var7(self):
        input = """Class Program {
            main() {
                Foreach (_0123::$a In 1 .. 10 By 2) {
                    Out.printLn("abc");
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(FieldAccess(Id(_0123),Id($a)),IntLit(1),IntLit(10),IntLit(2),Block([Call(Id(Out),Id(printLn),[StringLit(abc)])])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 380))

    def test_scalar_var8(self):
        input = """Class Program {
            main() {
                Foreach (Program::$a.b._val In 1 .. 10) {
                    Out.println("abc");
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(FieldAccess(FieldAccess(FieldAccess(Id(Program),Id($a)),Id(b)),Id(_val)),IntLit(1),IntLit(10),IntLit(1),Block([Call(Id(Out),Id(println),[StringLit(abc)])])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 381))

    def test_scalar_var9(self):
        input = """Class Program {
            main() {
                Foreach (a::$func().b._val In 1 .. 10) {
                    Out.println("abc");
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(FieldAccess(FieldAccess(CallExpr(Id(a),Id($func),[]),Id(b)),Id(_val)),IntLit(1),IntLit(10),IntLit(1),Block([Call(Id(Out),Id(println),[StringLit(abc)])])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 382))

    def test_scalar_var10(self):
        input = """Class Program {
            main() {
                Foreach (Program::$a(_1)._val In 1 .. 10) {
                    Out.printLn("abc");
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(FieldAccess(CallExpr(Id(Program),Id($a),[Id(_1)]),Id(_val)),IntLit(1),IntLit(10),IntLit(1),Block([Call(Id(Out),Id(printLn),[StringLit(abc)])])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 383))

    def test_scalar_var11(self):
        input = """Class Program {
            main() {
                Foreach (Program::$_val In 1 .. 10) {
                    Out.printLn("abc");
                }
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([For(FieldAccess(Id(Program),Id($_val)),IntLit(1),IntLit(10),IntLit(1),Block([Call(Id(Out),Id(printLn),[StringLit(abc)])])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 384))

    def test_simple_program1(self):
        input = """Class IOString {
            __init__() {
                Self.s = "";
            }
            getString() {
                Self.s = System.str(System.input());
            }
            printString() {
                Out.print(s.upper());
            }
        }
        Class Program {
            main() {
                Var strObj: String = New IOString();
                strObj.getString();
                strObj.printString();
            }
        }"""
        expect = "Program([ClassDecl(Id(IOString),[MethodDecl(Id(__init__),Instance,[],Block([AssignStmt(FieldAccess(Self(),Id(s)),StringLit())])),MethodDecl(Id(getString),Instance,[],Block([AssignStmt(FieldAccess(Self(),Id(s)),CallExpr(Id(System),Id(str),[CallExpr(Id(System),Id(input),[])]))])),MethodDecl(Id(printString),Instance,[],Block([Call(Id(Out),Id(print),[CallExpr(Id(s),Id(upper),[])])]))]),ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(strObj),StringType,NewExpr(Id(IOString),[])),Call(Id(strObj),Id(getString),[]),Call(Id(strObj),Id(printString),[])]))])])"
        self.assertTrue(TestAST.test(input, expect, 385))

    def test_simple_program2(self):
        input = """Class Program {
            main() {
                Var c, h: Int = 50, 30;
                Var d: Int = Math.int(System.input("Enter D: "));
                Var Q: Int = Math.int(2 * c * d / h);
                Out.print(Math.round(Math.sqrt(Q)));
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(c),IntType,IntLit(50)),VarDecl(Id(h),IntType,IntLit(30)),VarDecl(Id(d),IntType,CallExpr(Id(Math),Id(int),[CallExpr(Id(System),Id(input),[StringLit(Enter D: )])])),VarDecl(Id(Q),IntType,CallExpr(Id(Math),Id(int),[BinaryOp(/,BinaryOp(*,BinaryOp(*,IntLit(2),Id(c)),Id(d)),Id(h))])),Call(Id(Out),Id(print),[CallExpr(Id(Math),Id(round),[CallExpr(Id(Math),Id(sqrt),[Id(Q)])])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 386))
    
    def test_simple_program3(self):
        input = """Class Program {
            main() {
                Var input_str: String = System.input();
                Var dimensions: Array[Int, 2];
                Foreach(x In 0 .. input_str.length()) {
                    dimensions[x] = input_str[x];
                }
                Var rowNum, colNum: Int = dimensions[0], dimensions[1];
                Var multilist: Array[Array[Int, 1], 1];
                Foreach(row In 0 .. rowNum) {
                    Foreach(col In 0 .. colNum) {
                        multilist[row][col] = row * col;
                    }
                }
                Out.print(multilist);
            }
        }"""
        expect = "Program([ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(input_str),StringType,CallExpr(Id(System),Id(input),[])),VarDecl(Id(dimensions),ArrayType(2,IntType)),For(Id(x),IntLit(0),CallExpr(Id(input_str),Id(length),[]),IntLit(1),Block([AssignStmt(ArrayCell(Id(dimensions),[Id(x)]),ArrayCell(Id(input_str),[Id(x)]))])]),VarDecl(Id(rowNum),IntType,ArrayCell(Id(dimensions),[IntLit(0)])),VarDecl(Id(colNum),IntType,ArrayCell(Id(dimensions),[IntLit(1)])),VarDecl(Id(multilist),ArrayType(1,ArrayType(1,IntType))),For(Id(row),IntLit(0),Id(rowNum),IntLit(1),Block([For(Id(col),IntLit(0),Id(colNum),IntLit(1),Block([AssignStmt(ArrayCell(Id(multilist),[Id(row),Id(col)]),BinaryOp(*,Id(row),Id(col)))])])])]),Call(Id(Out),Id(print),[Id(multilist)])]))])])"
        self.assertTrue(TestAST.test(input, expect, 387))

    def test_simple_program4(self):
        input = """Class Solution {
            leastBricks(wall: Array[Array[Int, 10], 10]) {
                Var m: Array[Array[Int, 10], 10];
                Var res, n: Int = wall.size(), wall.size();
                Foreach(row In 0 .. n) {
                    Var curr_width: Int = 0;
                    Foreach(i In 0 .. row.size()-1) {
                        curr_width = curr_width + row[i];
                        res = Math.min(res, n - (m[curr_width] + 1));
                    }
                }
                Return res;
            }
        }"""
        expect = "Program([ClassDecl(Id(Solution),[MethodDecl(Id(leastBricks),Instance,[param(Id(wall),ArrayType(10,ArrayType(10,IntType)))],Block([VarDecl(Id(m),ArrayType(10,ArrayType(10,IntType))),VarDecl(Id(res),IntType,CallExpr(Id(wall),Id(size),[])),VarDecl(Id(n),IntType,CallExpr(Id(wall),Id(size),[])),For(Id(row),IntLit(0),Id(n),IntLit(1),Block([VarDecl(Id(curr_width),IntType,IntLit(0)),For(Id(i),IntLit(0),BinaryOp(-,CallExpr(Id(row),Id(size),[]),IntLit(1)),IntLit(1),Block([AssignStmt(Id(curr_width),BinaryOp(+,Id(curr_width),ArrayCell(Id(row),[Id(i)]))),AssignStmt(Id(res),CallExpr(Id(Math),Id(min),[Id(res),BinaryOp(-,Id(n),BinaryOp(+,ArrayCell(Id(m),[Id(curr_width)]),IntLit(1)))]))])])])]),Return(Id(res))]))])])"
        self.assertTrue(TestAST.test(input, expect, 388))

    def test_simple_program5(self):
        input = """Class Solution {
            fib(n: Int) {
                If (n == 0) {
                    Return 0;
                }
                If (n == 1) {
                    Return 1;
                }
                Return Self.fib(n-1) + Self.fib(n-2);
            }
        }"""
        expect = "Program([ClassDecl(Id(Solution),[MethodDecl(Id(fib),Instance,[param(Id(n),IntType)],Block([If(BinaryOp(==,Id(n),IntLit(0)),Block([Return(IntLit(0))])),If(BinaryOp(==,Id(n),IntLit(1)),Block([Return(IntLit(1))])),Return(BinaryOp(+,CallExpr(Self(),Id(fib),[BinaryOp(-,Id(n),IntLit(1))]),CallExpr(Self(),Id(fib),[BinaryOp(-,Id(n),IntLit(2))])))]))])])"
        self.assertTrue(TestAST.test(input, expect, 389))

    def test_simple_program6(self):
        input = """Class Solution {
            fizzBuzz(n: Int) {
                Var ans: Array[String, 10];
                Foreach(i In 1 .. n) {
                    If (i % 15 == 0) {
                        ans.push_back("FizzBuzz");
                    }
                    Elseif (i % 3 == 0) {
                        ans.push_back("Fizz");
                    }
                    Elseif (i % 5 == 0) {
                        ans.push_back("Buzz");
                    }
                    Else {
                        ans.push_back(System.to_string(i));
                    }
                }
                Return ans;
            }
        }"""
        expect = "Program([ClassDecl(Id(Solution),[MethodDecl(Id(fizzBuzz),Instance,[param(Id(n),IntType)],Block([VarDecl(Id(ans),ArrayType(10,StringType)),For(Id(i),IntLit(1),Id(n),IntLit(1),Block([If(BinaryOp(==,BinaryOp(%,Id(i),IntLit(15)),IntLit(0)),Block([Call(Id(ans),Id(push_back),[StringLit(FizzBuzz)])]),If(BinaryOp(==,BinaryOp(%,Id(i),IntLit(3)),IntLit(0)),Block([Call(Id(ans),Id(push_back),[StringLit(Fizz)])]),If(BinaryOp(==,BinaryOp(%,Id(i),IntLit(5)),IntLit(0)),Block([Call(Id(ans),Id(push_back),[StringLit(Buzz)])]),Block([Call(Id(ans),Id(push_back),[CallExpr(Id(System),Id(to_string),[Id(i)])])]))))])]),Return(Id(ans))]))])])"
        self.assertTrue(TestAST.test(input, expect, 390))

    def test_simple_program7(self):
        input = """Class Solution {
            candy(ratings: Array[Int, 10]) {
                Var n, res: Int = rating.size(), 0;
                Var count: Array[Int, 10];
                Foreach(i In 0 .. n) {
                    count[i] = 1;
                }
                Foreach(i In 1 .. n){
                    If (ratings[i] > ratings[(i-1)]) {
                        count[i] = count[(i-1)] + 1;
                    }
                }
                Foreach(i In n-2 .. 0 By -1) {
                    If ((ratings[i] > ratings[(i+1)]) && (count[i] <= count[(i+1)])) {
                        count[i] = count[(i+1)] + 1;
                    }
                }
                Foreach(i In 0 .. n) {
                    result = result + count[i];
                }
                Return result;
            }
        }"""
        expect = "Program([ClassDecl(Id(Solution),[MethodDecl(Id(candy),Instance,[param(Id(ratings),ArrayType(10,IntType))],Block([VarDecl(Id(n),IntType,CallExpr(Id(rating),Id(size),[])),VarDecl(Id(res),IntType,IntLit(0)),VarDecl(Id(count),ArrayType(10,IntType)),For(Id(i),IntLit(0),Id(n),IntLit(1),Block([AssignStmt(ArrayCell(Id(count),[Id(i)]),IntLit(1))])]),For(Id(i),IntLit(1),Id(n),IntLit(1),Block([If(BinaryOp(>,ArrayCell(Id(ratings),[Id(i)]),ArrayCell(Id(ratings),[BinaryOp(-,Id(i),IntLit(1))])),Block([AssignStmt(ArrayCell(Id(count),[Id(i)]),BinaryOp(+,ArrayCell(Id(count),[BinaryOp(-,Id(i),IntLit(1))]),IntLit(1)))]))])]),For(Id(i),BinaryOp(-,Id(n),IntLit(2)),IntLit(0),UnaryOp(-,IntLit(1)),Block([If(BinaryOp(&&,BinaryOp(>,ArrayCell(Id(ratings),[Id(i)]),ArrayCell(Id(ratings),[BinaryOp(+,Id(i),IntLit(1))])),BinaryOp(<=,ArrayCell(Id(count),[Id(i)]),ArrayCell(Id(count),[BinaryOp(+,Id(i),IntLit(1))]))),Block([AssignStmt(ArrayCell(Id(count),[Id(i)]),BinaryOp(+,ArrayCell(Id(count),[BinaryOp(+,Id(i),IntLit(1))]),IntLit(1)))]))])]),For(Id(i),IntLit(0),Id(n),IntLit(1),Block([AssignStmt(Id(result),BinaryOp(+,Id(result),ArrayCell(Id(count),[Id(i)])))])]),Return(Id(result))]))])])"
        self.assertTrue(TestAST.test(input, expect, 391))

    def test_simple_program8(self):
        input = """Class Solution {
            breakPalindrome(palindrome: String) {
                Var res: String;
                If (palindrome.size() == 1) {
                    Return res;
                }
                Foreach (i In 0 .. palindrome.size()/2) {
                    If (palindrome[i] != "a") {
                        palindrome[i] = "a";
                        Return palindrome;
                    }
                }
                palindrome[palindrome.size() - 1] = "b";
                Return palindrome;
            }
        }"""
        expect = "Program([ClassDecl(Id(Solution),[MethodDecl(Id(breakPalindrome),Instance,[param(Id(palindrome),StringType)],Block([VarDecl(Id(res),StringType),If(BinaryOp(==,CallExpr(Id(palindrome),Id(size),[]),IntLit(1)),Block([Return(Id(res))])),For(Id(i),IntLit(0),BinaryOp(/,CallExpr(Id(palindrome),Id(size),[]),IntLit(2)),IntLit(1),Block([If(BinaryOp(!=,ArrayCell(Id(palindrome),[Id(i)]),StringLit(a)),Block([AssignStmt(ArrayCell(Id(palindrome),[Id(i)]),StringLit(a)),Return(Id(palindrome))]))])]),AssignStmt(ArrayCell(Id(palindrome),[BinaryOp(-,CallExpr(Id(palindrome),Id(size),[]),IntLit(1))]),StringLit(b)),Return(Id(palindrome))]))])])"
        self.assertTrue(TestAST.test(input, expect, 392))

    def test_simple_program9(self):
        input = """Class Program {
            Val a, b: Array[Int, 5];
            Var c: Array[String, 10_0];
            main() {
               a = 1;
               b = Array();
               c = Array("1", "2", "3");
               d = Array(Array(1, 2, 3), Array(4, 5, 6)) + Array(1, 2, 3);

               e = a + b;
               f = (a +. b) ==. c;
               g = f.callFunc() - g::$something(a, b);
               h = g::$somethingElse;
               i = g.someValue();

               j = "Something special";
               Return;
            }
        }
        """
        expect = "Program([ClassDecl(Id(Program),[AttributeDecl(Instance,ConstDecl(Id(a),ArrayType(5,IntType),None)),AttributeDecl(Instance,ConstDecl(Id(b),ArrayType(5,IntType),None)),AttributeDecl(Instance,VarDecl(Id(c),ArrayType(100,StringType))),MethodDecl(Id(main),Static,[],Block([AssignStmt(Id(a),IntLit(1)),AssignStmt(Id(b),[]),AssignStmt(Id(c),[StringLit(1),StringLit(2),StringLit(3)]),AssignStmt(Id(d),BinaryOp(+,[[IntLit(1),IntLit(2),IntLit(3)],[IntLit(4),IntLit(5),IntLit(6)]],[IntLit(1),IntLit(2),IntLit(3)])),AssignStmt(Id(e),BinaryOp(+,Id(a),Id(b))),AssignStmt(Id(f),BinaryOp(==.,BinaryOp(+.,Id(a),Id(b)),Id(c))),AssignStmt(Id(g),BinaryOp(-,CallExpr(Id(f),Id(callFunc),[]),CallExpr(Id(g),Id($something),[Id(a),Id(b)]))),AssignStmt(Id(h),FieldAccess(Id(g),Id($somethingElse))),AssignStmt(Id(i),CallExpr(Id(g),Id(someValue),[])),AssignStmt(Id(j),StringLit(Something special)),Return()]))])])"
        self.assertTrue(TestAST.test(input, expect, 393))

    def test_simple_program10(self):
        input = """Class _Program {
            Var $A: Array[Array[String, 3], 3];
            $getMethodA() {
                Return _Program::$A;
            }
            $setMethodA(_a: Array[Array[String, 3], 3]) {
                _Program::$A = _a;
            }
        }
        Class Program {
            main() {
                Var arr: Array[Array[String, 3], 3] = Array(Array("Volvo", "22", "18"), Array("Saab", "5", "2"), Array("Land Rover", "17", "15"));
                _Program::$setMethodA(arr);
                Out.printLn(_Program::$getMethodA());
            }
        }"""
        expect = "Program([ClassDecl(Id(_Program),[AttributeDecl(Static,VarDecl(Id($A),ArrayType(3,ArrayType(3,StringType)))),MethodDecl(Id($getMethodA),Static,[],Block([Return(FieldAccess(Id(_Program),Id($A)))])),MethodDecl(Id($setMethodA),Static,[param(Id(_a),ArrayType(3,ArrayType(3,StringType)))],Block([AssignStmt(FieldAccess(Id(_Program),Id($A)),Id(_a))]))]),ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(arr),ArrayType(3,ArrayType(3,StringType)),[[StringLit(Volvo),StringLit(22),StringLit(18)],[StringLit(Saab),StringLit(5),StringLit(2)],[StringLit(Land Rover),StringLit(17),StringLit(15)]]),Call(Id(_Program),Id($setMethodA),[Id(arr)]),Call(Id(Out),Id(printLn),[CallExpr(Id(_Program),Id($getMethodA),[])])]))])])"
        self.assertTrue(TestAST.test(input, expect, 394))

    def test_simple_program11(self):
        input = """Class Solution {
            canCompleteCircuit(gas, cost: Array[Int, 10]) {
                Var totalTank, currentTank, result: Int = 0, 0, 0;
                Foreach(i In 0 .. gas.size()) {
                    totalTank = totalTank + gas[i] - cost[i];
                    currentTank = currentTank + gas[i] - cost[i];
                    If (currentTank < 0) {
                        currentTank = 0;
                        result = i + 1;
                    }
                }
                If (totalTank < 0) {
                    Return -1;
                }
                Return result;
            }
        }"""
        expect = "Program([ClassDecl(Id(Solution),[MethodDecl(Id(canCompleteCircuit),Instance,[param(Id(gas),ArrayType(10,IntType)),param(Id(cost),ArrayType(10,IntType))],Block([VarDecl(Id(totalTank),IntType,IntLit(0)),VarDecl(Id(currentTank),IntType,IntLit(0)),VarDecl(Id(result),IntType,IntLit(0)),For(Id(i),IntLit(0),CallExpr(Id(gas),Id(size),[]),IntLit(1),Block([AssignStmt(Id(totalTank),BinaryOp(-,BinaryOp(+,Id(totalTank),ArrayCell(Id(gas),[Id(i)])),ArrayCell(Id(cost),[Id(i)]))),AssignStmt(Id(currentTank),BinaryOp(-,BinaryOp(+,Id(currentTank),ArrayCell(Id(gas),[Id(i)])),ArrayCell(Id(cost),[Id(i)]))),If(BinaryOp(<,Id(currentTank),IntLit(0)),Block([AssignStmt(Id(currentTank),IntLit(0)),AssignStmt(Id(result),BinaryOp(+,Id(i),IntLit(1)))]))])]),If(BinaryOp(<,Id(totalTank),IntLit(0)),Block([Return(UnaryOp(-,IntLit(1)))])),Return(Id(result))]))])])"
        self.assertTrue(TestAST.test(input, expect, 395))
    
    def test_complex_program1(self):
        input = """Class Shape {
            Val $numOfShape: Int = 0;
            Val immutableAttribute: Int = 0;
            Var length, width: Int;

            $getNumOfShape() {
                Return Shape::$numOfShape;
            }
        }
        Class Rectangle: Shape {
            getArea() {
                Return Self.length * Self.width;
            }
        }
        Class Program {
            main() {
                Out.printInt(Shape::$numOfShape);
            }
        }
        """
        expect = "Program([ClassDecl(Id(Shape),[AttributeDecl(Static,ConstDecl(Id($numOfShape),IntType,IntLit(0))),AttributeDecl(Instance,ConstDecl(Id(immutableAttribute),IntType,IntLit(0))),AttributeDecl(Instance,VarDecl(Id(length),IntType)),AttributeDecl(Instance,VarDecl(Id(width),IntType)),MethodDecl(Id($getNumOfShape),Static,[],Block([Return(FieldAccess(Id(Shape),Id($numOfShape)))]))]),ClassDecl(Id(Rectangle),Id(Shape),[MethodDecl(Id(getArea),Instance,[],Block([Return(BinaryOp(*,FieldAccess(Self(),Id(length)),FieldAccess(Self(),Id(width))))]))]),ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([Call(Id(Out),Id(printInt),[FieldAccess(Id(Shape),Id($numOfShape))])]))])])"
        self.assertTrue(TestAST.test(input, expect, 396))

    def test_complex_program2(self):
        input = """Class Shape {
            Val $numOfShape: Int = 0;
            Val immutableAttribute: Int = 0;
            Var length, width: Int;

            $getNumOfShape() {
                Return Shape::$numOfShape;
            }
        }
        Class Rectangle: Shape {
            getArea() {
                Return Self.length * Self.width;
            }
        }
        Class Program {
            main() {
                Out.printInt(Shape::$numOfShape);
                Var r, s: Int;
                r = 2.0;
                Var a: Array[Int, 5];
                s = r * r * Self.myPI;
                a[0] = s;
            }
        }
        """
        expect = "Program([ClassDecl(Id(Shape),[AttributeDecl(Static,ConstDecl(Id($numOfShape),IntType,IntLit(0))),AttributeDecl(Instance,ConstDecl(Id(immutableAttribute),IntType,IntLit(0))),AttributeDecl(Instance,VarDecl(Id(length),IntType)),AttributeDecl(Instance,VarDecl(Id(width),IntType)),MethodDecl(Id($getNumOfShape),Static,[],Block([Return(FieldAccess(Id(Shape),Id($numOfShape)))]))]),ClassDecl(Id(Rectangle),Id(Shape),[MethodDecl(Id(getArea),Instance,[],Block([Return(BinaryOp(*,FieldAccess(Self(),Id(length)),FieldAccess(Self(),Id(width))))]))]),ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([Call(Id(Out),Id(printInt),[FieldAccess(Id(Shape),Id($numOfShape))]),VarDecl(Id(r),IntType),VarDecl(Id(s),IntType),AssignStmt(Id(r),FloatLit(2.0)),VarDecl(Id(a),ArrayType(5,IntType)),AssignStmt(Id(s),BinaryOp(*,BinaryOp(*,Id(r),Id(r)),FieldAccess(Self(),Id(myPI)))),AssignStmt(ArrayCell(Id(a),[IntLit(0)]),Id(s))]))])])"
        self.assertTrue(TestAST.test(input, expect, 397))

    def test_complex_program3(self):
        input = """Class Solution {
            threeSum(nums: Array[Int, 10]) {
                Math.sort(nums.begin(), nums.end());
                Var ans: Array[Int, 10];
                Foreach(i In 0 .. nums.size()) {
                    If ((i != 0) && (nums[i] == nums[(i-1)])) {
                        Continue;
                    }
                    Var sum, start, end: Int = (-1) * nums[i], i + 1, nums.size() - 1;
                    Foreach(j In start .. end) {
                        If (nums[start] + nums[end] == sum) {
                            Var vec: Array[Int, 10];
                            vec.push_back(nums[i]);
                            vec.push_back(nums[start]);
                            vec.push_back(nums[end]);
                            ans.push_back(vec);
                            If (nums[start] == nums[end]) {
                                Break;
                            }
                        }
                        Elseif (nums[start] + nums[end] < sum) {
                            start = start + 1;
                        }
                        Else {
                            end = end - 1;
                        }
                    }
                }
                Return ans;
            }
        }"""
        expect = "Program([ClassDecl(Id(Solution),[MethodDecl(Id(threeSum),Instance,[param(Id(nums),ArrayType(10,IntType))],Block([Call(Id(Math),Id(sort),[CallExpr(Id(nums),Id(begin),[]),CallExpr(Id(nums),Id(end),[])]),VarDecl(Id(ans),ArrayType(10,IntType)),For(Id(i),IntLit(0),CallExpr(Id(nums),Id(size),[]),IntLit(1),Block([If(BinaryOp(&&,BinaryOp(!=,Id(i),IntLit(0)),BinaryOp(==,ArrayCell(Id(nums),[Id(i)]),ArrayCell(Id(nums),[BinaryOp(-,Id(i),IntLit(1))]))),Block([Continue])),VarDecl(Id(sum),IntType,BinaryOp(*,UnaryOp(-,IntLit(1)),ArrayCell(Id(nums),[Id(i)]))),VarDecl(Id(start),IntType,BinaryOp(+,Id(i),IntLit(1))),VarDecl(Id(end),IntType,BinaryOp(-,CallExpr(Id(nums),Id(size),[]),IntLit(1))),For(Id(j),Id(start),Id(end),IntLit(1),Block([If(BinaryOp(==,BinaryOp(+,ArrayCell(Id(nums),[Id(start)]),ArrayCell(Id(nums),[Id(end)])),Id(sum)),Block([VarDecl(Id(vec),ArrayType(10,IntType)),Call(Id(vec),Id(push_back),[ArrayCell(Id(nums),[Id(i)])]),Call(Id(vec),Id(push_back),[ArrayCell(Id(nums),[Id(start)])]),Call(Id(vec),Id(push_back),[ArrayCell(Id(nums),[Id(end)])]),Call(Id(ans),Id(push_back),[Id(vec)]),If(BinaryOp(==,ArrayCell(Id(nums),[Id(start)]),ArrayCell(Id(nums),[Id(end)])),Block([Break]))]),If(BinaryOp(<,BinaryOp(+,ArrayCell(Id(nums),[Id(start)]),ArrayCell(Id(nums),[Id(end)])),Id(sum)),Block([AssignStmt(Id(start),BinaryOp(+,Id(start),IntLit(1)))]),Block([AssignStmt(Id(end),BinaryOp(-,Id(end),IntLit(1)))])))])])])]),Return(Id(ans))]))])])"
        self.assertTrue(TestAST.test(input, expect, 398))

    def test_complex_program4(self):
        input = """Class Shape {
            Val $numOfShape: Int = 0;
            Val immutableAttribute: Int = 0;
            Var length, width: Int;
            Var a : Array[Int, 3] = Array(1 + 1, 2, 3);

            $getNumOfShape() {
                Return Shape::$numOfShape;
            }
        }

        Class Program{
            main(){
                Var a : Int = 12;
                If (a + 1 == 9){
                    a = Self.Pi; 
                    Foreach(i In 1 .. 100 By 2){
                        a = a[(1 + 2 + 3)];
                        a = a.getShape();
                        Continue;
                    }
                    
                }
                Else{
                    a = a * 3 - 9; 
                }
            }
        }  
        """
        expect = "Program([ClassDecl(Id(Shape),[AttributeDecl(Static,ConstDecl(Id($numOfShape),IntType,IntLit(0))),AttributeDecl(Instance,ConstDecl(Id(immutableAttribute),IntType,IntLit(0))),AttributeDecl(Instance,VarDecl(Id(length),IntType)),AttributeDecl(Instance,VarDecl(Id(width),IntType)),AttributeDecl(Instance,VarDecl(Id(a),ArrayType(3,IntType),[BinaryOp(+,IntLit(1),IntLit(1)),IntLit(2),IntLit(3)])),MethodDecl(Id($getNumOfShape),Static,[],Block([Return(FieldAccess(Id(Shape),Id($numOfShape)))]))]),ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(a),IntType,IntLit(12)),If(BinaryOp(==,BinaryOp(+,Id(a),IntLit(1)),IntLit(9)),Block([AssignStmt(Id(a),FieldAccess(Self(),Id(Pi))),For(Id(i),IntLit(1),IntLit(100),IntLit(2),Block([AssignStmt(Id(a),ArrayCell(Id(a),[BinaryOp(+,BinaryOp(+,IntLit(1),IntLit(2)),IntLit(3))])),AssignStmt(Id(a),CallExpr(Id(a),Id(getShape),[])),Continue])])]),Block([AssignStmt(Id(a),BinaryOp(-,BinaryOp(*,Id(a),IntLit(3)),IntLit(9)))]))]))])])"
        self.assertTrue(TestAST.test(input, expect, 399))

    def test_complex_program5(self):
        input = """Class PrimeNumber {
            isPrimeNumber(n: Int) {
                Foreach(i In 2 .. n/2) {
                    If (n % i == 0) {
                        Return false;
                    }
                }
                Return true;
            }
        }
        Class Fibonacci {
            isFibonacci(n: Int) {
                Var a, b, Sum: Int = 0, 1, 0;
                Foreach(Sum In 0 .. n) {
                    Sum = a + b;
                    a = b;
                    b = Sum;
                    If (n == Sum) {
                        Return true;
                    }
                    Return false;
                }
            }
        }
        Class TriangleNumber{
            isTriangleNumber(n: Int) {
                Return (n * (n + 1)) / 2;
            }
        }
        Class Display {
            display(pR: Float) {
                If (pR < 0) {
                    pR = 0;
                }
                If (pR > 1) {
                    pR = 1;
                }
                pR = System.round(pR * 1000) / 1000;
                Out.print(pR);
            }
        }
        Class Program {
            main() {
                Var hp, d, s: Int = 0, 0, 0;
                Var P1, P2, f, pR: Float = 0, 0, 0, -1;
                If (System.readFile(hp, d, s)) {
                    If (PrimeNumber.isPrimeNumber(hp)) {
                        P1 = 1000;
                        P2 = (hp + s) % 1000;
                    }
                    Else {
                        P1 = hp;
                        P2 = (hp + d) % 100;
                    }
                }
                Var g: Float;
                If (d < 200 && !Fibonacci.isFibonacci(d + s)) {
                    f = 0;
                }
                Elseif (((d >= 200) && (d <= 800)) || (d < 200 && Fibonacci.isFibonacci(d + s))) {
                    If (s % 6 == 0) {
                        g = s/2;
                    }
                    Elseif (s % 6 == 1) {
                        g = 2 * s;
                    }
                    Elseif (s % 6 == 2) {
                        g = -Math.pow(s % 9, 3) / 5;
                    }
                    Elseif (s % 6 == 3) {
                        g = -Math.pow(s % 30, 2) + 3 * s;
                    }
                    Elseif (s % 6 == 4) {
                        g = -s;
                    }
                    Elseif (s % 6 == 5) {
                        g = -TriangleNumber.isTriangleNumber((s % 5) + 5);
                    }
                    f = 40 - Math.abs(d - 500) / 20 + g;
                }
                Elseif (d > 800) {
                    f = (-d * s) / 1000;
                }
                Var Bitten: Float;
                If ((d >= 200) && (d <= 300)) {
                    Bitten = (d + P1 + P2) / 1000;
                    If (Bitten > 0.8) {
                        pR = 0;
                    }
                }
                Else {
                    pR = (P1 + P2 * f) / (1000 + Math.abs(P2 * f));
                }
                Display.display(pR);
            }
        }
        """
        expect = "Program([ClassDecl(Id(PrimeNumber),[MethodDecl(Id(isPrimeNumber),Instance,[param(Id(n),IntType)],Block([For(Id(i),IntLit(2),BinaryOp(/,Id(n),IntLit(2)),IntLit(1),Block([If(BinaryOp(==,BinaryOp(%,Id(n),Id(i)),IntLit(0)),Block([Return(Id(false))]))])]),Return(Id(true))]))]),ClassDecl(Id(Fibonacci),[MethodDecl(Id(isFibonacci),Instance,[param(Id(n),IntType)],Block([VarDecl(Id(a),IntType,IntLit(0)),VarDecl(Id(b),IntType,IntLit(1)),VarDecl(Id(Sum),IntType,IntLit(0)),For(Id(Sum),IntLit(0),Id(n),IntLit(1),Block([AssignStmt(Id(Sum),BinaryOp(+,Id(a),Id(b))),AssignStmt(Id(a),Id(b)),AssignStmt(Id(b),Id(Sum)),If(BinaryOp(==,Id(n),Id(Sum)),Block([Return(Id(true))])),Return(Id(false))])])]))]),ClassDecl(Id(TriangleNumber),[MethodDecl(Id(isTriangleNumber),Instance,[param(Id(n),IntType)],Block([Return(BinaryOp(/,BinaryOp(*,Id(n),BinaryOp(+,Id(n),IntLit(1))),IntLit(2)))]))]),ClassDecl(Id(Display),[MethodDecl(Id(display),Instance,[param(Id(pR),FloatType)],Block([If(BinaryOp(<,Id(pR),IntLit(0)),Block([AssignStmt(Id(pR),IntLit(0))])),If(BinaryOp(>,Id(pR),IntLit(1)),Block([AssignStmt(Id(pR),IntLit(1))])),AssignStmt(Id(pR),BinaryOp(/,CallExpr(Id(System),Id(round),[BinaryOp(*,Id(pR),IntLit(1000))]),IntLit(1000))),Call(Id(Out),Id(print),[Id(pR)])]))]),ClassDecl(Id(Program),[MethodDecl(Id(main),Static,[],Block([VarDecl(Id(hp),IntType,IntLit(0)),VarDecl(Id(d),IntType,IntLit(0)),VarDecl(Id(s),IntType,IntLit(0)),VarDecl(Id(P1),FloatType,IntLit(0)),VarDecl(Id(P2),FloatType,IntLit(0)),VarDecl(Id(f),FloatType,IntLit(0)),VarDecl(Id(pR),FloatType,UnaryOp(-,IntLit(1))),If(CallExpr(Id(System),Id(readFile),[Id(hp),Id(d),Id(s)]),Block([If(CallExpr(Id(PrimeNumber),Id(isPrimeNumber),[Id(hp)]),Block([AssignStmt(Id(P1),IntLit(1000)),AssignStmt(Id(P2),BinaryOp(%,BinaryOp(+,Id(hp),Id(s)),IntLit(1000)))]),Block([AssignStmt(Id(P1),Id(hp)),AssignStmt(Id(P2),BinaryOp(%,BinaryOp(+,Id(hp),Id(d)),IntLit(100)))]))])),VarDecl(Id(g),FloatType),If(BinaryOp(<,Id(d),BinaryOp(&&,IntLit(200),UnaryOp(!,CallExpr(Id(Fibonacci),Id(isFibonacci),[BinaryOp(+,Id(d),Id(s))])))),Block([AssignStmt(Id(f),IntLit(0))]),If(BinaryOp(||,BinaryOp(&&,BinaryOp(>=,Id(d),IntLit(200)),BinaryOp(<=,Id(d),IntLit(800))),BinaryOp(<,Id(d),BinaryOp(&&,IntLit(200),CallExpr(Id(Fibonacci),Id(isFibonacci),[BinaryOp(+,Id(d),Id(s))])))),Block([If(BinaryOp(==,BinaryOp(%,Id(s),IntLit(6)),IntLit(0)),Block([AssignStmt(Id(g),BinaryOp(/,Id(s),IntLit(2)))]),If(BinaryOp(==,BinaryOp(%,Id(s),IntLit(6)),IntLit(1)),Block([AssignStmt(Id(g),BinaryOp(*,IntLit(2),Id(s)))]),If(BinaryOp(==,BinaryOp(%,Id(s),IntLit(6)),IntLit(2)),Block([AssignStmt(Id(g),BinaryOp(/,UnaryOp(-,CallExpr(Id(Math),Id(pow),[BinaryOp(%,Id(s),IntLit(9)),IntLit(3)])),IntLit(5)))]),If(BinaryOp(==,BinaryOp(%,Id(s),IntLit(6)),IntLit(3)),Block([AssignStmt(Id(g),BinaryOp(+,UnaryOp(-,CallExpr(Id(Math),Id(pow),[BinaryOp(%,Id(s),IntLit(30)),IntLit(2)])),BinaryOp(*,IntLit(3),Id(s))))]),If(BinaryOp(==,BinaryOp(%,Id(s),IntLit(6)),IntLit(4)),Block([AssignStmt(Id(g),UnaryOp(-,Id(s)))]),If(BinaryOp(==,BinaryOp(%,Id(s),IntLit(6)),IntLit(5)),Block([AssignStmt(Id(g),UnaryOp(-,CallExpr(Id(TriangleNumber),Id(isTriangleNumber),[BinaryOp(+,BinaryOp(%,Id(s),IntLit(5)),IntLit(5))])))]))))))),AssignStmt(Id(f),BinaryOp(+,BinaryOp(-,IntLit(40),BinaryOp(/,CallExpr(Id(Math),Id(abs),[BinaryOp(-,Id(d),IntLit(500))]),IntLit(20))),Id(g)))]),If(BinaryOp(>,Id(d),IntLit(800)),Block([AssignStmt(Id(f),BinaryOp(/,BinaryOp(*,UnaryOp(-,Id(d)),Id(s)),IntLit(1000)))])))),VarDecl(Id(Bitten),FloatType),If(BinaryOp(&&,BinaryOp(>=,Id(d),IntLit(200)),BinaryOp(<=,Id(d),IntLit(300))),Block([AssignStmt(Id(Bitten),BinaryOp(/,BinaryOp(+,BinaryOp(+,Id(d),Id(P1)),Id(P2)),IntLit(1000))),If(BinaryOp(>,Id(Bitten),FloatLit(0.8)),Block([AssignStmt(Id(pR),IntLit(0))]))]),Block([AssignStmt(Id(pR),BinaryOp(/,BinaryOp(+,Id(P1),BinaryOp(*,Id(P2),Id(f))),BinaryOp(+,IntLit(1000),CallExpr(Id(Math),Id(abs),[BinaryOp(*,Id(P2),Id(f))]))))])),Call(Id(Display),Id(display),[Id(pR)])]))])])"
        self.assertTrue(TestAST.test(input, expect, 400))