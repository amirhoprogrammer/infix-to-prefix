from structures.stack import Stack
from structures.tree import Tree

def generate(postfix):
    stack = Stack()
    depth: int = 0
    for c7 in postfix:
        if c7.isalnum():
            tree = Tree(c7)
            stack.push(tree)
        else:
            right = stack.pop()
            left = stack.pop()
            depth = left.depth if left.depth > right.depth else right.depth
            tree = Tree(c7, left, right, depth=depth+1)
            stack.push(tree)
    return stack.pop()