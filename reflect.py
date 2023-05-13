import sys

class Reflect:
    def __init__(self, prog):
        self.prog = prog
        self.ip = 0
        self.ip_step = 2
        self.stack = []
        self.otherstack = []

        self.acc = 16

    def rebound(self):
        self.ip_step = - self.ip_step 
        self.ip = len(prog) + self.ip_step

    def run(self):
        # only do the main loop for now

        while True:
            if self.ip < 0: break
            print(self.ip)

            if self.ip >= len(self.prog):
                self.rebound()
            else: # If not out of right bound, exec instrs normally
                # none defined yet, so just print debug info.
                print(self.ip, ":", repr(self.prog[self.ip]))

                self.ip += self.ip_step

if __name__ == "__main__":
    prog = open(sys.argv[1]).read()

    Reflect(prog).run()
