import sys
import math

class Flip:
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

    def keep(self, num):
        self.stack = self.stack[-num:]

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
            # Implicit `|` is also not as useful.
            self.done = True
            return
        else:
            if self.skip_next: # Do the IP bumping in advance
                self.skip_next = False
                self.prev_char = self.prog[self.ip]
                self.ip += self.ip_step
                return

            if self.in_str:
                if self.prog[self.ip] == '"': # End string.
                    self.in_str = False
                else:
                    self.stack.append(ord(self.prog[self.ip]))
                self.prev_char = self.prog[self.ip]
                self.ip += self.ip_step
                return

            # actual command logic
            # First do numbers, +, and *.

            # print(self.ip, self.prog[self.ip])
            c = self.prog[self.ip]

            if c == '"': # Strings.
                self.in_str = True
            elif c in "0123456789": # Numbers.
                if self.ip > 0 and \
                    self.prev_char in "0123456789": # multi-digit.
                    self.stack.append(self.stack.pop()*10 + int(c))
                else:
                    self.stack.append(int(c))

            elif c == "+": # Addition.
                self.stack.append(self.stack.pop() + self.stack.pop())
            elif c == "-": # Subtraction.
                RHS, LHS = self.stack.pop(), self.stack.pop()
                self.stack.append(LHS - RHS)
            elif c == "*": # Multiplication.
                self.stack.append(self.stack.pop() * self.stack.pop())
            elif c == "%": # Modulo.
                RHS, LHS = self.stack.pop(), self.stack.pop()
                self.stack.append(LHS % RHS)
            elif c == "/": # Int Division.
                RHS, LHS = self.stack.pop(), self.stack.pop()
                self.stack.append(LHS // RHS)
            elif c == "^": # Exponentiation.
                RHS, LHS = self.stack.pop(), self.stack.pop()
                self.stack.append(LHS ** RHS)
            elif c == "~": # Negate.
                self.stack.append(- self.stack.pop())
            elif c == "]": # x + 1
                self.stack.append(self.stack.pop() + 1)
            elif c == "[": # x - 1
                self.stack.append(self.stack.pop() - 1)

            elif c == "d": # log10.
                self.stack.append(math.log10(self.stack.pop()))
            elif c == "f": # Square root.
                self.stack.append(math.sqrt(self.stack.pop()))
            elif c == "j": # Floor.
                self.stack.append(math.floor(self.stack.pop()))
            elif c == "G": # Abs.
                self.stack.append(abs(self.stack.pop()))
            elif c == "h": # Sine.
                self.stack.append(math.sin(self.stack.pop()))

            elif c == "D": # Dup.
                self.stack.append(self.stack[-1])
            elif c == "v": # Over.
                self.stack.append(self.stack[-2])
            elif c == "s": # Swap.
                self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
            elif c == ";": # Drop.
                self.stack.pop()

            elif c == "A": # Pop to accumulator.
                self.acc = self.stack.pop()
            elif c == "a": # Push accumulator to the stack.
                self.stack.append(self.acc)

            elif c == "L": # swap the two stacks.
                self.stack, self.other = self.other, self.stack

            elif c == "Z": # Sum the stack.
                self.stack = [sum(self.stack)]
            elif c == "w": # Length of the stack.
                self.stack.append(len(self.stack))
            elif c == "R": # Reverse the stack.
                self.stack = self.stack[::-1]
            elif c == "y": # Put TOS to the bottom of the stack.
                self.stack = [self.stack[-1]] + self.stack[:-1]
            elif c == "t": # Sort the stack.
                self.stack = sorted(self.stack)
            elif c == "k": # Stack slicing (stack[-num:]).
                self.keep(self.stack.pop())
            elif c == "Y": # Repeat the stack N times.
                N = self.stack.pop()
                self.stack *= N
            elif c == "T": # Push whether all items in the stack is truthy.
                self.stack = [int(all(self.stack))]

            elif c == "e": # Push stack[N]. (Modular)
                N = self.stack.pop()
                self.stack.append(self.stack[N % len(self.stack)])
            elif c == "x": # Index of stack[N]. (-1 if not found)
                N = self.stack.pop()
                try:
                    self.stack.append(self.stack.index(N))
                except ValueError:
                    self.stack.append(-1)
            elif c == "u": # Push whether stack contains N.
                N = self.stack.pop()
                self.stack.append(int(N in self.stack))

            elif c == "=": # Equality.
                self.stack.append(int(self.stack.pop() == self.stack.pop()))
            elif c == "<": # Less than.
                self.stack.append(int(self.stack.pop() > self.stack.pop()))
            elif c == ">": # Greater than.
                self.stack.append(int(self.stack.pop() < self.stack.pop()))
            elif c == "!": # Logical not.
                self.stack.append(int(not self.stack.pop()))

            elif c == "|": # Reverse direction.
                self.rev_d()
                return     # Don't auto-increment ptr at the end.
            elif c == ":": # Reverse direction if TOS is nonzero.
                # Pops TOS, since that's more useful.
                if self.stack.pop():
                    self.rev_d()
                    return
                # Otherwise, increment by step as normal.
            elif c == "&": # "Times" loop (using acc as counter).
                self.acc -= 1
                if self.acc > 0:
                    self.rev_d()
                    return
            elif c == "b": # IP-relative jump.
                self.ip += self.stack.pop()
                return

            # Don't know how useful these two are, but add them anyway.
            elif c == ")": # Increment IP's speed.
                self.ip_step += 1
            elif c == "(": # Decrement IP's speed.
                self.ip_step -= 1

            elif c == "o": # Print entire stack as chr string.
                print("".join(map(chr,self.stack)))
                self.printed = True
            elif c == "z": # Pop, and print TOS as a number.
                print(self.stack.pop())
                self.printed = True
            elif c == "q": # Pop, and print TOS as a character.
                print(end = chr(self.stack.pop()))
                self.printed = True
            elif c == "g": # Push a single char from input.
                x = sys.stdin.read(1)
                if x == '':
                    self.stack.append(0)
                else:
                    self.stack.append(ord(x))
            elif c == "V": # Read a single integer from input (newline-terminated).
                x = input()
                self.stack.append(int(x))
            elif c == "@": # Debug: Output stack as an array.
                print(self.stack)

            elif c == "#": # End the prog.
                self.done = True
            elif c == "K": # Skip the next char.
                self.skip_next = True
            elif c == "?": # If TOS is zero, skip the next char.
                # Pops the top of stack.
                if not self.stack.pop():
                    self.skip_next = True

            self.prev_char = self.prog[self.ip]
            self.ip += self.ip_step

if __name__ == "__main__":
    prog = open(sys.argv[1]).read()

    x = Flip(prog)
    while not x.done:
        x.run()

    if not x.printed:
        # For now, output stack as an array.
        # I'll change that to chr & join output
        # when most of the coding is done.
        print(x.stack)
