import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    # 2.1 Redeclared Variable/Constant/Attribute/Class/Method/Parameter
    def test_class_redeclared_1(self):
        input = """
            Class A{} 
            Class B{} 
            Class A{}
            Class Program{
                main(){}
            }"""
        expect = "Redeclared Class: A"
        self.assertTrue(TestChecker.test(input, expect, 400))

    def test_class_redeclared_2(self):
        input = """
            Class A{} 
            Class B{} 
            Class Program{
                main(){}
            }
            Class Program{}
            """
        expect = "Redeclared Class: Program"
        self.assertTrue(TestChecker.test(input, expect, 401))

    def test_attr_redeclared_1(self):
        input = """
            Class A{
                Var a: Int = 1;
                Var $a: Int = 2;
                Val a: Float = 3.0;
            }
            Class Program{
                main(){}
            }"""
        expect = "Redeclared Attribute: a"
        self.assertTrue(TestChecker.test(input, expect, 402))

    def test_attr_redeclared_2(self):
        input = """
            Class A{
                Var a: Int = 1;
                Var $a: Int = 2;
                Val $a: Float = 3.0;
            }
            Class Program{
                main(){}
            }"""
        expect = "Redeclared Attribute: $a"
        self.assertTrue(TestChecker.test(input, expect, 403))

    def test_attr_redeclared_3(self):
        input = """
            Class Program{
                Var a: Int;
                Val $b: Float = 3.5;
                Var $b: Int;
                main(){}
            }"""
        expect = "Redeclared Attribute: $b"
        self.assertTrue(TestChecker.test(input, expect, 404))

    # def test_attr_redeclared_4(self):
    #     input = """
    #         Class Program{
    #             Var a: Int;
    #             Val $b: Float = 3.5;
    #             {
    #                 Var b: Int;
    #                 {
    #                     Var b: Int;
    #                 }
    #                 Val b: Int = 1;
    #             }
    #             main(){}
    #         }"""
    #     expect = "Redeclared Attribute: b"
    #     self.assertTrue(TestChecker.test(input, expect, 405))

    def test_attr_redeclared_4(self):
        input = """
            Class Program{
                Var a: Int;
                Val $b: Float = 3.5;
                foo(){
                    Var b: Int;
                    {
                        Var b: Int;
                    }
                }
                Val $b: Int = 3;
                main(){}
            }"""
        expect = "Redeclared Attribute: $b"
        self.assertTrue(TestChecker.test(input, expect, 405))

    def test_method_redeclared_1(self):
        input = """
            Class A{
                Var a: Int = 1;
                a(){}
                a(){}
            }
            Class Program{
                main(){}
            }"""
        expect = "Redeclared Method: a"
        self.assertTrue(TestChecker.test(input, expect, 406))

    def test_method_redeclared_2(self):
        input = """
            Class A{
                Var $a: Int = 1;
                a(){}
                $a(){}
                $a(){}
            }
            Class Program{
                main(){}
            }"""
        expect = "Redeclared Method: $a"
        self.assertTrue(TestChecker.test(input, expect, 407))

    def test_method_redeclared_3(self):
        input = """
            Class A{
                Var $a: Int = 1;
                a(){}
                $b(){}
                a(c, d: Int){}
            }
            Class Program{
                main(){}
            }"""
        expect = "Redeclared Method: a"
        self.assertTrue(TestChecker.test(input, expect, 408))

    def test_method_redeclared_4(self):
        input = """
            Class A{
                Var $a: Int = 1;
                a(){}
                $b(c: Int){}
                $b(c, d: Int){}
            }
            Class Program{
                main(){}
            }"""
        expect = "Redeclared Method: $b"
        self.assertTrue(TestChecker.test(input, expect, 409))

    def test_method_redeclared_5(self):
        input = """
            Class A{
                Var a: Int = 1;
                a(){}
                $b(c: Int){}
                Constructor(_a: Int){
                    Self.a = _a;
                }
                $Constructor(c, d: Int){
                    Return c + d + Self.a;
                }
                Constructor(){}
            }
            Class Program{
                main(){}
            }"""
        expect = "Redeclared Method: Constructor"
        self.assertTrue(TestChecker.test(input, expect, 410))

    def test_method_redeclared_6(self):
        input = """
            Class C {
                Destructor(){}
                Destructor(){
                    Val a : Int = 1;
                }
            }
            Class A{
                Var c: C = New C();  
            }
            Class Program{
                main(){}
            }"""
        expect = "Redeclared Method: Destructor"
        self.assertTrue(TestChecker.test(input, expect, 411))

    def test_var_redeclared_1(self):
        input = """
            Class A{
                Var a: Int = 1;
                foo(a, b: Int){
                    Var a: Int = 1;
                }
            }
            Class Program{
                main(){}
            }"""
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input, expect, 412))

    def test_var_redeclared_2(self):
        input = """
            Class A{
                foo(b, c: Int){
                    Var a: Int = 1;
                    Var a: Float = 2.5;
                }
            }
            Class Program{
                main(){}
            }"""
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input, expect, 413))

    def test_var_redeclared_3(self):
        input = """
            Class A{
                Val $a: Int = 10;
                Var $b: Float;
                foo(b, c: Int){
                    Var a: Int = 1;
                    {
                        Val a: Float = 1.5;
                        Val b: Float = 2.5;
                        Var b: Int;
                    }
                }
            }
            Class Program{
                main(){
                    A.foo(1, 2);
                }
            }"""
        expect = "Redeclared Variable: b"
        self.assertTrue(TestChecker.test(input, expect, 414))

    def test_var_redeclared_4(self):
        input = """
            Class A{
                Val $a: Int = 10;
                Var $b: Float;
                foo(b, c: Int){
                    Var a: Int = 1;
                    {
                        Val a: Float = 1.5;
                        Val b: Float = 2.5;
                        {
                            Var b: Int = 1;
                        }
                        Var b: Int = 3;
                    }
                    Var b: Int;
                }
            }
            Class Program{
                main(){
                    A.foo(1, 2);
                }
            }"""
        expect = "Redeclared Variable: b"
        self.assertTrue(TestChecker.test(input, expect, 415))

    def test_const_redeclared_1(self):
        input = """
            Class A{
                Var a: Int = 1;
                foo(a, b: Int){
                    Val a: Float = 1.0;
                }
            }
            Class Program{
                main(){}
            }"""
        expect = "Redeclared Constant: a"
        self.assertTrue(TestChecker.test(input, expect, 416))

    def test_const_redeclared_2(self):
        input = """
            Class A{
                Var a: Int = 1;
                foo(b, c: Int){
                    Var a: Float;
                    Val a: Int = 2;
                }
            }
            Class Program{
                main(){}
            }"""
        expect = "Redeclared Constant: a"
        self.assertTrue(TestChecker.test(input, expect, 417))

    def test_const_redeclared_3(self):
        input = """
            Class A{
                Var a: Int = 1;
                foo(b, c: Int){
                    Val a: Float = 1.0;
                    {
                        Var a: Int = 1;
                        Val a: Float = 2.0;
                    }
                }
            }
            Class Program{
                main(){}
            }"""
        expect = "Redeclared Constant: a"
        self.assertTrue(TestChecker.test(input, expect, 418))

    def test_param_redeclared_1(self):
        input = """
            Class A{
                Var abc: Int = 1;
                foo(a, b: Int; a: Float){}
            }
            Class Program{
                main(){}
            }"""
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input, expect, 419))

    def test_param_redeclared_2(self):
        input = """
            Class A{
                Var abc: Int = 1;
                foo1(a: Int){}
                foo2(a: Int; a: Float){}
            }
            Class Program{
                main(){}
            }"""
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input, expect, 420))

    # 2.2 Undeclared Identifier/Attribute/Method/Class
    def test_class_undeclared_1(self):
        input = """
            Class A{} 
            Class B: C{}
            Class Program{
                main(){}
            }"""
        expect = "Undeclared Class: C"
        self.assertTrue(TestChecker.test(input, expect, 421))

    def test_class_undeclared_2(self):
        input = """
            Class A{} 
            Class B: A{}
            Class Program: C{
                main(){}
            }"""
        expect = "Undeclared Class: C"
        self.assertTrue(TestChecker.test(input, expect, 422))

    def test_class_undeclared_3(self):
        input = """
            Class A{} 
            Class B{}
            Class Program{
                main(){
                    Var a: C;
                }
            }"""
        expect = "Undeclared Class: C"
        self.assertTrue(TestChecker.test(input, expect, 423))

    def test_class_undeclared_4(self):
        input = """
            Class Program{
                main(){
                    Var A: Int;
                    Var x: Int = A::$a;
                }
            }"""
        expect = "Undeclared Class: A"
        self.assertTrue(TestChecker.test(input, expect, 424)) 

    def test_class_undeclared_5(self):
        input = """
            Class A : A{}
            Class Program{
                main(){}
            }"""
        expect = "Undeclared Class: A"
        self.assertTrue(TestChecker.test(input, expect, 425))

    def test_attr_undeclared_1(self):
        input = """
            Class A{
                Var a: Int = 1;
                Var x: Int;
                foo(a, b: Int){
                    Val c: Float = 1;
                }
            }
            Class Program{
                main(){
                    Var a: A;
                    Var b: Int;
                    b = a.y;
                }
            }"""
        expect = "Undeclared Attribute: y"
        self.assertTrue(TestChecker.test(input, expect, 426))

    def test_attr_undeclared_2(self):
        input = """
            Class A{
                Val a: Float = 1.5;
                Val x: Int = 2;
                foo(a, b: Int){
                    Val c: Float = 1;
                }
            }
            Class B: A{
                Var b: Int = 1;
            }
            Class Program{
                main(){
                    Var x: B = New B();
                    Val b: Float = x.a;
                }
            }"""
        expect = "Undeclared Attribute: a"
        self.assertTrue(TestChecker.test(input, expect, 427))

    def test_attr_undeclared_3(self):
        input = """
            Class A{
                Var $a: Int = 1;
                Val x: Int = 2;
                foo(a, b: Int){
                    Val c: Float = 1;
                }
            }
            Class Program{
                main(){
                    Var b: Int = A::$a;
                    Var c: Int = A::$x;
                }
            }"""
        expect = "Undeclared Attribute: $x"
        self.assertTrue(TestChecker.test(input, expect, 428))

    def test_attr_undeclared_4(self):
        input = """
            Class A{
                Var a: Int = 1;
                Val x: Int = 2;
                foo(a, b: Int){
                    Val c: Float = 1;
                }
            }
            Class Program{
                main(){
                    Var a: A;
                    a.a = 2;
                    a.d = 2;
                }
            }"""
        expect = "Undeclared Attribute: d"
        self.assertTrue(TestChecker.test(input, expect, 429))

    def test_attr_undeclared_5(self):
        input = """
            Class A{
                Var $a: Int = 1;
                Val x: Int = 2;
                foo(a, b: Int){
                    Val c: Float = 1;
                }
            }
            Class Program{
                main(){
                    A::$a = 2;
                    A::$d = 2;
                }
            }"""
        expect = "Undeclared Attribute: $d"
        self.assertTrue(TestChecker.test(input, expect, 430))

    def test_method_undeclared_1(self):
        input = """
            Class A{
                Var a: Int = 1;
                Val b: Int = 2;
                foo1(a, b: Int){
                    Val c: Int = 1;
                    Return a + b + c;
                }
                Constructor(){
                    Return;
                }
            }
            Class B{
                foo2(){}
            }
            Class Program{
                main(){
                    Var a: A = New A();
                    Var b: Int = a.foo1(1, 2);
                    Var c: Int = a.foo2();
                }
            }"""
        expect = "Undeclared Method: foo2"
        self.assertTrue(TestChecker.test(input, expect, 431))

    def test_method_undeclared_2(self):
        input = """
            Class A{
                Var a: Int = 1;
                Var b: Int = 2;
                foo(_a, _b: Int){
                    Self.a = _a;
                    Self.b = _b;
                }
            }
            Class Program{
                main(){
                    Var a: A;
                    a.foo(1, 2);
                    A::$foo();
                }
            }"""
        expect = "Undeclared Method: $foo"
        self.assertTrue(TestChecker.test(input, expect, 432))
    
    def test_method_undeclared_3(self):
        input = """
            Class A{
                Var a: Int = 1;
                Var b: Int = 2;
                foo1(_a, _b: Int){
                    Val c: Int = 1;
                    Return _a + _b + c;
                }
                foo2(){
                    Return 1;
                }
                Constructor(_a, _b: Int){
                    Self.a = _a;
                    Self.b = _b;
                    Return;
                }
            }
            Class Program{
                main(){
                    Var a: A = New A(3, 4);
                    Var b: Int = a.foo1(1, 2);
                    Var c: Int = a.foo1(1, 2) + a.foo2() + a.foo3();
                }
            }"""
        expect = "Undeclared Method: foo3"
        self.assertTrue(TestChecker.test(input, expect, 433))
    
    def test_method_undeclared_4(self):
        input = """
            Class A{
                Var a: Int = 1;
                Var b: Int = 2;
                foo1(_a, _b: Int){
                    Val c: Int = 1;
                    Return _a + _b + c;
                }
                $foo2(){
                    Return 1;
                }
                Constructor(){
                    Return;
                }
            }
            Class B: A{
                foo(){
                    Return 1;
                }
            }
            Class Program{
                main(){
                    Var a: B = New B();
                    Var b: Int = 2;
                    Var c: Int;
                    c = b + A::$foo2() - a.foo1(1, 2);
                }
            }"""
        expect = "Undeclared Method: foo1"
        self.assertTrue(TestChecker.test(input, expect, 434))

    def test_method_undeclared_5(self):
        input = """
            Class A{
                Var a: Int;
                Var $a: Int;
            }
            Class Program{
                main(){
                    Var A: A = New A();
                    Var x: Int = A::$a;
                    Var y: Int = A.a;
                    Var z: Int = A.foo();
                }
            }"""
        expect = "Undeclared Method: foo"
        self.assertTrue(TestChecker.test(input, expect, 435)) 

    def test_id_undeclared_1(self):
        input = """
            Class Program{
                main(){
                    Var a: Int;
                    Var b: Int = c;
                }
            }"""
        expect = "Undeclared Identifier: c"
        self.assertTrue(TestChecker.test(input, expect, 436))

    def test_id_undeclared_2(self):
        input = """
            Class A{
                foo(){}
            }
            Class Program{
                main(){
                    a.foo();
                }
            }"""
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input, expect, 437))

    def test_id_undeclared_3(self):
        input = """
            Class A{
                Var a: Int = 1;
            }
            Class Program{
                main(){
                    x.a = 2;
                }
            }"""
        expect = "Undeclared Identifier: x"
        self.assertTrue(TestChecker.test(input, expect, 438))
    
    def test_id_undeclared_4(self):
        input = """
            Class A{
                foo(){}
            }
            Class Program{
                main(){
                    Var a: Int = 1;
                    Var b: Int;
                    b = a + c.foo();
                }
            }"""
        expect = "Undeclared Identifier: c"
        self.assertTrue(TestChecker.test(input, expect, 439))
    
    def test_id_undeclared_5(self):
        input = """
            Class Program{
                main(){
                    Var a: Int;
                    Foreach (i In 1 .. 5){
                        a = i;
                    }
                }
            }"""
        expect = "Undeclared Identifier: i"
        self.assertTrue(TestChecker.test(input, expect, 440))

    def test_id_undeclared_6(self):
        input = """
            Class Program{
                main(){
                    Var a: Int;
                    Var i: Int;
                    Foreach (i In 1 .. 5){
                        If (i == 1){
                            Break;
                        }
                        Elseif (i == b){
                            a = i + 1;
                        }
                    }
                }
            }"""
        expect = "Undeclared Identifier: b"
        self.assertTrue(TestChecker.test(input, expect, 441))

    def test_id_undeclared_7(self):
        input = """
            Class A{
                foo(){
                    Return x;
                }
            }
            Class Program{
                main(){
                    Var a: A;
                    Var b: Int = a.foo();
                }
            }"""
        expect = "Undeclared Identifier: x"
        self.assertTrue(TestChecker.test(input, expect, 442))

    def test_id_undeclared_8(self):
        input = """
            Class A{
                foo(){
                    Return 1;
                }
            }
            Class Program{
                main(){
                    Var a: A;
                    Var b: Int = a.foo();
                    c = b - 1;
                }
            }"""
        expect = "Undeclared Identifier: c"
        self.assertTrue(TestChecker.test(input, expect, 443))

    def test_id_undeclared_9(self):
        input = """
            Class A{
                $foo(){
                    Return 1;
                }
            }
            Class Program{
                main(){
                    Var a: Int = 1;
                    Var b: Int = A::$foo();
                    Var c: Int;
                    c = a + b - d;
                }
            }"""
        expect = "Undeclared Identifier: d"
        self.assertTrue(TestChecker.test(input, expect, 444))

    # 2.3 Cannot Assign To Constant
    def test_cannot_assign_const_1(self):
        input = """
            Class Program{
                main(){
                    Val a: Int = 1;
                    a = 2;
                }
            }"""
        expect = "Cannot Assign To Constant: AssignStmt(Id(a),IntLit(2))"
        self.assertTrue(TestChecker.test(input, expect, 445))

    def test_cannot_assign_const_2(self):
        input = """
            Class A{
                Val a: Int = 1;
            }
            Class Program{
                main(){
                    Var b: A;
                    b.a = 2;
                }
            }"""
        expect = "Cannot Assign To Constant: AssignStmt(FieldAccess(Id(b),Id(a)),IntLit(2))"
        self.assertTrue(TestChecker.test(input, expect, 446))

    def test_cannot_assign_const_3(self):
        input = """
            Class A{
                Val $a: Int = 1;
            }
            Class Program{
                main(){
                    A::$a = 2;
                }
            }"""
        expect = "Cannot Assign To Constant: AssignStmt(FieldAccess(Id(A),Id($a)),IntLit(2))"
        self.assertTrue(TestChecker.test(input, expect, 447))

    def test_cannot_assign_const_4(self):
        input = """
            Class Program{
                main(){
                    Val a: Int = 1;
                    Var i: Int;
                    Foreach (i In 1 .. 10){
                        a = i;
                    }
                }
            }"""
        expect = "Cannot Assign To Constant: AssignStmt(Id(a),Id(i))"
        self.assertTrue(TestChecker.test(input, expect, 448))

    def test_cannot_assign_const_5(self):
        input = """
            Class Program{
                main(){
                    Var a: Int;
                    Val i: Int = 0;
                    Foreach (i In 1 .. 10){
                        a = 1 + i;
                    }
                }
            }"""
        expect = "Cannot Assign To Constant: IntLit(1)"
        self.assertTrue(TestChecker.test(input, expect, 449))

    # 2.4 Type Mismatch In Statement
    def test_mismatch_stmt_1(self):
        input = """
            Class Program{
                main(){
                    Var i: Int;
                    Foreach (i In 1 .. 10){
                        If (i + 1){
                            Break;
                        }
                    }
                    Return;
                }
            }
        """
        expect = "Type Mismatch In Statement: If(BinaryOp(+,Id(i),IntLit(1)),Block([Break]))"
        self.assertTrue(TestChecker.test(input, expect, 450))

    def test_mismatch_stmt_2(self):
        input = """
            Class Program{
                main(){
                    Var i: Float = 1.5;
                    Var a: Float;
                    Foreach (i In 1 .. 10){
                        a = i;
                    }
                    Return;
                }
            }
        """
        expect = "Type Mismatch In Statement: For(Id(i),IntLit(1),IntLit(10),IntLit(1),Block([AssignStmt(Id(a),Id(i))])])"
        self.assertTrue(TestChecker.test(input, expect, 451))

    def test_mismatch_stmt_3(self):
        input = """
            Class Program{
                main(){
                    Var i: Int;
                    Var a: Float;
                    Foreach (i In 1.5 .. 10){
                        a = i;
                    }
                    Return;
                }
            }
        """
        expect = "Type Mismatch In Statement: For(Id(i),FloatLit(1.5),IntLit(10),IntLit(1),Block([AssignStmt(Id(a),Id(i))])])"
        self.assertTrue(TestChecker.test(input, expect, 452))
        
    def test_mismatch_stmt_4(self):
        input = """
            Class Program{
                main(){
                    Var i: Int;
                    Var a: Float;
                    Foreach (i In 1 .. 10 By 2.5){
                        a = i;
                    }
                    Return;
                }
            }
        """
        expect = "Type Mismatch In Statement: For(Id(i),IntLit(1),IntLit(10),FloatLit(2.5),Block([AssignStmt(Id(a),Id(i))])])"
        self.assertTrue(TestChecker.test(input, expect, 453))

    def test_mismatch_stmt_5(self):
        input = """
            Class Program{
                main(){
                    Var a: Float;
                    Var b: Int;
                    a = 1;
                    b = 1.5;
                }
            }
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(b),FloatLit(1.5))"
        self.assertTrue(TestChecker.test(input, expect, 454))

    def test_mismatch_stmt_6(self):
        input = """
            Class Program{
                main(){
                    Var a: Float;
                    Var b: Int;
                    Var c: Boolean;
                    a = 1;
                    b = 2;
                    c = 0;
                }
            }
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(c),IntLit(0))"
        self.assertTrue(TestChecker.test(input, expect, 455))

    def test_mismatch_stmt_7(self):
        input = """
            Class A{
                foo(_a,_b: Float){
                    Return _a + _b;
                }
            }
            Class Program{
                main(){
                    Var x: A;
                    x.foo(1.5, 2.5);
                }
            }
        """
        expect = "Type Mismatch In Statement: Call(Id(x),Id(foo),[FloatLit(1.5),FloatLit(2.5)])"
        self.assertTrue(TestChecker.test(input, expect, 456))

    def test_mismatch_stmt_8(self):
        input = """
            Class A{
                foo(_a,_b: Float){
                    Return;
                }
            }
            Class Program{
                main(){
                    Var x: A;
                    x.foo(1.5, 2.5);
                    x.foo(1.5, 2);
                    x.foo(1.5, True);
                }
            }
        """
        expect = "Type Mismatch In Statement: Call(Id(x),Id(foo),[FloatLit(1.5),BooleanLit(True)])"
        self.assertTrue(TestChecker.test(input, expect, 457))

    def test_mismatch_stmt_9(self):
        input = """
            Class A{
                foo(_a: Float; _b: Int){
                    Return _a + _b;
                }
            }
            Class Program{
                main(){
                    Var x: A;
                    Var a: Int;
                    a = x.foo(1.5, 2);
                }
            }
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),CallExpr(Id(x),Id(foo),[FloatLit(1.5),IntLit(2)]))"
        self.assertTrue(TestChecker.test(input, expect, 458))

    def test_mismatch_stmt_10(self):
        input = """
            Class Program{
                Constructor(){
                    Return 1;
                }
                main(){}
            }
        """
        expect = "Type Mismatch In Statement: Return(IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 459))

    def test_mismatch_stmt_11(self):
        input = """
            Class Program{
                Constructor(){
                    Return;
                }
                Destructor(){
                    Return 1;
                }
                main(){}
            }
        """
        expect = "Type Mismatch In Statement: Return(IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 460))

    def test_mismatch_stmt_12(self):
        input = """
            Class A{
                Var length: Float = 1;
                Var width: Int = 2;
            }
            Class B{
                Var a: A = New A();
            }
            Class Program{
                main(){
                    Var a: B;
                    a.a.length = 3;
                    a.a.width = 3.5;
                }
            }"""
        expect = "Type Mismatch In Statement: AssignStmt(FieldAccess(FieldAccess(Id(a),Id(a)),Id(width)),FloatLit(3.5))"
        self.assertTrue(TestChecker.test(input, expect, 461))

    def test_mismatch_stmt_13(self):
        input = """
            Class Program{
                Var a: Array[Int, 3];
                main(){
                    Self.a[1] = "a";
                }
            }"""
        expect = "Type Mismatch In Statement: AssignStmt(ArrayCell(FieldAccess(Self(),Id(a)),[IntLit(1)]),StringLit(a))"
        self.assertTrue(TestChecker.test(input, expect, 462))

    def test_mismatch_stmt_14(self):
        input = """
            Class Program{
                Var a: Array[Array[Int, 2], 2];
                main(){
                    Self.a[1] = Array(1.5, 2.5);
                }
            }"""
        expect = "Type Mismatch In Statement: AssignStmt(ArrayCell(FieldAccess(Self(),Id(a)),[IntLit(1)]),[FloatLit(1.5),FloatLit(2.5)])"
        self.assertTrue(TestChecker.test(input, expect, 463))
    
    def test_mismatch_stmt_15(self):
        input = """
            Class A{
                foo(_a: Float; _b: Int){
                    If (_a + _b > 10){
                        Return 1.5;
                    }
                    Return _a + _b;
                }
            }
            Class Program{
                main(){
                    Var x: A;
                    Var a: Int;
                    a = x.foo(1.5, 2);
                }
            }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),CallExpr(Id(x),Id(foo),[FloatLit(1.5),IntLit(2)]))"
        self.assertTrue(TestChecker.test(input, expect, 464))

    def test_mismatch_stmt_16(self):
        input = """
            Class A{
                Var a: Int = 1;
                Var $a: Int = 2;
                foo1(){
                    Return 1;
                }
                $foo2(){
                    Return 2.5;
                }
            }
            Class Program{
                main(){
                    Var x: A;
                    Var y: Int = 1;
                    y = 1 + x.foo1() + A::$foo2();
                }
            }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(y),BinaryOp(+,BinaryOp(+,IntLit(1),CallExpr(Id(x),Id(foo1),[])),CallExpr(Id(A),Id($foo2),[])))"
        self.assertTrue(TestChecker.test(input, expect, 465))

    def test_mismatch_stmt_17(self):
        input = """
            Class A{
                Var a: Int = 1;
                Var $a: Int = 2;
                foo1(){
                    Return 1;
                }
                $foo2(){
                    Return 2;
                }
            }
            Class Program{
                main(){
                    Var x: A;
                    Var y: Int = A::$foo2();
                    Var z: Int;
                    z = x.a * y * x.foo1() / A::$foo2() - 1.5;
                }
            }"""
        expect = "Type Mismatch In Statement: AssignStmt(Id(z),BinaryOp(-,BinaryOp(/,BinaryOp(*,BinaryOp(*,FieldAccess(Id(x),Id(a)),Id(y)),CallExpr(Id(x),Id(foo1),[])),CallExpr(Id(A),Id($foo2),[])),FloatLit(1.5)))"
        self.assertTrue(TestChecker.test(input, expect, 466)) 

    def test_mismatch_stmt_18(self):
        input = """
            Class A{
                Var a: Int = 1;
                Var $a: Float = 2;
            }
            Class Program{
                main(){
                    Var x: A;
                    Var y: Int = x.a + A::$a;
                }
            }"""
        expect = "Type Mismatch In Statement: VarDecl(Id(y),IntType,BinaryOp(+,FieldAccess(Id(x),Id(a)),FieldAccess(Id(A),Id($a))))"
        self.assertTrue(TestChecker.test(input, expect, 467))  

    '''-------------------------CODE BUGS-------------------------
    def test_mismatch_stmt_15(self):
        input = """
            Class Program{
                Var a: Array[Array[Int, 2], 2];
                main(){
                    Self.a[1][2] = 1;
                    Self.a[2] = Array(3, 4);
                    Self.a = Array(Array(3.5, 5.5), Array(3.5, 4.5));
                }
            }"""
        expect = "Type Mismatch In Statement: "
        self.assertTrue(TestChecker.test(input, expect, 458))
    '''

    # 2.5 Type Mismatch In Expression
    def test_mismatch_expr_1(self):
        input = """
            Class Program{
                main(){
                    Var x: Array[Int, 2];
                    x[1.5] = 1;
                }
            }
        """
        expect = "Type Mismatch In Expression: ArrayCell(Id(x),[FloatLit(1.5)])"
        self.assertTrue(TestChecker.test(input, expect, 468))

    def test_mismatch_expr_2(self):
        input = """
            Class Program{
                main(){
                    Var x: Array[Int, 2];
                    Val a: Int = 1;
                    Var b: Float = 1.5;
                    Var c: Int;
                    x[1] = 1;
                    c = (a + b) % (a - 1);
                }
            }
        """
        expect = "Type Mismatch In Expression: BinaryOp(%,BinaryOp(+,Id(a),Id(b)),BinaryOp(-,Id(a),IntLit(1)))"
        self.assertTrue(TestChecker.test(input, expect, 469))

    def test_mismatch_expr_3(self):
        input = """
            Class Program{
                main(){
                    Val a: Int = 1;
                    Var b: Float = 1.5;
                    Var c: Boolean;
                    c = (a + b) == (a - 1);
                }
            }
        """
        expect = "Type Mismatch In Expression: BinaryOp(==,BinaryOp(+,Id(a),Id(b)),BinaryOp(-,Id(a),IntLit(1)))"
        self.assertTrue(TestChecker.test(input, expect, 470))

    def test_mismatch_expr_4(self):
        input = """
            Class Program{
                main(){
                    Val a: Int = 1;
                    Var b: Int = 2;
                    Var c: Boolean;
                    c = (a + b) == !(a - 1);
                }
            }
        """
        expect = "Type Mismatch In Expression: UnaryOp(!,BinaryOp(-,Id(a),IntLit(1)))"
        self.assertTrue(TestChecker.test(input, expect, 471))

    def test_mismatch_expr_6(self):
        input = """
            Class A{
                Var a: Int = 1;
            }
            Class Program{
                main(){
                    Var x: Int;
                    Var y: Int;
                    y = x.a;
                }
            }
        """
        expect = "Type Mismatch In Expression: FieldAccess(Id(x),Id(a))"
        self.assertTrue(TestChecker.test(input, expect, 472))

    def test_mismatch_expr_7(self):
        input = """
            Class Program{
                Var i: Int;
                main(){
                    Var a: Int = 2;
                    If (True){
                        Var a: Int = 2;
                        Foreach (Self.i In 1 .. 20 By a){
                            Val a: Float = 1.5;
                            If (a >= 2){
                                Self.i = a % 2;
                            }
                            Else{
                                Self.i = Self.i + 1;
                            }
                        }
                    }
                    Return;
                }
            }
        """
        expect = "Type Mismatch In Expression: BinaryOp(%,Id(a),IntLit(2))"
        self.assertTrue(TestChecker.test(input, expect, 473))

    # 2.6 Type Mismatch In Constant
    def test_mismatch_const_1(self):
        input = """
            Class Program{
                main(){
                    Val a: Int = 1;
                    Val b: Float = 1;
                    Val c: Boolean = True;
                    Val d: String = "a";
                    Val e: Array[Int, 3] = Array(1.5, 2.5, 3.5);
                }
            }
        """
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(e),ArrayType(3,IntType),[FloatLit(1.5),FloatLit(2.5),FloatLit(3.5)])"
        self.assertTrue(TestChecker.test(input, expect, 474))

    def test_mismatch_const_2(self):
        input = """
            Class Program{
                main(){
                    Val a: Array[Int, 3] = Array(1, 2, 3);
                    Val b: Array[Int, 3] = Array(1, 2);
                }
            }
        """
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(b),ArrayType(3,IntType),[IntLit(1),IntLit(2)])"
        self.assertTrue(TestChecker.test(input, expect, 475))

    def test_mismatch_const_3(self):
        input = """
            Class Program{
                Val a: Array[Int, 3] = Array(1, 2, 3);
                main(){
                    Val a: Array[Float, 3] = Array("a", "b", "c");
                }
            }
        """
        expect = "Type Mismatch In Constant Declaration: ConstDecl(Id(a),ArrayType(3,FloatType),[StringLit(a),StringLit(b),StringLit(c)])"
        self.assertTrue(TestChecker.test(input, expect, 476))

    # 2.7 Break/Continue not in loop
    def test_must_in_loop_1(self):
        input = """
            Class Program{
                main(){
                    Var i: Int;
                    Foreach (i In 1 .. 20 By 2){
                        If (i > 10.5){
                            Break;
                        }
                        Elseif (i < 3.5){
                            Continue;
                        }
                        i = i + 1;
                    }
                    Continue;
                }
            }
        """
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input, expect, 477))

    # 2.8 Illegal Constant Expression
    def test_illegal_const_1(self):
        input = """
            Class A{
                Var a: Int = 1;
                Val b: Int;
            }
            Class Program{
                main(){}
            }"""
        expect = "Illegal Constant Expression: None"
        self.assertTrue(TestChecker.test(input, expect, 478))

    def test_illegal_const_2(self):
        input = """
            Class A{
                Var a: Int = 1;
                Val x: Int = 2;
                foo(a, b: Int){
                    Val c: Float = Self.x + Self.a;
                }
            }
            Class Program{
                main(){}
            }"""
        expect = "Illegal Constant Expression: BinaryOp(+,FieldAccess(Self(),Id(x)),FieldAccess(Self(),Id(a)))"
        self.assertTrue(TestChecker.test(input, expect, 479))

    def test_illegal_const_3(self):
        input = """
            Class A{
                Var a: Int = 1;
                Val x: Int = Self.a + 1;
            }
            Class Program{
                main(){}
            }"""
        expect = "Illegal Constant Expression: BinaryOp(+,FieldAccess(Self(),Id(a)),IntLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 480))

    def test_illegal_const_4(self):
        input = """
            Class A{
                Var a: Int = 1;
                Val x: Int = 2;
                foo(a, b: Int){
                    Val c: Float = 1;
                    Return a + b - c;
                }
            }
            Class Program{
                main(){
                    Var a: A;
                    Val b: Int = 1;
                    Val c: Int = a.x + a.foo(1, 2) + a.a;
                }
            }"""
        expect = "Illegal Constant Expression: BinaryOp(+,BinaryOp(+,FieldAccess(Id(a),Id(x)),CallExpr(Id(a),Id(foo),[IntLit(1),IntLit(2)])),FieldAccess(Id(a),Id(a)))"
        self.assertTrue(TestChecker.test(input, expect, 481))

    def test_illegal_const_5(self):
        input = """
            Class Program{
                Val a: Int = 1;
                main(){
                    Var b: Array[Int, 2] = Array(1, 2);
                    Val c: Int = Self.a + b[1];
                }
            }"""
        expect = "Illegal Constant Expression: BinaryOp(+,FieldAccess(Self(),Id(a)),ArrayCell(Id(b),[IntLit(1)]))"
        self.assertTrue(TestChecker.test(input, expect, 482))

    def test_illegal_const_6(self):
        input = """
            Class A{
                Var length: Int = 1;
                Var width: Int = 2;
            }
            Class B{
                Var a: A = New A();
            }
            Class Program{
                main(){
                    Var a: B;
                    Val b: Int = a.a.length;
                }
            }"""
        expect = "Illegal Constant Expression: FieldAccess(FieldAccess(Id(a),Id(a)),Id(length))"
        self.assertTrue(TestChecker.test(input, expect, 483))

    def test_illegal_const_7(self):
        input = """
        Class Program{
            Var a: Int = 10; 
            foo(){ 
                Var a: Array[Int, 3] = Array(Self.a, 1, 2);
                Val b: Int = a[0];
            }
            main(){}
        }
        """
        expect = "Illegal Constant Expression: ArrayCell(Id(a),[IntLit(0)])"
        self.assertTrue(TestChecker.test(input, expect, 484))

    def test_illegal_const_8(self):
        input = """
            Class Shape{}
            Class Program: Shape{
                Val a: Shape = Null;
                Var b: Shape = Null;
                Val c: Shape;
                Val d: String;
                main(){}
            }"""
        expect = "Illegal Constant Expression: None"
        self.assertTrue(TestChecker.test(input, expect, 485))

    # 2.9 Illegal Array Literal
    def test_illegal_array_1(self):
        input = """
            Class Program{
                Var a: Array[Int, 3] = Array(1, 2, 2.5);
                main(){}
            }"""
        expect = "Illegal Array Literal: [IntLit(1),IntLit(2),FloatLit(2.5)]"
        self.assertTrue(TestChecker.test(input, expect, 486))

    def test_illegal_array_2(self):
        input = """
            Class Program{
                Var a: Array[Int, 3] = Array(1, 2, 3);
                main(){
                    Val a: Array[Array[Int, 2], 2] = Array(Array(1, 2), Array(1, 2.5));
                }
            }"""
        expect = "Illegal Array Literal: [[IntLit(1),IntLit(2)],[IntLit(1),FloatLit(2.5)]]"
        self.assertTrue(TestChecker.test(input, expect, 487))

    def test_illegal_array_3(self):
        input = """
            Class Program{
                Var a: Array[Int, 3] = Array(1, 2, 3);
                main(){
                    Val a: Array[Array[Int, 2], 2] = Array(Array(1, 2), Array(1.5, 2.5));
                }
            }"""
        expect = "Illegal Array Literal: [[IntLit(1),IntLit(2)],[FloatLit(1.5),FloatLit(2.5)]]"
        self.assertTrue(TestChecker.test(input, expect, 488))

    # 2.10 Illegal Member Access
    def test_illegal_member_1(self):
        input = """
            Class A{
                Var a: Int = 1;
                Var $a: Int = 2;
            }
            Class Program{
                main(){
                    Var x: Int = A.a;
                }
            }"""
        expect = "Illegal Member Access: FieldAccess(Id(A),Id(a))"
        self.assertTrue(TestChecker.test(input, expect, 489))

    def test_illegal_member_2(self):
        input = """
            Class A{
                Var a: Int = 1;
                Var $a: Int = 2;
                foo1(){
                    Return 1;
                }
                $foo2(){
                    Return 2;
                }
            }
            Class Program{
                main(){
                    Var x: A;
                    Var y: Int = A.foo1();
                }
            }"""
        expect = "Illegal Member Access: CallExpr(Id(A),Id(foo1),[])"
        self.assertTrue(TestChecker.test(input, expect, 490))  

    # 2.11 No Entry Point
    def test_no_entry_1(self):
        input = """
            Class A{} 
            Class B{}"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 491))

    def test_no_entry_2(self):
        input = """
            Class A{} 
            Class B{}
            Class Program{}"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 492))

    def test_no_entry_3(self):
        input = """
            Class A{}
            Class B{}
            Class Program{
                _main(){}
            }"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 493))

    def test_complex_program_1(self):
        input = """
            Class Shape{
                Val $numOfShape: Int = 0;
                Val immutableAttribute: Int = 0;
                Var length, width: Int;
                $getNumOfShape(){
                    Return Shape::$numOfShape;
                }
            }
            Class Rectangle: Shape{
                getArea(){
                    Return Self.length * 1;
                }
            }
            Class Program{
                main(){
                    Var a: Int = Shape::$numOfShape + Shape::$getNumOfShape();
                }
            }"""
        expect = "Undeclared Attribute: length"
        self.assertTrue(TestChecker.test(input, expect, 494))

    def test_complex_program_2(self):
        input = """
            Class Shape{
                Val $numOfShape: Int = 0;
                Val immutableAttribute: Int = 0;
                Var length, width: Int;
                $getNumOfShape(){
                    Return Shape::$numOfShape;
                }
            }
            Class Rectangle: Shape{
                getArea(){
                    Return 1 * 2;
                }
            }
            Class Program{
                Var myPI: Float = 3.14;
                main() {
                    ## Out.printInt(Shape::$numOfShape); ##
                    Var r, s: Float;
                    r = 2.0;
                    Var a: Array[Int, 5];
                    s = r * r * Self.myPI;
                    a[1] = s;
                }
            }"""
        expect = "Type Mismatch In Statement: AssignStmt(ArrayCell(Id(a),[IntLit(1)]),Id(s))"
        self.assertTrue(TestChecker.test(input, expect, 495))

    def test_complex_program_3(self):
        input = """
            Class Shape{
                Val $numOfShape: Int = 0;
                Val immutableAttribute: Int = 0;
                Var length, width: Int;
                Var a : Array[Int, 3] = Array(1 + 1, 2, 3);
                $getNumOfShape(){
                    Return Shape::$numOfShape;
                }
            }
            Class Program{
                Val Pi: Int = 3;
                _main(){
                    Var a : Int = 12;
                    Var x: Shape;
                    Var i: Int;
                    If (a + 1 == 9){
                        a = Self.Pi; 
                        Foreach(i In 1 .. 100 By 2){
                            a = x.a[(1 + 2 + 3)];
                            a = Shape::$getNumOfShape();
                            Continue;
                        }
                    }
                    Else{
                        a = a * 3 - 9; 
                    }
                }
            }"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 496))

    def test_complex_program_4(self):
        input = """
            Class PrimeNumber{
                isPrimeNumber(n: Int){
                    Var i: Int;
                    Foreach(i In 2 .. n/2){
                        If (n % i == 0){
                            Return False;
                        }
                    }
                    Return True;
                }
            }
            Class System{
                readFile(a, b, c: Int){
                    Return True;
                }
            }
            Class Program{
                _main(){
                    Var hp, d, s: Int = 0, 0, 0;
                    Var P1, P2, f, pR: Float = 0, 0, 0, -1;
                    Var x: PrimeNumber;
                    Var System: System;
                    If (System.readFile(hp, d, s)){
                        If (x.isPrimeNumber(hp)){
                            P1 = 1000;
                            P2 = (hp + s) % 1000;
                        }
                        Else {
                            P1 = hp;
                            P2 = (hp + d) % 100;
                        }
                    }
                }
            }"""
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input, expect, 497))

    def test_complex_program_5(self):
        input = """
            Class Math{
                Val $pi: Float = 3.14;
            }
            Class Circle{
                Constructor(radius: Float; x: Int){}
            }
            Class Program{
                Var $str: String = "From Class Program: ";
                main(){      
                    Var circle: Circle = New Circle(Math::$pi, 4);
                }
                print(s: String){
                    System.out.println(s +. " says hello to the world!");
                    Return;
                }
            }"""
        expect = "Undeclared Identifier: System"
        self.assertTrue(TestChecker.test(input, expect, 498))

    def test_complex_program_6(self):
        input = """
            Class A{
                Var a: Int = 5;
                Val b: Int = 4;
                Var c: Float = 2.2;
            }
            Class D{
                daily(x: A){
                    If (x.a > 3){}
                    Elseif (x.b >= 3){}

                    If (x.a < 3){}
                    Elseif (x.a <= x.c){}
                    
                    If ((x.a == x.b) || (x.a != x.b)){}
                    Else{
                        Var a: Float = x.a + x.b;
                    }
                }
            }
            Class Program{
                main(){
                    D.daily(1);
                }
            }"""
        expect = "Illegal Member Access: Call(Id(D),Id(daily),[IntLit(1)])"
        self.assertTrue(TestChecker.test(input, expect, 499))