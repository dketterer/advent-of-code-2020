class Parser:
    """
    Most is taken from Wikipedia: https://de.wikipedia.org/wiki/Rekursiver_Abstieg#Beispiel
    """
    def __init__(self, part):
        if part == 'part1':
            self.expression = self.expression_part1
        else:
            self.expression = self.expression_part2

    @staticmethod
    def scan(s):
        a = []
        i = 0
        n = len(s)
        while i < n:
            if s[i] in "+-*()":
                a.append(s[i])
                i += 1
            elif s[i].isdigit():
                j = i
                while i < n and s[i].isdigit(): i += 1
                a.append(int(s[j:i]))
            elif s[i].isspace():
                i += 1
        a.append(None)
        return a

    def atom(self, a, i):
        t = a[i]
        if isinstance(t, int):
            return i + 1, a[i]
        elif t == "(":
            i, x = self.expression(a, i + 1)
            return i + 1, x

    def negation(self, a, i):
        if a[i] == "-":
            i, x = self.atom(a, i + 1)
            return i, ["~", x]
        else:
            return self.atom(a, i)

    def multiplication(self, a, i):
        i, x = self.addition(a, i)
        op = a[i]
        while op == "*" or op == "/":
            i, y = self.addition(a, i + 1)
            x = [op, x, y]
            op = a[i]
        return i, x

    def addition(self, a, i):
        i, x = self.negation(a, i)
        op = a[i]
        while op == "+" or op == "-":
            i, y = self.negation(a, i + 1)
            x = [op, x, y]
            op = a[i]
        return i, x

    def add_mul(self, a, i):
        i, x = self.negation(a, i)
        op = a[i]
        while op == "+" or op == "-" or op == "*" or op == "/":
            i, y = self.negation(a, i + 1)
            x = [op, x, y]
            op = a[i]
        return i, x

    def expression_part1(self, a, i):
        return self.add_mul(a, i)

    def expression_part2(self, a, i):
        return self.multiplication(a, i)

    def ast(self, a):
        i, t = self.expression(a, 0)
        return t


dispatch = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "~": lambda x: -x
}


def evaluate(t):
    if isinstance(t, int):
        return t
    else:
        return dispatch[t[0]](*map(evaluate, t[1:]))


if __name__ == '__main__':

    with open('input.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]
    s1 = 0
    s2 = 0
    parser1 = Parser('part1')
    parser2 = Parser('part2')
    for line in lines:
        a = Parser.scan(line)
        t1 = parser1.ast(a)
        t2 = parser2.ast(a)
        s1 += evaluate(t1)
        s2 += evaluate(t2)
    print(f'Part 1: {s1}')
    print(f'Part 2: {s2}')
