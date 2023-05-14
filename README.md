# Flip
A 1D fungeoid inspired by [Backhand](https://github.com/GrayJoKing/Backhand/).

Unlike Backhand, the default step of the instruction pointer is 2.

This can be seen from the following example:
```
1 _ 2 + #
```

Before the terminate `#` instruction, only `1`, `_`, `2`, `+` are executed. (Numbers need a separator instead of pusing individual digits.) After halting, if nothing is outputted, the entire stack is implicitly outputted, so this will output `[3]`.

I'll first explain how rebounding works.

* If the IP facing left, it moves left 1 position. If it's facing right, it moves right 1 position.

* Then, the IP reverses direction, and steps to the next instruction using the current IP step.

Another thing is that execution will be terminated if the IP goes out of bound, so you will need to write explicit `|`'s to rebound the IP. For example, the above program can be golfed to the following:
```
1+_2|
```

Execution order:
```
1     Initial IP position. 
  _   End number: Push 1.

    | Rebound: we move forward 1 char & reverse direction.
      (since IP is facing the right.)

   2  Push 2.
 +    Add. (1 + 2)

     When IP goes over the left bound, execution is terminated, and [3] is printed.
```
If you want to add the behavior of rebounding to your code, you have 3 options:

* `|`: Directly rebound the IP, like I've described above.
* `:`: Only rebound if TOS is nonzero (pops TOS).
* `&`: A kind of `repeat` loop: Decrement the accumulator, and rebound if `acc > 0`.

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
Flip has 2 stacks, but it also has 2 accumulators. The relevant operations are listed below:

* `L`: Exchange this stack with the other stack.
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
| `G` | Floor. |
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
| `L` | Exchange this stack w/ the other stack. |
| `,` | Copy the TOS of the other stack to this stack. |
| `.` | Pop TOS of this stack to other stack. |
| `U` | Pop the TOS of the other stack to this stack. |
| `n` | Copy the TOS of this stack to other stack. |
### Stack arithmetic

| Instruction | Description |
|:-:|:-:|
|`Z` | Push the sum of the stack (clears the previous stack). |
| `w` | Push the length of the stack. |
|`R` | Reverse the stack. |
|`y` | Shift TOS to the bottom of the stack. |
|`t` | sort the stack. |
|`W` | Uniquify the stack. |
|`J` | Generate inclusive range. Pops `L, R`, Pushes `range(L, R+1)` dumped onto the stack. |
|`k` | Take: `stack = stack[-stack.pop():]`|
|`Y` | Repeat the stack TOS times. |
|`T` | All: `stack = [all(stack)]`|
|`X` | Remove all occurrences of TOS from the stack. |
|`e` | Modular indexing: push `stack[stack.pop() % len(stack)]`. |
|`x` | Index of TOS in stack, or `-1` if not found. |
|`u` | Push 1 if the stack contains TOS, 0 otherwise. |
|`Q` | Push number of occurrences of TOS in stack. |

### Control flow
|Instruction | Description |
|:-:| :-:|
|`\|` | Rebound the IP. |
|`:` | rebound if tos is nonzero (pops tos). |
|`$`| Rebound if TOS is nonzero (does not pop TOS.) |
| <code>`</code> | Binary apply the next command (single-byte). |
| `{` | `IP -= 1`. (Does not affect IP's step.) |
| `}` | If `stack.pop()` is truthy, `IP -= 1`. |
| `S` | `IP += 1`. |
|`&`| Decrement acc. If acc > 0, rebound. (downwards `repeat` loop) |
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
