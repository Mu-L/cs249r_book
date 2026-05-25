import ast

def add_docstrings_to_file(filepath):
    with open(filepath, "r") as f:
        source = f.read()

    tree = ast.parse(source)
    # This is a bit complex to do cleanly with just AST replacement, but we can do a targeted replace for the main types.
