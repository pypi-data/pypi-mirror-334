from typing import Any


def create_raw(raw: list[Any]) -> str:
    return ' & '.join(map(str, raw))


def tabular(raw: list[list[Any]]) -> str:
    return '|c' * len(raw[0]) + '|'


def create_table(input_data: list[list[Any]]) -> str:
    return """
\\begin{{table}}
\\begin{{tabular}}{{{0}}}
\\hline
{1}\\\\
\\hline
\end{{tabular}}
\end{{table}}
""".format(tabular(input_data), '\\\\\\hline\n'.join(map(create_raw, input_data)))


def create_img(path: str) -> str:
    return """
\\begin{{figure}}
\\centering
\\includegraphics[width=0.25\\linewidth]{{{}}}
\\end{{figure}}
""".format(path)