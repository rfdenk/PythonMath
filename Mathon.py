import sys
from functools import reduce

from Node import *


def test() -> bool:
    root = NumberNode(0)
    
    root = root.append(NumberNode(3))
    # 3
    root = root.append(NumberNode(6))
    # 36
    if root.evaluate() != 36:
        root.squawk()
        return False
        
    root = root.append(AdditionOperatorNode(0))
    # 36+
    
    root = root.append(NumberNode(4))
    # 36+4
    if root.evaluate() != 40: 
        root.squawk()
        return False
    
    
    root = root.append(MultiplicationOperatorNode(0))
    # 36+4x
    root = root.append(NumberNode(6))
    # 36+4x6
    if root.evaluate() != 60: 
        root.squawk()
        return False

    return True
    

def processCommand(origRoot, origParenDepth, command):
    
    #clone off the original info.
    #if there is an error, we'll return the original.
    root = origRoot.clone()
    parenDepth = origParenDepth
    
    first = True
    try:
        for k in command:
            if k in ('0','1','2','3','4','5','6','7','8','9'): 
                if first and isinstance(root, NumberNode): 
                    # restart the formula
                    root = NumberNode(int(k))
                else:
                    # continue the formula
                    root = root.append(NumberNode(int(k)))
            elif k == '.': root = root.append(DecimalPointNode())
            elif k == '+': root = root.append(AdditionOperatorNode(parenDepth))
            elif k == '-': root = root.append(SubtractionOperatorNode(parenDepth))
            elif k == 'x': root = root.append(MultiplicationOperatorNode(parenDepth))   # preferred symbol for multiply
            elif k == '*': root = root.append(MultiplicationOperatorNode(parenDepth))   # allowed alternative symbol for multiply
            elif k == '/': root = root.append(DivisionOperatorNode(parenDepth))
            elif k == '%': root = root.append(ModuloOperatorNode(parenDepth))
            elif k == '^': root = root.append(ExponentiationOperatorNode(parenDepth))
            elif k == '(':
                parenDepth+=1
                if first and isinstance(root, NumberNode):
                    # restart the formula
                    # We need an operator to hold the parenthesized atom as a right child.
                    # We use the "Right" pseudo-operator, that only prints and evaluates its right side.
                    parendepth = 0
                    root = NumberNode(0)
                    root = root.append(RightOperatorNode(0))
                root = root.append(ParenthesisNode(parenDepth))
            elif k == ')': 
                if parenDepth > 0: 
                    root = root.closeParen(parenDepth)
                    parenDepth -= 1
                else:
                    print(") error")
                    raise InvalidOperatorSequenceError()
                    
            first = False
    except:
        print("Error; try again")
        return origRoot,origParenDepth
        
    return root,parenDepth

  
if __name__ == "__main__":

    #built-in-test
    if not test(): quit()
    
    
    root = NumberNode(0)
    
    command = ""
    
    # get the initial command from the command line (skipping the program name...)
    for a in sys.argv[1: ]:
      command += a
      
    print(command)
    print()

    #parenDepth is used to increase the precendence of operators that occur within parentheses
    parenDepth = 0
    
    while 1:
        root,parenDepth = processCommand(root, parenDepth, command)

        try:
            runningValue = root.evaluate()
        except:
            print("Error evaluating; try again");
            root = NumberNode(0)
        
        #print(parenDepth)
        root.squawk()
        print()
        
        # Don't "overcollapse": if parenDepth > 0, don't evaluate the contents of those parentheses
        root = root.collapse(parenDepth)
        # Show the current "running" tree, to which the user may append operations.
        root.squawk2()

        try:
            command = sys.stdin.readline()
        except:
            print()
            print()
            print("Bye!")
            quit()
        
    
    
    
