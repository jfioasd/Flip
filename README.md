# Flip
A 1D fungeoid inspired by [Backhand](https://github.com/GrayJoKing/Backhand/).

Unlike Backhand, the default step of the instruction pointer is 2.

This can be seen from the following example:
```
1 2 + z #
```

Before the terminate `#` instruction, only `1`, `2`, `+`, `z` are executed, so this will output `3`. After halting, if nothing is outputted, the entire stack is implicitly outputted, so nothing additional is outputted.

---

Another thing is that execution will be terminated if the IP goes out of the left bound, but the IP will wrap backwards for the right bound.

How wrapping is done: whenever the IP points to an index greater than the program length during program execution, we use whatever amount IP goes over the end of the program as a backwards index to the next character scanned by IP.

This can be visualized as follows (suppose our program is 5 chars):
```
abcde

a
  c
    e
      _ Our IP goes 2 characters out of bounds,
        so we flip whatever amount IP goes over the end of the program
        back as an index into the progam.
        i.e.:
   <<   (Now we're pointing to d)
   d
 b
        Execution goes over the left bound, so program is terminated.
```

Suppose our program is 4 chars:
```
abcd
a    Bump IP like normal.
  c
    _ IP goes 1 char out of bounds, so use that as a backwards index:
   <  (Now IP is pointing to `d`)
   d
 b
      Execution is terminated since IP goes out of bounds.
```

---

Another thing is IP mirroring commands.

I'll first explain how mirroring works.

* If the IP facing left, it moves left 1 position. If it's facing right, it moves right 1 position.

* Then, the IP reverses direction, and steps to the next instruction using the current IP step.

If you want to add the behavior of mirroring to your code, you have 4 options:

* `|`: Directly mirror the IP, like I've described above.
* `:`: Only mirror if TOS is nonzero (pops TOS).
* `$`: Mirror if TOS is nonzero (does not pop TOS).
* `&`: A kind of `repeat` loop: Decrement the accumulator, and mirror if `acc > 0`.

Like Backhand, you can `)` to increment the step of the IP, and `(` to decrement the step of the IP.

You can `{` for stepping IP left 1, and `}` for stepping IP left 1 if TOS is truthy.

You can also `b` to do an IP-relative jump (`IP += stack.pop()`)

---

P. S. There is also a binary apply <code>`</code> inspired by Factor. Syntax is like follows:
```
` command1 command2
```
Where `command1` and `command2` are both 1-byte commands. Execution: The current TOS is first saved to a temporary variable (non-popping), then `command1` is executed, then the temporary variable is retrieved, then `command2` is executed on the retrieved variable.

## Data structures
Flip has a stack and 2 accumulators. The relevant operations are listed below:

* `a`: Push the accumulator to the stack (initially `16`)
* `A`: Pop TOS to the accumulator
* `h`: Push other accumulator to stack (initially `-1`)
* `H`: Pop TOs to other accumulator

## Instruction reference
### Constants
| Instruction | Description |
| :---: | :-: |
| `0-9`       | Push a number onto the stack (single-digit). |
| `j`         | Push `10`. |
| `"`         | Start / End string mode, in which all characters in betwen have their `ord` codes pushed onto the stack. |
| `'`         | Push the ord code of the next character read by IP. |

### Arithmetic and Math
| Instruction | Description |
| :-: | :-: |
| `+`         | Add: `( a b -- a+b )` |
| `-`         | Subtract: `( a b -- a-b )` |
| `*`         | Multiply: `( a b -- a*b )` |
| `%`         | Modulo: `( a b -- a%b )` |
| `/`         | Float Division: `( a b -- a/b )` |
| `^`         | Exponentiation: `( a b -- a**b )` |
| `~`         | Negate TOS. |
| `]`         | Increment TOS. |
| `[`         | Decrement TOS. |

| Instruction | Description |
|:-: | :-:|
| `=` | Equals? (a == b) |
|`<` | Less than? (a < b) |
|`>` | Greater than? (a > b) |
|`F` | Within range (inclusive)? `(N l r -- l <= N <= r)` |
|`!` | Logical not. |
|`c`| Logical and. |
|`B`| Logical or. |
|`I`| Bitwise and. |
|`p`| Bitwise or. |

| Instruction | Description |
|:-:  |      :-: |
| `d` | log10. |
| `f` | Square root. |
| `E`| Absolute value. |
| `G` | Truncate to integer. |
| `i` | Push whether TOS is a prime. |

### Stack operations

| Instruction | Description |
|:-: | :-:|
| `D` | Dup. `(x -- x x)`|
|`v` | Over. `(x y -- x y x)`|
|`s` | swap. `(x y -- y x)`|
|`;` | drop. `(... x -- ... )`|
| `a` | Push the accumulator onto the stack. |
| `A` | Pop TOS to accumulator. |
| `h` | Push other accumulator to stack. |
| `H` | Pop TOS to other accumulator. |
### Stack arithmetic

| Instruction | Description |
|:-:|:-:|
|`Z` | Push the sum of the stack (clears the previous stack). |
| `w` | Push the length of the stack. |
|`R` | Reverse the stack. |
| `m` | Shift bottom of stack to TOS. |
|`t` | Sort the stack. |
|`J` | Generate inclusive range. Pops `L, R`, Pushes `range(L, R+1)` dumped onto the stack. |
|`k` | Take: `stack = stack[-stack.pop():]`|
|`W`| Uniquify the stack. |
|`Y` | Repeat each item of the stack TOS times. |
|`T` | All: `stack = [all(stack)]`|
|`X` | Remove all occurrences of TOS from the stack. |
|`e` | Modular indexing: push `stack[stack.pop() % len(stack)]`. |
|`x` | Index of TOS in stack, or `-1` if not found. |
|`u` | Push 1 if the stack contains TOS, 0 otherwise. |
|`Q` | Push number of occurrences of TOS in stack. |

### Control flow
|Instruction | Description |
|:-:| :-:|
|`\|` | Mirror the IP. |
|`:` | mirror if tos is nonzero (pops tos). |
|`$`| Mirror if TOS is nonzero (does not pop TOS.) |
| <code>`</code> | Binary apply the next command (single-byte). |
| `{` | `IP -= 1`. (Does not affect IP's step.) |
| `}` | If `stack.pop()` is truthy, `IP -= 1`. |
| `S` | `IP += 1`. |
|`&`| Decrement acc. If acc > 0, mirror. (downwards `repeat` loop) |
|`b` | IP-relative jump: `IP += stack.pop()` |
|`)` | Increment IP's step by 1. |
|`(` | Decrement IP's step by 1. |
|`#` | End the program.|
|`K` | Skip the next command scanned by the IP. |
|`?`| Pop TOS; Skip next command if TOS is 0. |

### I/O
|Instruction|Description|
|:-:|:-:|
|`o` | Print the entire stack as a `chr`'d string. |
|`N` | Same as `o`, but without a trailing newline. |
|`@`| Debug: Print the entire stack. |
|`z`| Pop & print TOS as a number. |
|`q`| Pop & print TOS as a character. |
|`g` | Read a single character from the input. Or `0` on EOF. |
|`V` | Read a single newline-terminated integer from the input. |
