class ImportNode:
    def __init__(self, lib): self.lib = lib.strip('"')

class ExternNode:
    def __init__(self, linkage, name, params): 
        self.linkage, self.name, self.params = linkage, name, params

class ExportFuncNode:
    def __init__(self, name, params, body): 
        self.name, self.params, self.body = name, params, body

class InlineDgmNode:
    def __init__(self, codes): self.codes = codes

class NumberNode: 
    def __init__(self, value): self.value = int(value)
class StringNode:
    def __init__(self, value): self.value = str(value).strip('"')
class VarNode:
    def __init__(self, name): self.name = name
class BinOpNode:
    def __init__(self, left, op, right): self.left, self.op, self.right = left, op, right

class FuncNode:
    def __init__(self, name, params, body, export=False):
        self.name, self.params, self.body, self.export = name, params, body, export

class CallNode:
    def __init__(self, name, args):
        self.name, self.args = name, args

class CallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args  # list of expressions

class FuncNode:
    def __init__(self, name, params, body, export=False):
        self.name, self.params, self.body, self.export = name, params, body, export

class CallNode:
    def __init__(self, func, args):
        self.func, self.args = func, args   # func can be VarNode or FuncNode reference

class ReturnNode:
    def __init__(self, expr): self.expr = expr

class LambdaNode:
    def __init__(self, params, body, captures=None):
        self.params = params
        self.body = body
        self.captures = captures or []

class ClosureNode:
    def __init__(self, fn_name, captures):
        self.fn_name = fn_name
        self.captures = captures  # list of (varname, value)

