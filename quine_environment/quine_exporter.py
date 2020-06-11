class QuineExporter:
    def __init__(self, quine_info, export_file):
        self.quine_info = quine_info
        self.export_file = export_file

    def export_quine_info(self):
        print(f"exporting {self.quine_info}")
        with open(self.export_file, 'w') as f:
            for quine in self.quine_info.quine_dict.values():
                f.write(f"hash: {quine.hash}\n")
                f.write(f"livable: {quine.livable}\n")
                f.write(f"parent: {quine.parent}\n")
                f.write(f"children:\n\t")
                pretty_children = ',\n\t'.join(quine.children)
                f.write(f"{pretty_children}\n")
                f.write(f"code:\n{'-' * 80}\n")
                f.write(quine.code)
                f.write(f"{'-' * 80}\n")
                f.write("\n")
