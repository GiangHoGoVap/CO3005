import unittest

from TestUtils import TestParser

class ParserSuite(unittest.TestCase):
    def test_program_structure1(self):
        input = """"""
        expect = "Error on line 1 col 0: <EOF>"
        self.assertTrue(TestParser.test(input, expect, 201))

    def test_program_structure2(self):
        input = """main () {}"""
        expect = "Error on line 1 col 0: main"
        self.assertTrue(TestParser.test(input, expect, 202))

    def test_program_structure3(self):
        input = """Class Program {}"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 203))

    def test_program_structure4(self):
        input = """Class _program123 {}"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 204))

    def test_program_structure5(self):
        input = """Class Continue {
            main() {}
        }"""
        expect = "Error on line 1 col 6: Continue"
        self.assertTrue(TestParser.test(input, expect, 205))

    def test_program_structure6(self):
        input = """Class Program {} Class _program {} Class program {}"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 206))

    def test_program_structure7(self):
        input = """Class Program {
            main() {}
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 207))

    def test_program_structure8(self):
        input = """Class Program {
            main() {
                Val a: Array[Array[Int, 10], 0x15];
                Return;
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 208))

    def test_attr_declaration1(self):
        input = """Class Shape {
            Var num: Array[Int, 2] = Array(1, 2 + 3);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 209))

    def test_attr_declaration2(self):
        input = """Class Shape {
            Val $num: Array[Int, 2] = Array(0123 + 0456, 1_234);
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 210))

    def test_method_declaration1(self):
        input = """Class Shape {
            Var num1, num2: Int = 1, 2;
            GetFunc(a, b: Int ; c: Float) {
                Var num3: Int = a;
                Val $num4, $num5: Int = a,b;
            }
        }"""
        expect = "Error on line 5 col 20: $num4"
        self.assertTrue(TestParser.test(input, expect, 211))
    
    def test_method_declaration2(self):
        input = """Class Shape {
            Var num1, num2: Int = 1;
            GetFunc(a, b: Int; c: Float) {
                Var num3: Int = a;
                Val num4: Int = b;
            }
        }"""
        expect = "Error on line 2 col 35: ;"
        self.assertTrue(TestParser.test(input, expect, 212))

    def test_attr_var_decl1(self):
        input = """Class Shape {
            Var num1: Int = True;
            Val $num2: Boolean = 1;
            main() {
                Var num3: Array[Int, 2] = Array("abc", 2);
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 213))

    def test_attr_var_decl2(self):
        input = """Class Program {
            Var $a: Int = 0b1111;
            Var b: Float = 5.5;
            main() {
                Var res: Int = a + b;
                Out.printInt(res);
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 214))

    def test_attr_var_decl3(self):
        input = """Class Program {
            Var a: Int = 1;
            main() {
                Var b: Int = 2;
                Var $res: Int = a + b;
            }
        }"""
        expect = "Error on line 5 col 20: $res"
        self.assertTrue(TestParser.test(input, expect, 215))

    def test_attr_var_decl4(self):
        input = """Class Program {
            Var ab: String = "";
            Val $bc: String = "a1b2";
            main() {
                Var a: String = "abcdef";
                Val b: String = "123456";
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 216))

    def test_constructor_destructor1(self):
        input = """Class Shape {
            Constructor() {
                Return;
            }
            Destructor() {}
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 217))

    def test_constructor_destructor2(self):
        input = """Class Shape {
            Constructor() {}
            Destructor() {}
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 218))

    def test_constructor_destructor3(self):
        input = """Class Shape {
            Constructor() {
                Return;
            }
            Destructor() {
                Return;
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 219))

    def test_constructor_destructor4(self):
        input = """Class Shape {
            Constructor(length, width: Int; area: Float) {
                Self.length = length;
                Self.width = width;
                Return;
            }
            Destructor() {}
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 220))

    def test_constructor_destructor5(self):
        input = """Class Shape {
            Constructor() {
                Return;
            }
            Destructor(length, width: Int) {}
        }"""
        expect = "Error on line 5 col 23: length"
        self.assertTrue(TestParser.test(input, expect, 221))

    def test_constructor_destructor6(self):
        input = """Class Program {
            Destructor(w: Int) {
                Self.call();
            }
            main() {
                Self.a();
                Return;
            }
        }"""
        expect = "Error on line 2 col 23: w"
        self.assertTrue(TestParser.test(input, expect, 222))

    def test_indexed_arr1(self):
        input = """Class Program {
            main() {
                Val a : Array[Int, 0];
            }
        }"""
        expect = "Error on line 3 col 35: 0"
        self.assertTrue(TestParser.test(input, expect, 223))

    def test_indexed_arr2(self):
        input = """Class Program {
            main() {
                Val a : Array[Int, 5];
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 224))

    def test_multi_arr1(self):
        input = """Class Program {
            main() {
                a = Array(Array("A"), Array("B"), Array("C"));
                Self.a[0] = 1;
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 225))

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
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 226))

    def test_multi_arr3(self):
        input = """Class Program {
            main() {
                Var $arr: Array[Int, 3] = Array(1, 2 + 2, True);
                arr[3] = 3;
                Out.printStr(arr);
            }
        }"""
        expect = "Error on line 3 col 20: $arr"
        self.assertTrue(TestParser.test(input, expect, 227))

    def test_var_decl_stmt1(self):
        input = """Class Program {
            main() {
                Val $num: Array[Int, 1];
            }
        }"""
        expect = "Error on line 3 col 20: $num"
        self.assertTrue(TestParser.test(input, expect, 228))

    def test_var_decl_stmt2(self):
        input = """Class Program {
            main() {
                Var num: Array[Float, 2] = Array(1.5, 2.e+5);
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 229))

    def test_var_decl_stmt3(self):
        input = """Class Shape {
            methodA(){
                Var $a: Int;
            }
        }"""
        expect = "Error on line 3 col 20: $a"
        self.assertTrue(TestParser.test(input, expect, 230))

    def test_var_decl_stmt4(self):
        input = """Class Program {
            main() {
                Var a: Int = -1;
                Val $b: Float = -1.5;
                Var c: Boolean;
                c = True;
                c = !c;
            }
        }"""
        expect = "Error on line 4 col 20: $b"
        self.assertTrue(TestParser.test(input, expect, 231))

    def test_direct_func(self):
        input = """Class Program {
            getName() {
                Var b: Float = 0.3;
            }
            main() {
                If (a >= b) {
                    Var a: Int = 0;
                    a = a + 3;
                }
                Elseif (b <= c) {
                    getName(a >= b);
                }
                Else {
                    c = Self.a;
                }
            }
        }"""
        expect = "Error on line 11 col 27: ("
        self.assertTrue(TestParser.test(input, expect, 232))

    def test_instance_access1(self):
        input = """Class Program {
            main() {
                Shape.width.val = 5;
                a = (a.b)::$c;
                a = Shape.width.val;
            }
        }"""
        expect = "Error on line 4 col 25: ::"
        self.assertTrue(TestParser.test(input, expect, 233))

    def test_instance_access2(self):
        input = """Class Program {
            main() {
                Shape.width = Self._width;
                Shape.area = Shape.length * Self._width;
                Var d: Int = Shape.area;
                Out.printInt(d);
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 234))

    def test_instance_access3(self):
        input = """Class Program {
            main() {
                a = (1 + 2).b;
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 235))

    def test_static_access1(self):
        input = """Class Program {
            main($a : Int) {}
        }"""
        expect = "Error on line 2 col 17: $a"
        self.assertTrue(TestParser.test(input, expect, 236))

    def test_static_access2(self):
        input = """Class Program {
            main() {
                Shape::$width = 10;
                a = (Shape::$width)::$length;
                b = Shape::$width::$length;
            }
        }"""
        expect = "Error on line 4 col 35: ::"
        self.assertTrue(TestParser.test(input, expect, 237))

    def test_static_access3(self):
        input = """Class Program {
            main() {
                Shape::$width = 10;
                a = Shape::area;
            }
        }"""
        expect = "Error on line 4 col 27: area"
        self.assertTrue(TestParser.test(input, expect, 238))

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
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 239))

    def test_static_access5(self):
        input = """Class Program {
            Var $a: String = "Hello World";
            main() {
                Var b: Int = 100000000;
                b.c.d = Program::$a.b.c().d.e.x::$f() + 1;
                Return (b - Self::$a + Self.what - Program::$a.b.c(Program::$a.b).d.e.x::$f());
            }
        }
        """
        expect = """Error on line 5 col 47: ::"""
        self.assertTrue(TestParser.test(input, expect, 240))

    def test_operator1(self):
        input = """Class Program {
            main() {
                a = g != ((b * c / d % e) > f);
                b = ((abc +. def) ==. ghi).upper();
                c = 1 || True && False;
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 241))

    def test_operator2(self):
        input = """Class Program {
            main() {
                a = -1 + -2 + -3;
                b = str1 +. str2.str3;
                c = !True + -!2;
            }
        }"""
        expect = "Error on line 5 col 29: !"
        self.assertTrue(TestParser.test(input, expect, 242))

    def test_operator3(self):
        input = """Class Program {
            main() {
                a = a[a.b] + c[a::$b];
                d = True && False && True || False ==. e;
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 243))

    def test_operator4(self):
        input = """Class Program {
            Var a: Int = a.b().c::$d;
        }"""
        expect = "Error on line 2 col 32: ::"
        self.assertTrue(TestParser.test(input, expect, 244))

    def test_operator5(self):
        input = """Class Program {
            Var $a: String = a::$b.c();
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 245))

    def test_operator6(self):
        input = """Class Program {
            main() {
                New X()::$abc();
            }
        }"""
        expect = "Error on line 3 col 23: ::"
        self.assertTrue(TestParser.test(input, expect, 246))

    def test_operator7(self):
        input = """Class Program {
            main() {
                a = New X()::$abc;
            }
        }"""
        expect = "Error on line 3 col 27: ::"
        self.assertTrue(TestParser.test(input, expect, 247))

    def test_operator8(self):
        input = """Class Program {
            main() {
                Val a : Int = a[1] + b[2]; 
                a = New X()::$abc();
            }
        }"""
        expect = "Error on line 4 col 27: ::"
        self.assertTrue(TestParser.test(input, expect, 248))

    def test_operator9(self):
        input = """Class Program {
            main() {
                a = b.(New C());
            }
        }"""
        expect = "Error on line 3 col 22: ("
        self.assertTrue(TestParser.test(input, expect, 249))

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
                Var obj: Shape = New Shape(1, 4);
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 250))

    def test_assign_stmt1(self):
        input = """Class Program {
            Var $a: Array[Int, 3] = Array(1, 2, 3);
            main(){
                a[1] = 4;
                Var b: Int = 10;
                Val c: Float = 2.0;
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 251))

    def test_assign_stmt2(self):
        input = """Class Program {
            main() {
                a._123::$_456 = 1 + 2;
            }
        }"""
        expect = "Error on line 3 col 22: ::"
        self.assertTrue(TestParser.test(input, expect, 252))

    def test_assign_stmt3(self):
        input = """Class Program {
            main() {
                a::$b.c(e: Int).f = a::$b.c() - a.b().c;
            }
        }"""
        expect = "Error on line 3 col 25: :"
        self.assertTrue(TestParser.test(input, expect, 253))

    def test_assign_stmt4(self):
        input = """Class Shape {
            $methodA(){
                Return Self::$A;
            }
        }
        Class Program {
            main() {
                Var a: Int = Shape::$methodA();
                Out.printInt(a);
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 254))

    def test_assign_stmt5(self):
        input = """Class _program {
            Var $a: Int = 0b10;
            $methodA() {
                Return Self::$a;
            }
        }
        Class Program {
            main() {
                Var b: Int;
                b = _program::$methodA();
                Out.printInt(b);
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 255))

    def test_assign_stmt6(self):
        input = """Class _Program {
            Var $A: Array[Array[String, 3], 3];
            $getMethodA() {
                Return Self::$A;
            }
            $setMethodA(_a: Array[Array[String, 3], 3]) {
                Self::$A = _a;
            }
        }
        Class Program {
            main() {
                Var arr: Array[Array[String, 3], 3] = Array(Array("Volvo", "22", "18"), Array("Saab", "5", "2"), Array("Land Rover", "17", "15"));
                _Program::$setMethodA(arr);
                Out.printLn(_Program::$getMethodA());
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 256))

    def test_assign_stmt7(self):
        input = """Class Program {
            main() {
                a = "1a2b3c"::$d();
            }
        }"""
        expect = "Error on line 3 col 28: ::"
        self.assertTrue(TestParser.test(input, expect, 257))

    def test_assign_stmt8(self):
        input = """Class Program1 {
            Val a: Int = Self.function(1, str1 +. str2,);
        }"""
        expect = "Error on line 2 col 55: )"
        self.assertTrue(TestParser.test(input, expect, 258))

    def test_if_stmt1(self):
        input = """Class Program {
            Var a, b: Int;
            If ((a > 0) && (b > 0)) {
                ## Do Something ##
            }
        }"""
        expect = "Error on line 3 col 12: If"
        self.assertTrue(TestParser.test(input, expect, 259))

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
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 260))

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
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 261))

    def test_if_stmt4(self):
        input = """Class Program {
            main() {
                If (a > b > c) {
                    Out.printLn("1");
                }
                If (a > b < c) {
                    Out.printLn("2");
                }
                If (a < b > c) {
                    Out.printLn("3");
                }
                If (a < b < c) {
                    Out.printLn("4");
                }
                Else {
                    Out.printLn("5");
                }
            }
        }"""
        expect = "Error on line 3 col 26: >"
        self.assertTrue(TestParser.test(input, expect, 262))

    def test_if_stmt5(self):
        input = """Class Program {
            main() {
                If (a == 1) Then {
                    System.HelloWorld();
                }
                Else {
                    System.HelloVietNam();
                }
                Return;
            }
        }
        """
        expect = "Error on line 3 col 28: Then"
        self.assertTrue(TestParser.test(input, expect, 263))

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
                        Return Self::$a;
                    }
                }
            }
        }"""
        expect = "successful";
        self.assertTrue(TestParser.test(input, expect, 264))

    def test_foreach_stmt2(self):
        input = """Class Program {
            main() {
                Foreach(Self.i In n-100 .. n+0b1 By 0xAF) {
                    Out.printLn(0X123ABC);
                }
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 265))

    def test_foreach_stmt3(self):
        input = """Class Program {
            main() {
                Foreach(i In True .. False By a[0]) {
                    a[1] = i;
                    Out.printInt(a[i]);
                }
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 266))

    def test_foreach_stmt4(self):
        input = """Class Program {
            main() {
                Foreach(x In 100 .. 1 By True) {
                    a[i] = x;
                }
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 267))

    def test_foreach_stmt5(self):
        input = """Class Program {
            main() {
                Foreach(i In a .. b By c) {
                    Out.printLn(a);
                }
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 268))

    def test_foreach_stmt6(self):
        input = """Class Program {
            main() {
                Foreach (i In 1..10 By 2) {
                    Out.printInt(i);
                }
            }
        }"""
        expect = "Error on line 3 col 33: 10"
        self.assertTrue(TestParser.test(input, expect, 269))

    def test_break_stmt1(self):
        input = """Class Program {
            main() {
                Break;
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 270))

    def test_break_stmt2(self):
        input = """Class Program {
            main() {
                Foreach(i In 1 .. 100 By 101) {
                    If (i == 5) {
                        Break a;
                    }
                }
            }
        }"""
        expect = "Error on line 5 col 30: a"
        self.assertTrue(TestParser.test(input, expect, 271))

    def test_continue_stmt1(self):
        input = """Class Program {
            main() {
                Continue;
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 272))

    def test_continue_stmt2(self):
        input = """Class Program {
            main() {
                Foreach(x In 5 .. 2) {
                    If (x == 3) {
                        Continue a;
                    }
                }
            }
        }"""
        expect = "Error on line 5 col 33: a"
        self.assertTrue(TestParser.test(input, expect, 273))

    def test_method_invocation_stmt1(self):
        input = """Class Program {
            Shape::$getNumOfShape();
        }"""
        expect = "Error on line 2 col 17: ::"
        self.assertTrue(TestParser.test(input, expect, 274))

    def test_scalar_var1(self):
        input = """Class Program {
            main() {
                Foreach (Self.func In 1 .. 10) {
                    Out.println("abc");
                }
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 275))

    def test_scalar_var2(self):
        input = """Class Program {
            main() {
                Foreach (a._val In 1 .. 10) {
                    Out.println("abc");
                }
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 276))

    def test_scalar_var3(self):
        input = """Class Program {
            main() {
                Foreach(Self.a.b In 1 .. 10 By 2) {
                    a = Self.a.b._val;
                    b = Program.d;
                }
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 277))

    def test_scalar_var4(self):
        input = """Class Program {
            main() {
                Foreach (Self.a.b._val In 1 .. 10) {
                    Out.println("abc");
                }
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 278))

    def test_scalar_var5(self):
        input = """Class Program {
            main() {
                Foreach (Self.func().b._val In 1 .. 10 By 3) {
                    Out.println("abc");
                }
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 279))

    def test_scalar_var6(self):
        input = """Class Program {
            main() {
                Foreach (a::$b In 1 .. 10) {
                    Out.println("abc");
                }
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 280))

    def test_scalar_var7(self):
        input = """Class Program {
            main() {
                Foreach (Self::$a In 1 .. 10 By 2) {
                    Out.printLn("abc");
                }
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 281))

    def test_scalar_var8(self):
        input = """Class Program {
            main() {
                Foreach (Self::$a.b._val In 1 .. 10) {
                    Out.println("abc");
                }
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 282))

    def test_scalar_var9(self):
        input = """Class Program {
            main() {
                Foreach (Self::$func().b._val In 1 .. 10) {
                    Out.println("abc");
                }
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 283))

    def test_scalar_var10(self):
        input = """Class Program {
            main() {
                Foreach (Program::$a[1]._val In 1 .. 10) {
                    Out.printLn("abc");
                }
            }
        }"""
        expect = "Error on line 3 col 36: ["
        self.assertTrue(TestParser.test(input, expect, 284))

    def test_scalar_var11(self):
        input = """Class Program {
            main() {
                Foreach (Program.a::$_val In 1 .. 10) {
                    Out.printLn("abc");
                }
            }
        }"""
        expect = "Error on line 3 col 34: ::"
        self.assertTrue(TestParser.test(input, expect, 285))

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
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 286))

    def test_simple_program2(self):
        input = """Class Program {
            main() {
                Var c, h: Int = 50, 30;
                Var d: Int = Math.int(System.input("Enter D: "));
                Var Q: Int = Math.int(2 * c * d / h);
                Out.print(Math.round(Math.sqrt(Q)));
            }
        }"""
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 287))
    
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
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 288))

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
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 289))

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
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 290))

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
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 291))

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
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 292))

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
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 293))

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
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 294))

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
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 295))
    
    def test_complex_program1(self):
        input = """Class Shape {
            Val $numOfShape: Int = 0;
            Val immutableAttribute: Int = 0, 1;
            Var length, width: Int;

            $getNumOfShape() {
                Return Self::$numOfShape;
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
        expect = "Error on line 3 col 43: ,"
        self.assertTrue(TestParser.test(input, expect, 296))

    
    def test_complex_program2(self):
        input = """Class Shape {
            Val $numOfShape: Int = 0;
            Val immutableAttribute: Int = 0;
            Var length, width: Int;

            $getNumOfShape() {
                Return Self::$numOfShape;
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
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 297))

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
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 298))

    def test_complex_program4(self):
        input = """Class Shape {
            Val $numOfShape: Int = 0;
            Val immutableAttribute: Int = 0;
            Var length, width: Int;
            Var a : Array[Int, 3] = Array(1 + 1, 2, 3);

            $getNumOfShape() {
                Return $numOfShape;
            }
        }

        Class Program{
            main(){
                Var a : Int = 12;
                If (a + 1 == 9){
                    a = b = c = d = Self.Pi; 
                    Foreach(i In 1 .. 100 By 2){
                        a = a[1 + 2 + 3];
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
        expect = "Error on line 8 col 23: $numOfShape"
        self.assertTrue(TestParser.test(input, expect, 299))

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
        expect = "successful"
        self.assertTrue(TestParser.test(input, expect, 300))