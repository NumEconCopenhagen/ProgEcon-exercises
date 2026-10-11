def gen_table(x1_vec, x2_vec, u_func):
    """Return a text table of u(x1,x2): x2 values in the header, x1 values in the left column.
    u_func is passed in as an argument, so the function does not rely on any global variable."""

    # a. empty text
    text = ''

    # b. top header: empty corner, then the x2 values
    text += f'{"":8s}'
    for x2 in x2_vec:
        text += f'{x2:8.1f}'
    text += '\n'  # line shift

    # c. body: one row per x1 value
    for i, x1 in enumerate(x1_vec):
        if i > 0:
            text += '\n'  # line shift between rows (none after the last row)
        text += f'{x1:8.1f}'  # left header: the x1 value
        for x2 in x2_vec:
            text += f'{u_func(x1, x2):8.3f}'

    return text
