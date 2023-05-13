import sys

class Reflect:
    def __init__(self, prog):
        self.prog = prog
        self.ip = 0
        self.ip_step = 2

        self.prev_char = ""

        self.stack = []
        self.other = []

        self.done = False
        self.printed = False
        self.in_str = False
        self.skip_next = False

        self.acc = 16

    def rebound(self):
        self.ip_step = - self.ip_step 

        # Backhand's reflect only works for step=3,
        # so it makes sense to make Reflect's reflect only work for step=2.

        self.ip = len(prog) - (self.ip - len(prog) + 1)

    def rev_d(self): # Reverse IP direction
        if self.ip % 2 == 0: # Even.
            self.ip -= 1
        else: # Odd.
            self.ip += 1

        self.ip_step = - self.ip_step

    def run(self):
        if self.ip < 0:
            self.done = True
            return

        if self.ip >= len(self.prog):
            self.rebound()
        else:
            if self.skip_next: # Do the IP bumping in advance
                self.skip_next = False
                self.prev_char = self.prog[self.ip]
                self.ip += self.ip_step
                return
                
            # actual command logic
            # First do numbers, +, and *.

            # print(self.ip, self.prog[self.ip])
            c = self.prog[self.ip]

            if c in "0123456789": # Numbers.
                if self.ip > 0 and \
                    self.prev_char in "0123456789": # multi-digit.
                    self.stack.append(self.stack.pop()*10 + int(c))
                else:
                    self.stack.append(int(c))

            elif c == "+": # Addition.
                self.stack.append(self.stack.pop() + self.stack.pop())
            elif c == "*": # Multiplication.
                self.stack.append(self.stack.pop() * self.stack.pop())
            elif c == "~": # Negate.
                self.stack.append(- self.stack.pop())
            elif c == "]": # x + 1
                self.stack.append(self.stack.pop() + 1)
            elif c == "[": # x - 1
                self.stack.append(self.stack.pop() - 1)

            elif c == "d": # Dup.
                self.stack.append(self.stack[-1])
            elif c == "v": # Over.
                self.stack.append(self.stack[-2])
            elif c == "s": # Swap.
                self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
            elif c == ";": # Drop.
                self.stack.pop()

            elif c == "=": # Equality.
                self.stack.append(int(self.stack.pop() == self.stack.pop()))
            elif c == "<": # Less than.
                self.stack.append(int(self.stack.pop() > self.stack.pop()))

            elif c == "|": # Reverse direction.
                self.rev_d()
                return     # Don't auto-increment ptr at the end.
            elif c == ":": # Reverse direction if TOS is zero.
                # Does not pop TOS.
                if not self.stack[-1]:
                    self.rev_d()
                    return
                # Otherwise, increment by step as normal.

            # Don't know how useful these are, but add them anyway.
            elif c == ")": # Increment IP's speed.
                self.ip_step += 1
            elif c == "(": # Decrement IP's speed.
                self.ip_step -= 1
            elif c == "}": # Increment IP's speed, but only in the next iteration.
                pass

            elif c == "#": # End the prog.
                self.done = True
            elif c == "T": # Skip the next char.
                self.skip_next = True
            elif c == "Y": # If TOS is zero, skip the next char.
                # Pops the top of stack.
                if not self.stack.pop():
                    self.skip_next = True

            self.prev_char = self.prog[self.ip]
            self.ip += self.ip_step

if __name__ == "__main__":
    prog = open(sys.argv[1]).read()

    x = Reflect(prog)
    while not x.done:
        x.run()

    if not x.printed:
        # For now, output stack as an array.
        # I'll change that to chr & join output
        # when most of the coding is done.
        print(x.stack)
