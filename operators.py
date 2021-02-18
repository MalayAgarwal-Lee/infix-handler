OPERATORS = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '%': 2,
    '^': 3,
    'UMINUS': 4,
    '(': 0,
    ')': None,
}


def operator_map(op, left_opr, right_opr=None):
    '''
    Function to map an operator to its equivalent Python operation

    It avoids if statements by using a dictionary look-up in its place

    Arguments:
        op: str, the operator which needs to be mapped
        left_opr: int, the left operand for the operator
        right_opr: int or None, the right operand for the operator
                   None implies that op is unary

    Returns:
        The numeric value obtained by performing the operation

    Raises:
        KeyError when an unsupported operand is passed
    '''
    return {
        '+': left_opr + right_opr,
        '-': left_opr - right_opr,
        '*': left_opr * right_opr,
        '/': left_opr / right_opr,
        '%': left_opr % right_opr,
        '^': left_opr ** right_opr,
        'UMINUS': -left_opr,
    }[op]
