import sys


def get(vrs, v) -> int:
    if v.isdigit():
        return int(v)
    else:
        return int(vrs[v])


def main(f, skip=False, variables=None, funcs=None) -> int:
    variables = variables or dict()
    funcs = funcs or dict()

    for i, (first, *string) in enumerate(f):
        if skip:
            skip = first != "return"
            continue
        
        # Match/case statement must be used here with Python version >= 3.10
        if first == "function":
            skip = True
            funcs[string[0]] = {"args": string[1:], "body": f[i + 1:]}

        elif first == "init":
            variables[string[0]] = get(variables, string[1])

        elif first == "return":
            return get(variables, string[0])

        elif first == "end_program":
            sys.exit()

        elif first in ("add", "sub", "mul", "div"):
            variables[string[0]] = {
                "add": lambda x, y: x + y,
                "sub": lambda x, y: x - y,
                "mul": lambda x, y: x * y,
                "div": lambda x, y: x // y,
            }[first](variables[string[0]], get(variables, string[1]))

        else:  # call custom function
            temp_vs = {key: get(variables, val) for key, val in zip(funcs[first]["args"], string)}
            variables[string[0]] = main(funcs[first]["body"], skip=False, variables=temp_vs, funcs=funcs)


if __name__ == "__main__":
    print(main([i.rstrip('\n').split() for i in sys.stdin.readlines() if i != '\n']))
