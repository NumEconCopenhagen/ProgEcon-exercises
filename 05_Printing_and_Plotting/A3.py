def write_table(filename, table):
    """(a) Write the table to a file. 'w' creates the file or replaces an existing one."""
    with open(filename, 'w') as f:
        f.write(table + '\n')  # gen_table has no final line shift, so add one


def append_parameters(filename, alpha, beta):
    """(b) Add one line at the end of the file. 'a' keeps the old content."""
    with open(filename, 'a') as f:
        f.write(f'alpha = {alpha:.2f}, beta = {beta:.2f}\n')


def read_and_print(filename):
    """(c) Read the whole file and print it."""
    with open(filename, 'r') as f:
        content = f.read()
    print(content, end='')  # the file already ends with a line shift


def write_latex(filename, x1_vec, x2_vec, u_func):
    """(e) Write the same numbers as rows of a LaTeX table."""
    with open(filename, 'w') as f:
        for x1 in x1_vec:
            cells = ' & '.join([f'{u_func(x1, x2):.3f}' for x2 in x2_vec])  # 'a & b & c'
            f.write(fr'{x1:.1f} & {cells} \\' + '\n')  # fr = raw f-string: \\ stays \\
