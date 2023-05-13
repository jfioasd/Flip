# Flip
A 1D fungeoid inspired by [Backhand](https://github.com/GrayJoKing/Backhand/).

Unlike Backhand, the default step of the instruction pointer is 2.

This can be seen from the following example:
```
1 _ 2 + #
```

Before the terminate `#` instruction, only `1`, `_`, `2`, `+` are executed. (Numbers need a separator instead of pusing individual digits.) After halting, if nothing is outputted, the entire stack is implicitly outputted, so this will output `[3]`.

I'll first explain how rebounding works.

* If the IP is initially facing the right, then it'll step forward 1 char and reverse direction.

* Otherwise, if it's rebounding while facing the left, then it'll first reverse direction, then step forward 1 char.

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

You can also `b` to do an IP-relative jump (`IP += stack.pop()`)

## Data structures
Flip has 2 stacks, but it also has an accumulator. The relevant operations are listed below:

* `L`: Exchange this stack with the other stack.
* `a`: Push the accumulator to the stack (initially `16`)
* `A`: Pop TOS to the accumulator

## Instruction reference
### Constants
| Instruction | Description |
| :---: | :-: |
| `0-9`       | Push a number onto the stack, or multi-digit numbers if previous character is a number. |
| `"`         | Start / End string mode, in which all characters in betwen have their `ord` codes pushed onto the stack. |
| `'`         | Push the ord code of the next character read by IP. |

### Arithmetic and Math
| Instruction | Description |
| :-: | :-: |
| `+`         | Add: `( a b -- a+b )` |
| `-`         | Subtract: `( a b -- a-b )` |
| `*`         | Multiply: `( a b -- a*b )` |
| `%`         | Modulo: `( a b -- a%b )` |
| `/`         | Integer Division: `( a b -- a//b )` |
| `\`        | Float division: `( a b -- a/b )` |
| `^`         | Exponentiation: `( a b -- a**b )` |
| `~`         | Negate TOS. |
| `]`         | Increment TOS. |
| `[`         | Decrement TOS. |

| Instruction | Description |
|:-: | :-:|
| `=` | Equals? (a == b) |
|`<` | Less than? (a < b) |
|`>` | Greater than? (a > b) |
|`!` | Logical not. |

| Instruction | Description |
|:-:  |      :-: |
| `d` | log10. |
| `f` | Square root. |
| `j` | 2 ** X |
| `G` | Abs. |
| `E` | Factorial of TOS. |

### Stack operations

| Instruction | Description |
|:-: | :-:|
| `D` | Dup. `(x -- x x)`|
|`v` | Over. `(x y -- x y x)`|
|`s` | swap. `(x y -- y x)`|
|`;` | drop. `(... x -- ... )`|
| `a` | Push the accumulator onto the stack. |
| `A` | Pop TOS to accumulator. |
| `L` | Exchange this stack w/ the other stack. |
### Stack arithmetic

| Instruction | Description |
|:-:|:-:|
|`Z` | Push the sum of the stack (clears the previous stack). |
| `w` | Push the length of the stack. |
|`R` | Reverse the stack. |
|`y` | Shift TOS to the bottom of the stack. |
|`t` | sort the stack. |
|`r` | Push random item from stack. (Clears previous stack) |
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
| `{` | IP -= 1. (Does not affect IP's step.) |
| `}` | If `stack.pop()` is truthy, IP -= 1. |
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
|`@`| Debug: Print the entire stack. |
|`z`| Pop & print TOS as a number. |
|`q`| Pop & print TOS as a character. |
|`g` | Read a single character from the input. Or `0` on EOF. |
|`V` | Read a single newline-terminated integer from the input. |
