# Flip
A 1D fungeoid inspired by [Backhand](https://github.com/GrayJoKing/Backhand/).

Unlike Backhand, the default step of the instruction pointer is 2.

This can be seen from the following example:
```
1 2 + z #
```

Before the terminate `#` instruction, only `1`, `2`, `+`, `z` are executed, so this will output `3`.

After halting, if nothing is outputted, the entire stack is `chr`'d before outputting as a single string, so nothing additional is outputted.

## IP wrapping

### Right bound
If the IP goes over the right bound, it will wrap backwards (like Backhand).

Whenever IP points to a position after the end of program, the amount that IP goes over the last character is used as a backwards index to the next character scanned by IP.

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

### Left bound
If the IP goes over the left bound, thr rebounding mechanism is similar to the right bound, because it also uses the IP offset as a backwards index. IP is set to `len(self.prog) - self.ip`.

Since the IP will usually step to the index `-1` if it is facing left, you can expect that IP will (usually) jump to the last character of the program.

E.g. :

```
1B2A| # C
```

Execution order:
```
1
  2
    |        Mirror: reflect IP
   A
 B
             Index of -1: IP is set to len(prog) - 1
        C    This means it continues at the character C.
      #      End the program.
```

## IP mirroring

* If the IP facing left, it moves left 1 position. If it's facing right, it moves right 1 position.

* Then, the IP reverses direction, and steps to the next instruction using the current IP step.

If you want to add the behavior of mirroring to your code, you have 4 options:

* `|`: Directly mirror the IP, like I've described above.
* `:`: Only mirror if TOS is nonzero (pops TOS).
* `$`: Mirror if TOS is nonzero (does not pop TOS).
* `&`: A kind of `filter` loop. Described below.

### How the filter loop works
Basically, the filter loop does the following in each iteration:

1. `self.acc -= 1`
2. Pop condition from TOS:
    1. If condition is truthy: shift TOS downwards.
    2. Otherwise: Drop TOS.
3. If `self.acc > 0`: mirror the IP.

#### An example

The following program filters out all odd-indexed items of the input list:

```
_#w@A&aI1
```

Explanation:
```
_            Read a list from the input (dumping onto the stack)
  w          Push the length of the stack
    A        Store the length to the accumulator
             ## Filter loop ##
      a          Push accumulator
        1
       I         Bitwise AND with 1 (this is our condition of the filter loop)
     &           This does the following:
                     1. acc -= 1
                     2. Pop the condition (which is the parity of our iteration index)
                         i. If condition is truthy, we put TOS to the bottom.
                         ii. Otherwise, if it's falsy, drop TOS. (No stack shifting happens)
                     3. If acc > 0: mirror the IP.
                 So basically this goes back to `a` until the filter loop is done.
            ## End filter loop ##
            
   @        Print the entire stack as a list
 #          End the program
```

If you want to do a map loop, just do whatever operation you want on the TOS. But make sure you push a condition of `1` at the end.

Reduce loops aren't as common as map / filter loops, so I didn't make a separate command for it. However, it can be implemented quite easily. One approach: repeat `len(stack) - 1` times: 1) shift bottom of stack to top (i.e. `1 m`). 2) Apply whatever binary operation you want in the reduce loop. Repeat can be implemented as a `:` with the accumulator pushed as the condition.

## Stuff from Backhand

Like Backhand, you can use `)` to increment the step of the IP, and `(` to decrement the step of the IP.

I also added `?` to conditionally skip the next N iterations of the program.

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
| `u`         | Push `30`. |
| `U`         | Push `12`. |
| `y`         | Push `25`. |
| `C`         | Push `100`. |
| `b`         | Push `20`. |
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
|`I`| Bitwise and. (both operands rounded with `int()`) |
|`p`| Bitwise or. (both operands rounded with `int()`) |
|`r`| Bitwise xor. (both operands rounded with `int()`) |

| Instruction | Description |
|:-:  |      :-: |
| `d` | log10. |
| `E`| Absolute value. |
| `G`| Truncate to integer. |

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
| `m` | Pop `N`: `stack = self.stack[N:] + self.stack[:N]` |
|`t` | Sort the stack. |
|`k` | Take: `stack = stack[-stack.pop():]`|
|`W`| Uniquify the stack. |
|`Y` | Repeat each item of the stack TOS times. |
|`T` | All: `stack = [all(stack)]`|
|`X` | Remove all occurrences of TOS from the stack. |
|`e` | Modular indexing: push `stack[stack.pop() % len(stack)]`. |
|`x` | Index of TOS in stack, or `-1` if not found. |
|`Q` | Push number of occurrences of TOS in stack. |

### Control flow
|Instruction | Description |
|:-:| :-:|
|`\|` | Mirror the IP. |
|`:` | mirror if tos is nonzero (pops tos). |
|`$`| Mirror if TOS is nonzero (does not pop TOS.) |
|`&`| Filter loop. |
|`)` | Increment IP's step by 1. |
|`(` | Decrement IP's step by 1. |
|`#` | End the program.|
|`?`| Pop `cond, N`; Skip next `N` commands if `cond` is falsy. |

### I/O
|Instruction|Description|
|:-:|:-:|
|`o` | Print the entire stack as a `chr`'d string. |
|`N` | Same as `o`, but without a trailing newline. |
|`@`| Debug: Print the entire stack. |
|`z`| Pop & print TOS as a number. |
|`q`| Pop & print TOS as a character. |
|`g` | Read a single character from the input. Or `0` on EOF. |
|`_` | Read a line from the input, eval as Python: </br> `str`: push the character codes onto the stack. </br> `list`: push all items of list onto stack. </br> `int` / `float`: push item onto stack. |
