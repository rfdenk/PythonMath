import unittest
from Node import *
from Mathon import processCommand

class TestNode(unittest.TestCase):
    
    def testManual(self):
        root = NumberNode(0)
    
        root = root.append(NumberNode(3))
        self.assertTrue(root.evaluate() == 3)
        root = root.append(NumberNode(6))
        self.assertTrue(root.evaluate() == 36)
        
        root = root.append(AdditionOperatorNode(0))
        # 36+
        self.assertTrue(root.describe() == '36+')
    
        root = root.append(NumberNode(4))
        # 36+4
        self.assertTrue(root.evaluate() == 40)
        self.assertTrue(root.describe() == '36+4')
    
        root = root.append(MultiplicationOperatorNode(0))
        # 36+4x
        self.assertTrue(root.describe() == '36+4x')
        root = root.append(NumberNode(6))
        # 36+4x6
        self.assertTrue(root.evaluate() == 60)

    def testString1(self):
        root = NumberNode(0)
        parenDepth = 0;
        root,parenDepth = processCommand(root, 0, "4+6")
        self.assertTrue(parenDepth==0)
        self.assertTrue(root.evaluate() == 10)
        
    def testStringWithPrecedence(self):
        root = NumberNode(0)
        parenDepth = 0;
        root,parenDepth = processCommand(root, 0, "4+6x4")
        self.assertTrue(parenDepth==0)
        self.assertTrue(root.evaluate() == 28)
        
    def testStringWithParens(self):
        root = NumberNode(0)
        parenDepth = 0;
        root,parenDepth = processCommand(root, parenDepth, "4 x (6 + 4)")
        self.assertTrue(parenDepth==0)
        self.assertTrue(root.evaluate() == 40)
        self.assertTrue(root.describe() == '4x(6+4)')
        
    def testStringWithParens2(self):
        root = NumberNode(0)
        parenDepth = 0;
        root,parenDepth = processCommand(root, parenDepth, "4 x (6")
        self.assertTrue(parenDepth==1)
        self.assertTrue(root.describe() == '4x(6')
        
        root,parenDepth = processCommand(root, parenDepth, '+4')
        self.assertTrue(parenDepth == 1)
        self.assertTrue(root.describe() == '4x(6+4')
        
        root,parenDepth = processCommand(root, parenDepth, ')')
        self.assertTrue(parenDepth == 0)
        self.assertTrue(root.describe() == '4x(6+4)')
        self.assertTrue(root.evaluate() == 40)
        
    def testStartWithParen(self):
        root = NumberNode(0)
        parenDepth=0
        root,parenDepth=processCommand(root, parenDepth, '(4+5)')
        self.assertTrue(parenDepth == 0)
        self.assertTrue(root.describe() == '(4+5)')
        self.assertTrue(root.evaluate() == 9)
        
    def testAddNegative(self):
        root = NumberNode(0)
        parenDepth=0
        root,parenDepth=processCommand(root, parenDepth, '4+-3')
        self.assertTrue(parenDepth == 0)
        self.assertTrue(root.describe() == '4+-3')
        self.assertTrue(root.evaluate() == 1)
        
    def testParen1(self):
        root = NumberNode(0)
        parenDepth=0
        root,parenDepth=processCommand(root, parenDepth, '(4+3)x5')

        self.assertTrue(parenDepth == 0)
        self.assertTrue(root.describe() == '(4+3)x5')
        self.assertTrue(root.evaluate() == 35)
        
    def testParen2(self):
        root = NumberNode(0)
        parenDepth=0
        root,parenDepth=processCommand(root, parenDepth, '2x(4+3)')
        self.assertTrue(parenDepth == 0)
        self.assertTrue(root.describe() == '2x(4+3)')
        self.assertTrue(root.evaluate() == 14)
        
    def testParen3(self):
        root = NumberNode(0)
        parenDepth=0
        root,parenDepth=processCommand(root, parenDepth, '1+(4+3)x5')

        self.assertTrue(parenDepth == 0)
        self.assertTrue(root.describe() == '1+(4+3)x5')
        self.assertTrue(root.evaluate() == 36)
        
    def testAppendToParen(self):
        root = NumberNode(0)
        parenDepth=0
        root,parenDepth=processCommand(root, parenDepth, '(4+3)')
        self.assertTrue(parenDepth == 0)
        self.assertTrue(root.describe() == '(4+3)')
        self.assertTrue(root.evaluate() == 7)
        
        root,parenDepth=processCommand(root, parenDepth, 'x5')
        self.assertTrue(parenDepth == 0)
        self.assertTrue(root.describe() == '(4+3)x5')
        self.assertTrue(root.evaluate() == 35)
        
    def testStartWithNegativeParen(self):
        root = NumberNode(0)
        parenDepth=0
        root,parenDepth=processCommand(root, parenDepth, '-(4+3)')
        self.assertTrue(parenDepth == 0)
        self.assertTrue(root.describe() == '0-(4+3)')
        self.assertTrue(root.evaluate() == -7)
        
        root,parenDepth=processCommand(root, parenDepth, 'x5')
        self.assertTrue(parenDepth == 0)
        self.assertTrue(root.describe() == '0-(4+3)x5')
        self.assertTrue(root.evaluate() == -35)
        
    def testTwoParens(self):
        root = NumberNode(0)
        parenDepth=0
        root,parenDepth = processCommand(root, parenDepth,"(4+3)x(3+5)")
        self.assertTrue(parenDepth == 0)
        self.assertTrue(root.describe() == "(4+3)x(3+5)")
        self.assertTrue(root.evaluate() == 56)
        
    def testNestedParens(self):
        root = NumberNode(0)
        parenDepth=0
        root,parenDepth = processCommand(root, parenDepth,"4x(4+(3x5))")
        self.assertTrue(parenDepth == 0)
        self.assertTrue(root.describe() == "4x(4+(3x5))")
        self.assertTrue(root.evaluate() == 76)
    
if __name__ == '__main__':
  unittest.main()
  
  

