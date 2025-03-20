from string import Template

_TEMPLATE_TABLE = Template("""\\begin{center}
\\begin{tabular}{ $columns } 
\\hline
\t$value
\\hline
\\end{tabular}
\\end{center}
""")

_TEMPLATE_IMAGE = Template("\\includegraphics[width=\\textwidth]{$imagepath}")

def generate_table(table_values):
    rows_len = [len(row) for row in table_values]

    if len(rows_len) == 0 or not all(x == rows_len[0] for x in rows_len):
        raise ValueError("values must be not empty and rows must be of equals len")

    string_values = [map(str, row) for row in table_values]
    formated_rows = [" & ".join(row) for row in string_values]
    formated_values = " \\\\\n\\hline\n\t".join(formated_rows) + " \\\\"
    columns_pattern = "|c" * len(table_values) + "|"

    return _TEMPLATE_TABLE.substitute(columns=columns_pattern, value=formated_values)


def generate_image(imagepath):
    return _TEMPLATE_IMAGE.substitute(imagepath=imagepath)
