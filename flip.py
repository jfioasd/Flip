import sys
import math

class Flip:
    def __init__(self, prog):
        self.prog = prog
        self.ip = 0
        self.ip_step = 2

        self.stack = []

        self.done = False
        self.printed = False
        self.in_str = False
        self.skip_next = False
        self.next_char = False

        self.acc = 16
        self.other_acc = -1

    def keep(self, num):
        self.stack = self.stack[-num:]

    def rev_d(self): # Reverse IP direction
        if self.ip_step > 0: # Facing right.
            self.ip -= 1
        else: # Facing left.
            self.ip += 1

        self.ip_step = - self.ip_step

    def right_rebound(self): # Rebound from right out-of-bound.
        self.ip = len(self.prog) - (self.ip - len(self.prog)) - 1
        self.ip_step = - self.ip_step

    def is_prime(self, num):
        if num == 1: return 0
        for i in range(2, int(math.sqrt(num))+1):
            if num % i == 0:
                return 0
        return 1

    def run(self):
        if self.ip < 0:
            self.done = True
            return

        if self.ip >= len(self.prog):
            # Implicit `|` on right bound.
            self.right_rebound()
            return
        else:
            if self.skip_next: # Do the IP bumping in advance
                self.skip_next = False
                self.prev_char = self.prog[self.ip]
                self.ip += self.ip_step
                return

            if self.next_char: # Also do the IP bumping in advance
                self.stack.append(ord(self.prog[self.ip]))
                self.next_char = False
                self.ip += self.ip_step
                return

            if self.in_str:
                if self.prog[self.ip] == '"': # End string.
                    self.in_str = False
                else:
                    self.stack.append(ord(self.prog[self.ip]))
                self.ip += self.ip_step
                return

            # actual command logic
            # First do numbers, +, and *.

            # print(self.ip, self.prog[self.ip])
            c = self.prog[self.ip]

            if c == '"': # Strings.
                self.in_str = True
            elif c == "'": # Single char string.
                self.next_char = True
            elif c.isdigit(): # Numbers.
                self.stack.append(int(c))
            elif c == "j": # 10.
                self.stack.append(10)

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
            elif c == "/": # Float Division.
                RHS, LHS = self.stack.pop(), self.stack.pop()
                self.stack.append(LHS / RHS)
                self.stack.append(LHS / RHS)
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
            elif c == "E": # Absolute value.
                self.stack.append(abs(self.stack.pop()))
            elif c == "G": # Truncate to integer.
                self.stack.append(int(self.stack.pop()))

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
            elif c == "H": # Pop to other accumulator.
                self.other_acc = self.stack.pop()
            elif c == "h": # Push other accumulator to the stack.
                self.stack.append(self.other_acc)

            elif c == "Z": # Sum the stack.
                self.stack = [sum(self.stack)]
            elif c == "w": # Length of the stack.
                self.stack.append(len(self.stack))
            elif c == "R": # Reverse the stack.
                self.stack = self.stack[::-1]
            elif c == "m": # Put bottom of the stack to TOS.
                self.stack = self.stack[1:] + [self.stack[0]]
            elif c == "t": # Sort the stack.
                self.stack = sorted(self.stack)
            elif c == "J": # Generate inclusive range.
                # (a b -- range(a, b+1))
                R, L = self.stack.pop(), self.stack.pop()
                for i in range(L, R+1):
                    self.stack.append(i)
            elif c == "k": # Take: (stack[-num:]).
                self.keep(self.stack.pop())
            elif c == "X": # Remove all occurrences of TOS in stack.
                N = self.stack.pop()
                self.stack = list(filter(lambda x: x != N, self.stack))
            elif c == "W": # Uniquify the stack.
                tmp = []
                for i in self.stack:
                    if i not in tmp: tmp.append(i)
                self.stack = tmp
            elif c == "Y": # Repeat each item of the stack N times.
                N = self.stack.pop()
                tmp = []
                for i in self.stack:
                    for j in range(N):
                        tmp.append(i)
                self.stack = tmp
            elif c == "i": # Push whether TOS is a prime.
                self.stack.append(self.is_prime(self.stack.pop()))
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
            elif c == "Q": # Count number of occurrences of TOS in stack.
                N = self.stack.pop()
                self.stack.append(self.stack.count(N))

            elif c == "=": # Equality.
                self.stack.append(int(self.stack.pop() == self.stack.pop()))
            elif c == "<": # Less than.
                self.stack.append(int(self.stack.pop() > self.stack.pop()))
            elif c == ">": # Greater than.
                self.stack.append(int(self.stack.pop() < self.stack.pop()))
            elif c == "F": # Within Range (inclusive): (a b c -- b <= a <= c)
                R, L, N = self.stack.pop(), self.stack.pop(), self.stack.pop()
                self.stack.append(int(L <= N <= R))
            elif c == "!": # Logical not.
                self.stack.append(int(not self.stack.pop()))
            elif c == "c": # Logical and.
                RHS, LHS = self.stack.pop(), self.stack.pop()
                self.stack.append(int(LHS and RHS))
            elif c == "I": # Bitwise and.
                RHS, LHS = self.stack.pop(), self.stack.pop()
                self.stack.append(LHS & RHS)
            elif c == "p": # Bitwise or.
                RHS, LHS = self.stack.pop(), self.stack.pop()
                self.stack.append(LHS | RHS)
            elif c == "r": # Bitwise xor.
                RHS, LHS = self.stack.pop(), self.stack.pop()
                self.stack.append(LHS ^ RHS)
            elif c == "B": # Logical or.
                RHS, LHS = self.stack.pop(), self.stack.pop()
                self.stack.append(int(LHS or RHS))

            elif c == "|": # Reverse direction.
                self.rev_d()
                return     # Don't auto-increment ptr at the end.
            elif c == ":": # Reverse direction if TOS is nonzero.
                # Pops TOS.
                if self.stack.pop():
                    self.rev_d()
                    return
                # Otherwise, increment by step as normal.
            elif c == "$": # Reverse direction if TOS is nonzero.
                # Does not pop TOS.
                if self.stack[-1]:
                    self.rev_d()
                    return
                # Like above
            elif c == "&": # "Times" loop (using acc as counter).
                self.acc -= 1
                if self.acc > 0:
                    self.rev_d()
                    return
            elif c == "b": # IP-relative jump.
                self.ip += self.stack.pop()
                return

            # Don't know how useful these are, but add them anyway.
            elif c == ")": # Increment IP's speed.
                self.ip_step += 1
            elif c == "(": # Decrement IP's speed.
                self.ip_step -= 1
            elif c == "{": # IP -= 1 (doesn't affect step).
                self.ip -= 1
            elif c == "S": # IP -= 1 if TOS is true.
                if self.stack.pop():
                    self.ip -= 1
            elif c == "}": # IP += 1.
                self.ip += 1

            elif c == "o": # Print entire stack as chr string.
                print("".join(map(chr,self.stack)))
                self.printed = True
            elif c == "N": # Same as `o`, but without a trailing newline.
                print(end = "".join(map(chr,self.stack)))
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
                self.stack.append(eval(x))
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

            self.ip += self.ip_step

if __name__ == "__main__":
    prog = open(sys.argv[1]).read()

    x = Flip(prog)
    while not x.done:
        x.run()

    if not x.printed:
        print("".join(map(chr,x.stack)))
