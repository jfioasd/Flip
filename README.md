# Reflect
A 1D fungeoid inspired by [Backhand](https://github.com/GrayJoKing/Backhand/).

Unlike Backhand, the default step of the instruction pointer is 2; so the IP will execute a character, skip a character, execute another character, skip another character, ... etc.

This can be seen from the following example:
```
1 _ 2 + #
```

Before the terminate `#` instruction, only `1`, `_`, `2`, `+` are executed. (Numbers need a separator instead of pusing individual digits.) After halting, if nothing is outputted, the entire stack is implicitly outputted, so this will output `[3]`.

I'll first explain how rebounding works.

* If the IP is about to step out of bounds, if it is initially facing the right, then it'll step forward 1 char and reverse direction.

* Otherwise, If it's rebounding while facing the left (e.g. when you're using `|` to reflect the IP), then it'll first reverse direction, then step forward 1 char.

Another thing is that although the IP will bounce back if it goes across the right bound, execution will be terminated if the IP goes over the left bound. For example, the above program can be golfed to the following:
```
1+_2
```

Execution order:
```
1    Initial IP position. 
  _  End number: Push 1.
     IP is about to step out of bounds, so we move forward 1 char & reverse direction.
     (since IP is facing the right.)
   2 Push 2.
 +   Add. (1 + 2)

     When IP goes over the left bound, execution is terminated, and [3] is printed.
```
If you want to add the behavior of rebounding to your code, you have 3 options:

* `|`: Directly rebound the IP, like I've described above.
* `:`: Only rebound if TOS is nonzero (pops TOS).
* `&`: A kind of `repeat` loop: Decrement the accumulator, and rebound if `acc > 0`.

Like Backhand, you can `)` to increment the step of the IP, and `(` to decrement the step of the IP.

You can also `b` to do an IP-relative jump (`IP += stack.pop()`)

## Data structures
Reflect has 2 stacks, but it also has an accumulator. The relevant operations are listed below:

* `L`: Exchange this stack with the other stack.
* `a`: Push the accumulator to the stack (initially `16`)
* `A`: Pop TOS to the accumulator

## Instruction reference
### Constants
| Instruction | Description |
| :---: | :-: |
| `0-9`       | Push a number onto the stack, or multi-digit numbers if previous character is a number. |
| `"`         | Start / End string mode, in which all characters in betwen have their `ord` codes pushed onto the stack. |

### Arithmetic and Math
| Instruction | Description |
| :-: | :-: |
| `+`         | Add: `( a b -- a+b )` |
| `*`         | Multiply: `( a b -- a*b )` |
| `%`         | Modulo: `( a b -- a%b )` |
| `/`         | Division: `( a b -- a/b )` |
| `^`         | Exponentiation: `( a b -- a**b )` |
| `~`         | Negate TOS. |
| `]`         | Increment TOS. |
| `[`         | Decrement TOS. |

| Instruction | Description |
|:-:  |      :-: |
| `d` | log10. |
| `f` | Square root. |
| `j` | floor. |
| `G` | Abs. |
| `h` | sine.|
