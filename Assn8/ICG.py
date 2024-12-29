class QuadrupleGenerator:
    def __init__(self):
        self.temp_count = 0
        self.quadruples = []

    def new_temp(self):
        self.temp_count += 1
        return f"T{self.temp_count}"

    def add_quadruple(self, operation, arg1, arg2, result):
        self.quadruples.append((operation, arg1, arg2, result))

    def generate(self, expression):
        stack = []
        
        for token in expression:
            if token in "+-*/":
                arg2 = stack.pop()
                arg1 = stack.pop()
                result = self.new_temp()
                self.add_quadruple(token, arg1, arg2, result)
                stack.append(result)
            else:
                stack.append(token)
        return stack.pop()

    def display(self):
        print("Quadruples (Operation, Arg1, Arg2, Result):")
        for op, arg1, arg2, res in self.quadruples:
            print(f"({op}, {arg1}, {arg2}, {res})")

print("Expression : (a + b) * c - d \n")
expression = ["a", "b", "+", "c", "*", "d", "-"]  # represents (a + b) * c - d
generator = QuadrupleGenerator()
generator.generate(expression)
generator.display()