import sys

class Reflect:
    def __init__(self, prog):
        self.prog = prog
        self.ip = 0
        self.ip_step = 2

        self.stack = []
        self.otherstack = []

        self.done = False

        self.acc = 16

    def rebound(self):
        if len(self.prog) % 2 == 1: # Odd length:
            self.ip -= 1
        else: # Even length
            self.ip += 1

        self.ip_step = - self.ip_step 
        self.ip += self.ip_step

    def run(self):
        if self.ip < 0:
            self.done = True
            return

        if self.ip >= len(self.prog):
            self.rebound()
        else: 
            # none defined yet, so just print debug info.
            print(self.ip, ":", repr(self.prog[self.ip]))

            self.ip += self.ip_step

if __name__ == "__main__":
    prog = open(sys.argv[1]).read()

    x = Reflect(prog)
    while not x.done:
        x.run()
