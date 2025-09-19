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
