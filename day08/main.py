class GameConsole():
    def __init__(self):
        self.r_accumulator = 0

    def execute(self, operation, argument):
        if operation == 'acc':
            self.r_accumulator += argument
            return 1
        elif operation == 'nop':
            return 1
        elif operation == 'jmp':
            return argument

    def run_program(self, instructions):
        visited = []
        index = 0

        while True:
            visited.append(index)
            index += self.execute(*instructions[index])
            if index in visited:
                return False
            if 0 < index >= len(instructions):
                return True


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    instructions = [(line.strip().split(' ')[0], int(line.strip().split(' ')[1])) for line in lines]
    console = GameConsole()
    console.run_program(instructions)
    print(f'Part 1: {console.r_accumulator}')

    for i, (op, arg) in enumerate(instructions):
        if op in ['jmp', 'nop']:
            temp_int = instructions.copy()
            temp_int[i] = ('nop' if op == 'jmp' else 'jmp', arg)
            console = GameConsole()
            if console.run_program(temp_int):
                print(f'Part 2: {console.r_accumulator}')
                break
