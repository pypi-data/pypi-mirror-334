from functools import reduce
import operator


def make_tex(type=None, *args, ctx=None):

    apply_tab = lambda string :'\n'.join(map(lambda s: '\t\t' + s, string.split('\n')))

    if ctx is None:
        ctx = []

    _basic_header = """\\documentclass{article}
\\usepackage{graphicx}
\\usepackage{float}

\\begin{document}"""

    _basic_footer = "\\end{document}\n"


    def add_header(header=None):
        if header is None:
            header = _basic_header
        ctx.append(header)
    
    def add_footer(footer=None):
        if footer is None:
            footer = _basic_footer
        ctx.append(footer)

    def add_table(table):
        tex_table = ''
        row_len = len(table[0])
        table_format_string = '|' + 'c|'*row_len
        table_begin = """\\begin{table}[h]
    \centering
    \\begin{tabular}{%s}""" % (table_format_string)
        table_end = """    \\end{tabular}
\\end{table}"""
        hline = '\n\t\t\\hline\n'
        tab_row = lambda row: '\t\t' + ' & '.join(list(map(str,row))) + '\\\\' + hline
        tex_table = map(tab_row, table)
        # print(reduce(operator.add, tex_table))
        tex_table = hline + reduce(operator.add, tex_table)
        tmp_string = table_begin + tex_table + table_end
        ctx.append(apply_tab(tmp_string))
    
    def add_picture(picture, width=0.25):
        s = """\\begin{figure}[H]
\\centering
\\includegraphics[width=%.2f\\linewidth]{%s}
\\end{figure}""" % (width, picture)
        ctx.append(apply_tab(s))
    
    def add_with_ctx(type,*args):
        return make_tex(type,*args,ctx=ctx)
    
    def finalize():
        return '\n\n'.join(ctx)
    if type is None:
        return add_with_ctx
    if type == 'finalize':
        return finalize()
    elif type == 'header':
        add_header(*args)
        return add_with_ctx
    elif type == 'footer':
        add_footer(*args)
        return add_with_ctx
    elif type == 'table':
        add_table(*args)
        return add_with_ctx
    elif type == 'picture':
        add_picture(*args)
        return add_with_ctx
    else:
        raise SyntaxError("Unknown operation")