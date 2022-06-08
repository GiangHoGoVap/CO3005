import unittest
from TestUtils import TestCodeGen
from AST import *


class CheckCodeGenSuite(unittest.TestCase):
    def test_simple_program(self):
        input = """Class Program{
            main(){
                io::$writeInt(1);
            }
        }"""
        expect = "1"
        self.assertTrue(TestCodeGen.test(input, expect, 500))
