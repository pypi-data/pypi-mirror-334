import re as _re

import pysyntax as _pysyntax


def imports(code: str, mapping: dict[str, str]) -> str:
    """
    Rename imports in a module.

    Parameters
    ----------
    code : str
        The content of the Python module as a string.
    mapping : dict[str, str]
        A dictionary mapping the old import names to the new import names.

    Returns
    -------
    new_module_content : str
        The updated module content as a string with the old names replaced by the new names.
    """
    updated_module_content = code
    for old_name, new_name in mapping.items():
        # Regular expression patterns to match the old name in import statements
        patterns = [
            rf"^\s*from\s+{_re.escape(old_name)}(?:.[a-zA-Z0-9_]+)*\s+import",
            rf"^\s*import\s+{_re.escape(old_name)}(?:.[a-zA-Z0-9_]+)*",
        ]
        for pattern in patterns:
            # Compile the pattern into a regular expression object
            regex = _re.compile(pattern, flags=_re.MULTILINE)
            # Replace the old name with the new name wherever it matches
            updated_module_content = regex.sub(
                lambda match: match.group(0).replace(old_name, new_name, 1), updated_module_content
            )
    return updated_module_content


def docstring(code: str, new_docstring, quotes: str = '"""'):
    """
    Replaces the existing module docstring with new_docstring, or adds it if none exists.

    Parameters:
        code (str): The content of the Python file as a string.
        new_docstring (str): The new docstring to replace or add.

    Returns:
        str: The modified file content.
    """
    existing_docstring = _pysyntax.parse.docstring(code)
    if existing_docstring is not None:
        # Replace the existing docstring with the new one
        return code.replace(existing_docstring, new_docstring, 1)

    lines = code.splitlines()
    insert_pos = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('#') or stripped == '':
            insert_pos = i + 1
        else:
            break
    whitespace_before = "\n" if insert_pos != 0 and lines[insert_pos - 1].strip() else ""
    whitespace_after = "\n" if insert_pos != len(lines) and lines[insert_pos].strip() else "\n"
    lines.insert(insert_pos, f'{whitespace_before}{quotes}{new_docstring}{quotes}{whitespace_after}')
    return '\n'.join(lines)


def header_comments(code: str, new_comments: str, empty_lines: int = 1):
    """Replace or add header comments to a Python module content.

    Parameters
    ----------
    code
        Python module content as a string.
    new_comments
        New header comments to replace or add.
    empty_lines
        Number of empty lines to add after the header comments.

    Returns
    -------
    The modified module content.
    """
    existing_comments = _pysyntax.parse.header_comments(code)
    if existing_comments:
        # Replace the existing header comments with the new ones
        return code.replace(
            "\n".join(existing_comments),
            f"{new_comments.rstrip()}{"\n" * empty_lines}",
            1
        )
    return f"{new_comments.rstrip()}{"\n" * (empty_lines + 1)}{code}"
