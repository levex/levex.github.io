---
layout: post
title: "x86 ISA Extensions part I: MMX"
date:   2018-03-31 19:28:00 +0100
categories: post x86-extensions
---

Welcome to this series about instruction set extensions to the x86 architecture. X86 is a computer architecture that has evolved loads over the years and there have been many extensions to the original instruction set (including 64-bit "long" mode). Over the course of a few blog posts, we explore these extensions and the reasoning behind their existence.

So, the first extension I'd like to talk about is the MMX extension originally introduced with the Pentium P5 family of Intel processors in the late 1990s. Let's dive in!

<!-- MORE -->

Do you have MMX?
----------------

As with every instruction set extension, there is a possibility that the CPU of your system does not support it. The chances are pretty slim with MMX given that it has been around for a long while, but just to be sure follow these instructions:

On Linux:

```sh
$ cat /proc/cpuinfo | grep -wq mmx && echo "MMX available" || echo "MMX not available"
```

On OS X/macOS:

```sh
$ sysctl machdep.cpu.features | grep -wq MMX && echo "MMX available" || echo "MMX not available"
```

Alternatively, you can use the `CPUID` instruction to figure whether your CPU supports MMX (as indicated by Leaf 1, Bit 23):

```assembly_x86
.text
.globl _is_mmx_available
_is_mmx_available:
    pushq   %rbx

    movq    $1, %rax
    cpuid
    movq    %rdx, %rax
    shrq    $23, %rax
    andq    $1, %rax

    popq    %rbx
    ret
```

Technical details
------------------

Interestingly, MMX does not introduce new registers, but instead opts to introduce aliases for the 80-bit x87 FPU registers' bottom 64 bits. These are called `%mmx0, %mmx1, ..., %mmx7`. Since these are only aliases and not real registers, it is immediately obvious that the registers cannot be used while an FPU operation is taking place. Since FPU registers are 80-bit long and MMX "registers" are 64-bit it's important to note where in those FPU registers are the MMX registers: they form the 64-bit mantissa of the original FPU register, and the remaining 16 bits are all set to 1. This is useful, since it means the FPU can recognize the SIMD data in the registers as NaN or infinities and of course, software can distinguish between the two types of data as well.

But why did Intel choose to use aliases instead of adding new registers? They wanted to be trivially compatible with existing operating systems' context switching code which already knew how to save and restore the FPU registers and now by the virtue of aliasing, it also supports saving and restoring the MMX registers.

The main selling point of MMX is the ability to pack multiple values into the MMX registers and do operations on each individual value separately, in one instruction, hence the SIMD (_Single Instruction Multiple Data_) nature. It is possible to have eight, one-byte values in a single MMX register:

```
%mmx0 = 
+------+------+------+------+------+------+------+------+
|   7  |   6  |  5   |   4  |   3  |   2  |  1   |   0  | Byte
+------+------+------+------+------+------+------+------+
| 0x11 | 0x22 | 0x33 | 0x44 | 0x55 | 0x66 | 0x77 | 0x88 | Values
+------+------+------+------+------+------+------+------+
```

or it is possible to have two, 4-byte long values in the register:

```
%mmx1 = 
+------+------+------+------+------+------+------+------+
|   7  |   6  |  5   |   4  |   3  |   2  |  1   |   0  | Byte
+------+------+------+------+------+------+------+------+
|          0xcc77ff88       |          0x11223344       | Values
+------+------+------+------+------+------+------+------+
```

Similarly, it is possible to have four, two-byte values as well.

New instructions
----------------

An example usage of the new instructions can be found in the [GitHub Repo](https://github.com/levex/x86-isa-extensions/tree/master/mmx) of this series. It simply adds two times four, one-byte values together.

Some simple instructions introduced by MMX can be seen in the following table:

| Instruction | Description  |
| ----------- | ------------ |
| `emms`      | Reset the MMX state |
| `paddb` / `paddw` / `paddd` / `paddq` | Add two groups of bytes, words, double-words, or quad-words |
| `psub` / `psubw` / `psubd` / `psubq` | Substract two groups of bytes, words, double-words, or quad-words |
| `pcmpeqb` / `pcmpeqw` / `pcmpeqd` / `pcmpeqq` | Compare two groups of bytes, words, double-words, or quad-words for equality  |

A more complex instruction would be the `unpck` class of instructions that allow interleaving data from two groups of data by doubling the group size:

- `punpckhbw`
- `punpckhwd`
- `punpckhdq`
- `punpcklbw` 
- `punpcklwd`
- `punpckldq`

The interleave done by `punpckhbw` is best described by the following graphic, however let us decompose this instruction into a more readable form:

- `p` => packed
- `unpck` => unpack
- `h` => high order
- `b` => from bytes
- `w` => to words

Putting it all together this seems to imply that this instruction interleaves the higher order part (top half) of a group of bytes into a group of words in the destination register. This can be still quite confusing, so here's a graphic that explains it a bit better I'd hope:

```
                                                                                               
             Source Register                          Destination Register                     
                                                                                               
+----+----+----+----+----+----+----+----+   +----+----+----+----+----+----+----+----+          
| Y7 | Y6 | Y5 | Y4 | Y3 | Y2 | Y1 | Y0 |   | X7 | X6 | X5 | X4 | X3 | X2 | X1 | X0 |          
+----+----+----+----+----+----+----+----+   +----+----+----+----+----+----+----+----+          
   |    |    |    |                            |    |    |    |                                
   |    |    |    |                            |    |    |    |                                
   |    |    |    |                            |    |    |    |                                
   |    |    |    |           +---------+------+--+-+----+  +-+                                
   |    |    |    |           |         |         |         |                                  
   |    |    |    |           |         |         |         |                                  
   |    |    |    |           v         v         v         v                                  
   |    |    |    |   +----+----+----+----+----+----+----+----+                                
   |    |    |    |   | Y7 | X7 | Y6 | X6 | Y5 | X5 | Y4 | X4 | Destination Register           
   |    |    |    |   +----+----+----+----+----+----+----+----+                                
   |    |    |    |      ^         ^         ^         ^                                       
   |    |    |    |      |         |         |         |                                       
   +----+----+----+------+---------+---------+---------+                                                                                                         
```




Successor
---------

AMD shortly caught on with its own extension to Intel's MMX, named "3DNow!" which didn't really see much success, but we will cover it in a next installment of this series.

Other successors include an "Extended MMX" from Intel, and SSE (_Streaming SIMD Extensions_). Extended MMX is of particular interest because it introduces several new, interesting instructions to MMX:

| Instruction | Description  |
| ----------- | ------------ |
| `movntq`      | Move a quad-word (64-bit value) to memory and   do not put it in the cache (bypass the cache)|
| `pextrw` | Extract a (specified) word from a group |
| `pinsrw` | Insert a word into a group at a specified location |
| `pmovmskb` | Create an 8-bit integer from the most significant bits of eight one-byte values in an MMX register |
| `pavgb` / `pavgw` | Averages the (unsigned) bytes or words |

Conclusion
----------

I hope you enjoyed this part and will enjoy the rest of the series. I would be highly appreciative of any feedback you may have. If you have an example of a use-case for MMX, it would be nice to hear from you and of course, feel free to submit a pull request to the repo linked above.
