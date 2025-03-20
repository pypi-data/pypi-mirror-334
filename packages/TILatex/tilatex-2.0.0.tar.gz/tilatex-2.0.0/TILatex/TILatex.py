from functools import wraps


def _tex_header(packages: list[str]) -> str:
    packages_str = "\n".join(f"\\usepackage{pkg}" for pkg in packages)
    return f"\\documentclass{{article}}\n{packages_str}\n\\begin{{document}}\n"


def _tex_footer() -> str:
    return f"\n\\end{{document}}\n"


def latex_env_decorator(packages: list[str]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            content = func(*args, **kwargs)
            return f"{_tex_header(packages)}" f"\n{content}\n" f"{_tex_footer()}"

        return wrapper

    return decorator


def _escape_special(path) -> str:
    return str(path).replace("_", r"\_")


def _format_table_header(header_row, max_length: int = 25) -> str:
    processed = [_escape_special(cell)[:max_length] for cell in header_row]
    return " & ".join(processed) + " \\\\\n\\hline\\hline\n"


def _format_table_body(data_rows, max_length: int = 25) -> str:
    return "\n".join(" & ".join(_escape_special(cell)[:max_length] for cell in row) + " \\\\" for row in data_rows)


@latex_env_decorator(packages=[f"[margin=1cm]{{geometry}}"])
def generate_latex_table(table) -> str:
    """Convert table to tex string
    Args:
        table: list[list[T]] - table to format, T is something convertible to str
    Return:
        Valid text document with table
    """
    if not table:
        return ""

    num_columns = len(table[0])
    column_spec = f"{{|{'c'*num_columns}|}}"
    header = _format_table_header(table[0])
    body = _format_table_body(table[1:])

    return f"\\begin{{tabular}}{column_spec}\n" f"\\hline\n{header}" f"{body}\n" f"\\hline\n" f"\\end{{tabular}}"


@latex_env_decorator(packages=[f"{{graphicx}}", f"[margin=1cm]{{geometry}}"])
def generate_latex_image(image_path: str, width: str = r"\textwidth", label: str = "") -> str:
    """Convert image to tex string

    Args:
        image_path
        width
        label
    Returns:
        Valid text document with image
    """
    image_path = _escape_special(image_path)
    image_code = f"\\centering\n" f"\\includegraphics[width={width}]{{{image_path}}}\n"

    if label:
        image_code += f"\\label{{{label}}}\n"

    return f"\\begin{{figure}}\n" f"{image_code}\n" f"\\end{{figure}}"
