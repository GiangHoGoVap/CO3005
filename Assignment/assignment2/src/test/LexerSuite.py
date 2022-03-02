import unittest
from TestUtils import TestLexer

class LexerSuite(unittest.TestCase):
    def test_lowercase_identifier(self):
        self.assertTrue(TestLexer.test("abc","abc,<EOF>",101))
    def test_uppercase_identifier(self):
        self.assertTrue(TestLexer.test("ABC", "ABC,<EOF>", 102))

    def test_lower_upper_id1(self):
        self.assertTrue(TestLexer.test("aCBbdc","aCBbdc,<EOF>",103))
    def test_lower_upper_id2(self):
        self.assertTrue(TestLexer.test("AaBbCc", "AaBbCc,<EOF>",104))

    def test_mixed_lowercase_id(self):
        self.assertTrue(TestLexer.test("abc123", "abc123,<EOF>", 105))
    def test_mixed_uppercase_id(self):
        self.assertTrue(TestLexer.test("ABC123", "ABC123,<EOF>", 106))

    def test_mixed_id1(self):
        self.assertTrue(TestLexer.test("aAsVN3","aAsVN3,<EOF>",107))
    def test_mixed_id2(self):
        self.assertTrue(TestLexer.test("AaSvn3", "AaSvn3,<EOF>", 108))

    def test_underscore_id1(self):
        self.assertTrue(TestLexer.test("abc_123", "abc_123,<EOF>", 109))
    def test_underscore_id2(self):
        self.assertTrue(TestLexer.test("ABC_123", "ABC_123,<EOF>", 110))
    def test_underscore_id3(self):
        self.assertTrue(TestLexer.test("aBc_d123", "aBc_d123,<EOF>", 111))
    def test_underscore_id4(self):
        self.assertTrue(TestLexer.test("abC_D123", "abC_D123,<EOF>", 112))
    def test_underscore_id5(self):
        self.assertTrue(TestLexer.test("_abc", "_abc,<EOF>", 113))
    def test_underscore_id6(self):
        self.assertTrue(TestLexer.test("abc_", "abc_,<EOF>", 114))
    def test_underscore_id7(self):
        self.assertTrue(TestLexer.test("__ABC", "__ABC,<EOF>", 115))
    def test_underscore_id8(self):
        self.assertTrue(TestLexer.test("__123", "__123,<EOF>", 116))

    def test_dolla_id1(self):
        self.assertTrue(TestLexer.test("$abc_123", "$abc_123,<EOF>", 117))
    def test_dolla_id2(self):
        self.assertTrue(TestLexer.test("$_123abc", "$_123abc,<EOF>", 118))
    def test_dolla_id3(self):
        self.assertTrue(TestLexer.test("$______", "$______,<EOF>", 119))
    def test_dolla_id4(self):
        self.assertTrue(TestLexer.test("$123", "$123,<EOF>", 120))
    
    def test_integer_binary1(self):
        self.assertTrue(TestLexer.test("0b0001", "0b0,00,1,<EOF>",121))
    def test_integer_binary2(self):
        self.assertTrue(TestLexer.test("0B0010", "0B0,010,<EOF>", 122))
    def test_integer_binary3(self):
        self.assertTrue(TestLexer.test("0B0_0", "0B0,_0,<EOF>", 123))
    def test_integer_binary4(self):
        self.assertTrue(TestLexer.test("0B00_", "0B0,0,_,<EOF>", 124))
    def test_integer_binary5(self):
        self.assertTrue(TestLexer.test("0b_00", "0,b_00,<EOF>", 125))
    def test_integer_binary6(self):
        self.assertTrue(TestLexer.test("0_b00", "0,_b00,<EOF>", 126))

    def test_integer_octal1(self):
        self.assertTrue(TestLexer.test("01234567", "01234567,<EOF>", 127))
    def test_integer_octal2(self):
        self.assertTrue(TestLexer.test("00000", "00,00,0,<EOF>", 128))
    def test_integer_octal3(self):
        self.assertTrue(TestLexer.test("000123", "00,0123,<EOF>", 129))
    def test_integer_octal4(self):
        self.assertTrue(TestLexer.test("00_00_", "00,_00_,<EOF>", 130))
    def test_integer_octal5(self):
        self.assertTrue(TestLexer.test("0012_8", "00,128,<EOF>", 131))
    
    def test_integer_decimal1(self):
        self.assertTrue(TestLexer.test("-123", "-,123,<EOF>", 132))
    def test_integer_decimal2(self):
        self.assertTrue(TestLexer.test("1_234_567", "1234567,<EOF>", 133))
    def test_integer_decimal3(self):
        self.assertTrue(TestLexer.test("1_234_567_", "1234567,_,<EOF>", 134))

    def test_integer_hexa1(self):
        self.assertTrue(TestLexer.test("0x0123_456_789_ABC_DEF", "0x0,123456789,_ABC_DEF,<EOF>", 135))
    def test_integer_hexa2(self):
        self.assertTrue(TestLexer.test("0X0123A", "0X0,123,A,<EOF>", 136))
    def test_integer_hexa3(self):
        self.assertTrue(TestLexer.test("0x0_01", "0x0,_01,<EOF>", 137))
    def test_integer_hexa4(self):
        self.assertTrue(TestLexer.test("0xABC_DEF", "0xABCDEF,<EOF>", 138))
    def test_integer_hexa5(self):
        self.assertTrue(TestLexer.test("0x_01AB", "0,x_01AB,<EOF>", 139))
    def test_integer_hexa6(self):
        self.assertTrue(TestLexer.test("0X01_AB_", "0X0,1,_AB_,<EOF>", 140))
    def test_integer_hexa7(self):
        self.assertTrue(TestLexer.test("0_xF11", "0,_xF11,<EOF>", 141))
    def test_integer_hexa8(self):
        self.assertTrue(TestLexer.test("0xF11_", "0xF11,_,<EOF>", 142))
    def test_integer_hexa9(self):
        self.assertTrue(TestLexer.test("0Xabcd", "0,Xabcd,<EOF>", 143))
    def test_integer_hexa10(self):
        self.assertTrue(TestLexer.test("0X1A1a_b", "0X1A1,a_b,<EOF>", 144))
    
    def test_float1(self):
        self.assertTrue(TestLexer.test("1.0234", "1.0234,<EOF>", 145))
    def test_float2(self):
        self.assertTrue(TestLexer.test("000000.000","00,00,00,.,00,0,<EOF>",146))
    def test_float3(self):
        self.assertTrue(TestLexer.test("1.001", "1.001,<EOF>", 147))
    def test_float4(self):
        self.assertTrue(TestLexer.test("1.0e01", "1.0e01,<EOF>", 148))
    def test_float5(self):
        self.assertTrue(TestLexer.test("7E-10", "7E-10,<EOF>", 149))
    def test_float6(self):
        self.assertTrue(TestLexer.test("0.200000", "0.200000,<EOF>", 150))
        # self.assertTrue(TestLexer.test("0.00000000", "0.00000000,<EOF>", 150))
    def test_float7(self):
        self.assertTrue(TestLexer.test("1.2e3", "1.2e3,<EOF>", 151))
    def test_float8(self):
        self.assertTrue(TestLexer.test("1_234.567", "1234.567,<EOF>", 152))
    def test_float9(self):
        self.assertTrue(TestLexer.test("1_2.E-1_0", "12.E-1,_0,<EOF>", 153))
    def test_float10(self):
        self.assertTrue(TestLexer.test("1_.23", "1,_,.,23,<EOF>", 154))
    def test_float11(self):
        self.assertTrue(TestLexer.test("12e01","12e01,<EOF>",155))
    def test_float12(self):
        self.assertTrue(TestLexer.test(".e3", ".e3,<EOF>", 156))
    def test_float13(self):
        self.assertTrue(TestLexer.test(".E+10", ".E+10,<EOF>", 157))
    def test_float14(self):
        self.assertTrue(TestLexer.test(".e-101230xA_F", ".e-101230,xA_F,<EOF>", 158))
    def test_float15(self):
        self.assertTrue(TestLexer.test(".E0b001", ".E0,b001,<EOF>", 159))
    def test_float16(self):
        self.assertTrue(TestLexer.test(".E00b001", ".E00,b001,<EOF>", 160))
    def test_float17(self):
        self.assertTrue(TestLexer.test(".e000X01AB", ".e000,X01AB,<EOF>", 161))

    def test_boolean1(self):
        self.assertTrue(TestLexer.test("True", "True,<EOF>", 162))
    def test_boolean2(self):
        self.assertTrue(TestLexer.test("False", "False,<EOF>", 163))
    def test_boolean3(self):
        self.assertTrue(TestLexer.test("trueFalse", "trueFalse,<EOF>", 164))

    def test_string1(self):
        self.assertTrue(TestLexer.test("\"\"",",<EOF>", 165))
    def test_string2(self):
        self.assertTrue(TestLexer.test("\"Hello World!\"", "Hello World!,<EOF>", 166))
    def test_string3(self):
        self.assertTrue(TestLexer.test("\"He asked me\"\"", "He asked me,Unclosed String: ", 167))
    def test_string4(self):
        self.assertTrue(TestLexer.test("\"Nguyen \\b \\f Minh \\r \\n \\t \\\' \\\\ Tam\"", "Nguyen \\b \\f Minh \\r \\n \\t \\\' \\\\ Tam,<EOF>", 168))
    def test_string5(self):
        self.assertTrue(TestLexer.test("\"He asked me: \'\"Where is John?\'\"\"", "He asked me: \'\"Where is John?\'\",<EOF>", 169))
    def test_string6(self):
        self.assertTrue(TestLexer.test("\"\\b \\' He is my ex's man\"", "\\b \\' He is my ex's man,<EOF>", 170))
    def test_string7(self):
        self.assertTrue(TestLexer.test("\"She is Tam\'s girlfriend.\"", "She is Tam\'s girlfriend.,<EOF>", 171))

    def test_string_unclose1(self):
        self.assertTrue(TestLexer.test("\"He is a man", "Unclosed String: He is a man", 172))
    def test_string_unclosed2(self):
        self.assertTrue(TestLexer.test("\"abc \\n \\f 's def", "Unclosed String: abc \\n \\f 's def", 173))
    def test_string_unclose3(self):
        self.assertTrue(TestLexer.test("\"He is \\b a man", "Unclosed String: He is \\b a man", 174))
    def test_string_unclosed4(self):
        self.assertTrue(TestLexer.test("\"It is a unclosed \\n string", "Unclosed String: It is a unclosed \\n string", 175))
    def test_string_unclosed5(self):
        self.assertTrue(TestLexer.test("\"This is a \\t string \\n containing tab \" \"He asked \\n me: '\"Where '\"is'\" John?'\"\" \"I am not closed", "This is a \\t string \\n containing tab ,He asked \\n me: '\"Where '\"is'\" John?'\",Unclosed String: I am not closed", 176))
    
    def test_string_illegal_esc1(self):
        self.assertTrue(TestLexer.test("\"I have an escape sequence \'\"Here it is \\k\'\"\"", "Illegal Escape In String: I have an escape sequence \'\"Here it is \k", 177))
    def test_string_illegal_esc2(self):
        self.assertTrue(TestLexer.test("\"\\a He is a man\"", "Illegal Escape In String: \\a", 178))
    def test_string_illegal_esc3(self):
        self.assertTrue(TestLexer.test("\"\\\\ He is a \\\\ \\\' 19-year-old man \\a\"", "Illegal Escape In String: \\\\ He is a \\\\ \\\' 19-year-old man \\a", 179))
    
    def test_operator1(self):
        self.assertTrue(TestLexer.test("===", "==,=,<EOF>", 180))
    def test_operator2(self):
        self.assertTrue(TestLexer.test("====", "==,==,<EOF>", 181))
    def test_operator3(self):
        self.assertTrue(TestLexer.test("||||", "||,||,<EOF>", 182))
    def test_operator4(self):
        self.assertTrue(TestLexer.test("[a,1,b]", "[,a,,,1,,,b,],<EOF>", 183))
    def test_operator5(self):
        self.assertTrue(TestLexer.test("*/%::!=!<><===.+.", "*,/,%,::,!=,!,<,>,<=,==.,+.,<EOF>", 184))
    def test_operator6(self):
        self.assertTrue(TestLexer.test("&&&", "&&,Error Token &", 185))
    def test_operator7(self):
        self.assertTrue(TestLexer.test("-12_3", "-,123,<EOF>", 186))
    def test_operator8(self):
        self.assertTrue(TestLexer.test("-0x0123_AEF", "-,0x0,123,_AEF,<EOF>", 187))
    def test_operator9(self):
        self.assertTrue(TestLexer.test("-0b000_1238", "-,0b0,00,_1238,<EOF>", 188))
    def test_operator10(self):
        self.assertTrue(TestLexer.test("-01230x43520b10", "-,01230,x43520b10,<EOF>", 189))

    def test_keyword1(self):
        self.assertTrue(TestLexer.test("Break, Continue, If, Elseif", "Break,,,Continue,,,If,,,Elseif,<EOF>", 190))
    def test_keyword2(self):
        self.assertTrue(TestLexer.test("false", "false,<EOF>", 191))
    def test_keyword3(self):
        self.assertTrue(TestLexer.test("NULL", "NULL,<EOF>", 192))
    
    def test_seperator(self):
        self.assertTrue(TestLexer.test("()[].,;{}", "(,),[,],.,,,;,{,},<EOF>", 193))
    
    def test_for_stmt(self):
        input = """Foreach (i In 1 .. 100 By 2) {
            Out.printInt(i);
        }"""
        expected = "Foreach,(,i,In,1,..,100,By,2,),{,Out,.,printInt,(,i,),;,},<EOF>"
        self.assertTrue(TestLexer.test(input, expected, 194))

    def test_method_invocation_stmt(self):
        input = """Shape::$getNumOfShape();"""
        expected = "Shape,::,$getNumOfShape,(,),;,<EOF>"
        self.assertTrue(TestLexer.test(input, expected, 195))

    def test_block_stmt(self):
        input = """{
            Var r, s: Int;
            r = 2.0;
            Var a, b: Array[Int, 5];
            s = r * r * Self.myPI;
            a[0] = s;
        }"""
        expected = "{,Var,r,,,s,:,Int,;,r,=,2.0,;,Var,a,,,b,:,Array,[,Int,,,5,],;,s,=,r,*,r,*,Self,.,myPI,;,a,[,0,],=,s,;,},<EOF>"
        self.assertTrue(TestLexer.test(input, expected, 196))

    def test_comment1(self):
        input = """## This is a 
            multi-line 
            comment.##"""
        expected = "<EOF>"
        self.assertTrue(TestLexer.test(input, expected, 197))

    def test_comment2(self):
        input = "### This is a comment. ###"
        expected = "Error Token #"
        self.assertTrue(TestLexer.test(input, expected, 198))
    
    def test_dot(self):
        self.assertTrue(TestLexer.test("1.....1", "1.,..,..,1,<EOF>", 199))

    def test_random1(self):
        self.assertTrue(TestLexer.test("Val a : String = \"", "Val,a,:,String,=,Unclosed String: ", 200))