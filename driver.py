from infixhandler import Infix


def main():
    expr = input(
        "Enter the infix expression "
        "(operators allowed - +, -, /, *, ^, %, (, ); "
        "you can also use whitespace): "
    )

    infix = Infix(expr)
    postfix = infix.topostfix()
    prefix = infix.toprefix()

    print(postfix, prefix)


if __name__ == "__main__":
    main()
