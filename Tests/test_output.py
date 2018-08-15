#!/usr/bin/python

import unittest
from subprocess import PIPE, STDOUT, Popen

from lxml import etree


class OutputTests(unittest.TestCase):
    def validate_xml_tree(self, tex_input, expected):
        p = Popen(
            ['../blahtex', '--mathml', '--spacing', 'moderate'],
            stdout=PIPE,
            stdin=PIPE,
            stderr=STDOUT
        )
        
        p.stdin.write(tex_input.encode())
        p.stdin.close()
        p.wait()
        
        parser = etree.XMLParser(remove_blank_text=True)
        
        actual = p.stdout.read()
        
        root_node = etree.XML(actual, parser=parser)
        expected_root_node = etree.XML(expected, parser=parser)
        
        o1 = etree.tostring(root_node)
        o2 = etree.tostring(expected_root_node)
        
        self.assertEquals(o1, o2)


class TextTests(OutputTests):
    def test_raw_text(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mi>t</mi><mi>e</mi><mi>s</mi><mi>t</mi></mrow>
            </math>
        """
        
        self.validate_xml_tree("test", output)
    
    def test_raw_text2(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mi>c</mi><mi>o</mi><mi>m</mi><mi>p</mi><mi>u</mi><mi>t</mi><mi>e</mi><mo stretchy="false">(</mo><mi>T</mi><mo stretchy="false">)</mo></mrow>
            </math>
        """
        
        self.validate_xml_tree("compute(T)", output)


class ExpressionTests(OutputTests):
    def test_expr(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mi>n</mi><mo>=</mo><mn>1</mn></mrow>
            </math>
        """
        
        self.validate_xml_tree("n = 1", output)
    
    def test_expr2(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mi>n</mi><mo>=</mo><mn>1</mn><mo>,</mo><mo>.</mo><mo>.</mo><mo>.</mo><mo>,</mo><mi>k</mi><mo>-</mo><mn>1</mn></mrow>
            </math>
        """
        
        self.validate_xml_tree("n = 1, ... , k - 1", output)
    
    def test_expr3(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mi>n</mi><mo>&#8800;</mo><mn>3</mn></mrow>
            </math>
        """
        
        self.validate_xml_tree("n \\neq 3", output)
    
    def test_expr4(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mo>&#x2264;</mo><mi>m</mi></mrow>
            </math>
        """
        
        self.validate_xml_tree("\\leq m", output)
    
    def test_expr5(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mi>x</mi><mi>y</mi><mo>=</mo><mi>s</mi><mi>t</mi></mrow>
            </math>
        """
        
        self.validate_xml_tree("xy = st", output)


class EquationTests(OutputTests):
    def test_eq(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mi>n</mi><mo>=</mo><msup><mn>2</mn><mrow><mi>h</mi><mo>+</mo><mn>1</mn></mrow></msup><mo>-</mo><mn>1</mn></mrow>
            </math>
        """
        
        self.validate_xml_tree("n = 2^{h+1} - 1", output)
    
    def test_eq2(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mi>&#x3b8;</mi><mo stretchy="false">(</mo><mi>n</mi><mo stretchy="false">)</mo><mo>=</mo><mi>&#x3b8;</mi><mo stretchy="false">(</mo><msup><mn>2</mn><mrow><mi>h</mi><mo>+</mo><mn>1</mn></mrow></msup><mo>-</mo><mn>1</mn><mo stretchy="false">)</mo></mrow>
            </math>
        """
        
        self.validate_xml_tree("\\theta(n) = \\theta(2^{h+1} - 1)", output)
    
    def test_eq3(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mi>S</mi><mo>=</mo><mi>G</mi><mo>-</mo><mo stretchy="false">{</mo><mi>e</mi><mo stretchy="false">}</mo></mrow>
            </math>
        """
        
        self.validate_xml_tree("S = G - \\{ e \\}", output)
    
    def test_eq4(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><msub><mi>&#x03BB;</mi><mi>S</mi></msub><mo>=</mo><mn>3</mn><mi>k</mi><mo>,</mo><mi>k</mi><mo>&#x2208;</mo><msup><mi mathvariant="double-struck">Z</mi><mo>+</mo></msup></mrow>
            </math>
        """
        
        self.validate_xml_tree("\\lambda_S = 3k, k \\in \\mathbb{Z}^+", output)
        self.validate_xml_tree("\\lambda_S = 3k, k \\in \\mathbb{Z}^{+}", output)
    
    def test_eq5(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><msub><mi>&#x03BB;</mi><mrow><mi>S</mi><mn>2</mn></mrow></msub><mo>=</mo><mn>3</mn><mi>b</mi></mrow>
            </math>
        """
        
        self.validate_xml_tree("\\lambda_{S2} = 3b", output)
    
    def test_eq_long(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mn>2</mn><mo stretchy="false">(</mo><mi>k</mi><mo>-</mo><mn>1</mn><mo stretchy="false">)</mo><mo>-</mo><mn>1</mn><mo>+</mo><mn>2</mn><mo>=</mo><mn>2</mn><mi>k</mi><mo>-</mo><mn>2</mn><mo>-</mo><mn>1</mn><mo>+</mo><mn>2</mn><mo>=</mo><mn>2</mn><mi>k</mi><mo>-</mo><mn>1</mn></mrow>
            </math>
        """
        
        self.validate_xml_tree("2(k - 1) - 1 + 2 = 2k - 2 - 1 + 2 = 2k - 1", output)

class SymbolTests(OutputTests):
    def test_theta(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mi>&#x3b8;</mi><mo stretchy="false">(</mo><mi>n</mi><mo stretchy="false">)</mo></mrow>
            </math>
        """
        
        self.validate_xml_tree("\\theta(n)", output)
    
    def test_theta2(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mi>&#x3b8;</mi><mo stretchy="false">(</mo><msup><mn>2</mn><mi>h</mi></msup><mo stretchy="false">)</mo></mrow>
            </math>
        """
        
        self.validate_xml_tree("\\theta(2^h)", output)
    
    def test_fact(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mn>10</mn><mo>!</mo><mo>-</mo><mi>n</mi><mo>=</mo><mn>11</mn><mo>*</mo><mi>b</mi></mrow>
            </math>
        """
        
        self.validate_xml_tree("10! - n = 11*b", output)
    
    def test_cup(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mo stretchy="false">|</mo><mi>A</mi><mo>&#x222A;</mo><mi>B</mi><mo>&#x222A;</mo><mi>C</mi><mo stretchy="false">|</mo><mo>=</mo><mo stretchy="false">|</mo><mi>A</mi><mo stretchy="false">|</mo><mo>+</mo><mo stretchy="false">|</mo><mi>B</mi><mo stretchy="false">|</mo><mo>+</mo><mo stretchy="false">|</mo><mi>C</mi><mo stretchy="false">|</mo><mo>-</mo><mo stretchy="false">|</mo><mi>A</mi><mo>&#x2229;</mo><mi>B</mi><mo stretchy="false">|</mo><mo>-</mo><mo stretchy="false">|</mo><mi>B</mi><mo>&#x2229;</mo><mi>C</mi><mo stretchy="false">|</mo><mo>-</mo><mo stretchy="false">|</mo><mi>A</mi><mo>&#x2229;</mo><mi>C</mi><mo stretchy="false">|</mo><mo>+</mo><mo stretchy="false">|</mo><mi>A</mi><mo>&#x2229;</mo><mi>B</mi><mo>&#x2229;</mo><mi>C</mi><mo stretchy="false">|</mo></mrow>
            </math>
        """
        
        self.validate_xml_tree("| A \cup B \cup C | = | A | + | B | + | C | - | A \cap B | - | B \cap C | - | A \cap C | + | A \cap B \cap C |", output)


class VariableTests(OutputTests):
    def test_variables(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mi>x</mi><mo>,</mo><mi>y</mi><mo>,</mo><mi>s</mi><mo>,</mo><mi>t</mi><mo>,</mo><mi>m</mi><mo>,</mo><mi>n</mi><mo>&#x2208;</mo><mi mathvariant="double-struck">R</mi></mrow>
            </math>
        """
        
        self.validate_xml_tree("x, y, s, t, m, n \\in \\mathbb{R}", output)
    
    def test_variables2(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mi>f</mi><mo>:</mo><mi mathvariant="double-struck">N</mi><mo>&#x2192;</mo><mi mathvariant="double-struck">N</mi></mrow>
            </math>
        """
        
        self.validate_xml_tree("f : \\mathbb{N} \\rightarrow \\mathbb{N}", output)
        
    def test_variables3(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mi>g</mi><mo>:</mo><msup><mi mathvariant="double-struck">N</mi><mn>2</mn></msup><mo>&#x2192;</mo><mi mathvariant="double-struck">Z</mi></mrow>
            </math>
        """
        
        self.validate_xml_tree("g : \\mathbb{N}^2 \\rightarrow \\mathbb{Z}", output)

class FunctionTests(OutputTests):
    def test_function(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <mrow><mi>g</mi><mo stretchy="false">(</mo><mi>m</mi><mo>,</mo><mi>n</mi><mo stretchy="false">)</mo><mo>=</mo><mo stretchy="false">(</mo><mn>2</mn><mo>-</mo><mi>n</mi><mo stretchy="false">)</mo><mi>f</mi><mo stretchy="false">(</mo><mi>m</mi><mo stretchy="false">)</mo></mrow>
            </math>
        """
        
        self.validate_xml_tree("g(m,n) = (2 - n) f(m)", output)

class ScriptTests(OutputTests):
    def test_subscript(self):
        output = """
            <math xmlns="http://www.w3.org/1998/Math/MathML">
            <msub><mi>W</mi><mn>3</mn></msub>
            </math>
        """
        
        self.validate_xml_tree("W_3", output)

if __name__ == '__main__':
    unittest.main()
