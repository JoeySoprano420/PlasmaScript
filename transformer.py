class PlasmaTransformer(Transformer):
    def import_stmt(self, items):
        return ImportNode(str(items[0]))
    def extern_decl(self, items):
        linkage = str(items[0]).strip('"')
        name = str(items[1])
        params = [str(x) for x in items[2:]] if len(items) > 2 else []
        return ExternNode(linkage, name, params)
    def export_def(self, items):
        name = str(items[0])
        params = [str(x) for x in items[1].children] if hasattr(items[1], "children") else []
        body = items[-1]
        return ExportFuncNode(name, params, body)
    def inline_dgm(self, items):
        codes = []
        for dgm in items:
            codes.extend(dgm)  # flatten
        return InlineDgmNode(codes)
    def dgm_call(self, items):
        return [int(str(x)) for x in items]
