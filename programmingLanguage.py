class language:
    def __init__(self,fileName):
        self.file = fileName
        self.commands = ['print','loop','input']
        self.lines = []
        self.words = []
        self.variables = {}
        self.ignore = ['comment','end']

    def readFile(self):
        with open(self.file) as f:
            self.lines = f.read().splitlines()
        for x in self.lines:
            self.words.append(x.split(' '))

    def execute(self):
        while self.lines:
            line = self.lines.pop(0)
            if self.words[0][0] == 'print':
                self.words.pop(0)
                print(line[5:])
            elif self.words[0][0] == 'loop':
                loopTime = self.words[0][1]
                self.words.pop(0)
                toLoop = []
                toWords = []
                while not self.words[0][0] == 'end':
                    x = self.lines.pop(0)
                    y = self.words.pop(0)
                    toLoop.append(x)
                    toWords.append(y)
                for x in range(int(loopTime)):
                    self.lines = toLoop + self.lines
                    self.words = toWords + self.words
            elif self.words[0][0] == 'variable':
                if self.words[0][2] == '=':
                    if self.words[0][3] == 'input':
                        varIn = input(" ".join(self.words[0][4:]) + "\n")
                        self.variables[self.words[0][1]] = varIn
                        self.replaceVar(self.words[0][1],varIn)
                    else:
                        self.variables[self.words[0][1]] = ' '.join(self.words[0][3:])
                        self.replaceVar(self.words[0][1],' '.join(self.words[0][3:]))
                else:
                    return "Error","No Variable Assignment"
                self.words.pop()
            elif self.words[0][0] in self.ignore:
                self.words.pop(0)
                pass
            else:
                return "Error","Unknown Command"

    def replaceVar(self,variable,replacement):
        for i,v in enumerate(self.lines):
            w = v.split(' ')
            for j,word in enumerate(w):
                if word == variable:
                    w[j] = replacement
            self.lines[i] = ' '.join(w)
            self.words[i] = w

class Lexer():
    tokens = { r'[a-zA-Z_][a-zA-Z0-9_]*', '^[-+]?[0-9]+$', r'\".*?\"' }
    ignore = '\t '
    literals = { '=', '+', '-', '/','*', '(', ')', ',', ';'}

    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    def COMMENT(self, t):
        pass

    def newline(self, t):
        self.lineno = t.value.count('\n')

class Parser():
    tokens = Lexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.env = { }

    def statement(self, p):
        pass

    def statement(self, p):
        return p.var_assign

    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)

    def var_assign(self, p):
        return ('var_assign', p.NAME, p.STRING)

    def statement(self, p):
        return (p.expr)

    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    def expr(self, p):
        return p.expr

    def expr(self, p):
        return ('var', p.NAME)
    def expr(self, p):
        return ('num', p.NUMBER)

def main():
    file = input("What file do you want compiled?")
    if file == '':
        file = 'programTesting.txt'
    Compiler = language(file)
    Compiler.readFile()
    errors = Compiler.execute()
    if errors != None and errors[0] == 'Error':
        print("Error:" + errors[1])


if __name__ == "__main__":
    main()