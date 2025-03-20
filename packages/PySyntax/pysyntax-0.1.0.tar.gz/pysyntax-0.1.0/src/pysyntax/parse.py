from typing import Any as _Any
import ast as _ast


def function_call(code: str) -> tuple[str, dict[str, _Any]]:
    """
    Parse a Python function call from a string.

    Parameters
    ----------
    code : str
        The code to parse.

    Returns
    -------
    tuple[str, dict[str, Any]]
        A tuple containing the function name and a dictionary of keyword arguments.
    """

    class CallVisitor(_ast.NodeVisitor):

        def visit_Call(self, node):
            # Function name
            self.func_name = getattr(node.func, 'id', None)
            # Keyword arguments
            self.args = {arg.arg: self._arg_value(arg.value) for arg in node.keywords}

        def _arg_value(self, node):
            if isinstance(node, _ast.Constant):
                return node.value
            elif isinstance(node, (_ast.List, _ast.Tuple, _ast.Dict)):
                return _ast.literal_eval(node)
            return "Complex value"  # Placeholder for complex expressions

    tree = _ast.parse(code)
    visitor = CallVisitor()
    visitor.visit(tree)
    return visitor.func_name, visitor.args


def docstring(code: str) -> str | None:
    """Extract docstring from a Python module, class, or function content.

    Parameters
    ----------
    code : str
        The code to parse.

    Returns
    -------
    str or None
        The module docstring or None if not found.
    """
    tree = _ast.parse(code)
    return _ast.get_docstring(tree, clean=False)


def imports(code: str) -> list[str]:
    """Extract import statements from a Python module content.

    Parameters
    ----------
    code
        The code to parse.

    Returns
    -------
    A list of imported module names.
    """
    tree = _ast.parse(code, filename='<string>')
    imported_modules = []
    for node in _ast.walk(tree):
        if isinstance(node, _ast.Import):
            for alias in node.names:
                imported_modules.append(alias.name)
        elif isinstance(node, _ast.ImportFrom):
            if node.module:  # Sometimes this can be None (for relative imports)
                imported_modules.append(node.module)
    return imported_modules


def object_definition_lines(code: str, object_name: str) -> tuple[int, int | None] | None:
    """Get the line numbers of an object definition in the source file.

    Parameters
    ----------
    filepath
        Path to the source file.
    object_name
        Name of the object to find in the source file.

    Returns
    -------
    Start and end line numbers of the object definition.
    End line number is `None` if the object definition is a single line.
    If the object is not found, `None` is returned.
    """
    tree = _ast.parse(code, filename="<string>")
    for node in _ast.walk(tree):
        # Check for class or function definitions
        if isinstance(
            node,
            (_ast.ClassDef, _ast.FunctionDef, _ast.AsyncFunctionDef)
        ) and node.name == object_name:
            return node.lineno, getattr(node, 'end_lineno', None)
        # Check for variable assignments (without type annotations)
        if isinstance(node, _ast.Assign):
            for target in node.targets:
                if isinstance(target, _ast.Name) and target.id == object_name:
                    return node.lineno, getattr(node, 'end_lineno', None)
        # Check for variable assignments (with type annotations)
        if isinstance(node, _ast.AnnAssign):
            target = node.target
            if isinstance(target, _ast.Name) and target.id == object_name:
                return node.lineno, getattr(node, 'end_lineno', None)
    return


def header_comments(code: str) -> list[str]:
    """Extract header comments from a Python module content.

    Parameters
    ----------
    code
        The code to parse.

    Returns
    -------
    str
        The header comments from the module content.
    """
    lines = code.splitlines()
    header_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#') or stripped == '':
            header_lines.append(line)
        else:
            break
    return header_lines