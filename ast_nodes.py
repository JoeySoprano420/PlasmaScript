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

