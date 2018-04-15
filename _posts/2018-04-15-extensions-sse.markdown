---
layout: post
title: "x86 ISA Extensions part II: SSE"
date:   2018-04-15 16:42:00 +0100
categories: post x86-extensions
---

Welcome back to this series exploring the many extensions the x86 architecture has seen over the past decades. In this installment of the series, we will be looking at the successor to [MMX](https://dev.to/ilevex/x86-isa-extensions-part-i-mmx-1hjf): Streaming SIMD Extensions， or SSE for short. Most of these instructions are SIMD (as their name implies), which stands for **S**ingle **I**nstruction **M**ultiple **D**ata. In brief, SIMD instructions are similar to the ones we’ve covered in the MMX article: an instruction can possibly work on multiple data groups.

SSE was introduced in 1999 with Intel’s Pentium III soon after Intel saw AMD’s “3DNow!” extension (we will cover this extension in a future installment, but right now I lack access to an AMD machine that I could use 🙂). A question arises naturally: SSE wasn’t the first SIMD set that Intel has introduced to the x86 family of processors, so why did Intel create a new extension set? Unfortunately, MMX had two major problems at the time. First, the registers it “introduced” were aliases of previously existing registers (amusingly, this was touted as an advantage for a while because of the easier context switching), this meant that floating points and MMX operations couldn’t coexist. Second, MMX only worked on integers, it had no support for floating points which was an increasingly important aspect of 3D computer graphics. SSE adds dozens of new instructions that operate on an independent register set and a few integer instructions that continue to operate on the old MMX registers.

<!-- MORE -->

*(A slight note before we start: In this article “SSE” refers to the very first SSE extension introduced by Intel. In future installments of this series, we will explore SSE2, SSE3, SSSE3, SSE4 and SSE4.1, but here we focus on “SSE1”.)*

## Do you have SSE?
As with all instruction set extensions, there is a chance that your CPU does not have it. The chances are once again pretty slim with SSE, given its age, but it’s always interesting to see how one can feel sure about its CPU’s support for SSE.

On Linux:
```sh
$ cat /proc/cpuinfo | grep -wq sse && echo “SSE available”  || echo “SSE not available”
```

On OS X/macOS:
```sh
$ sysctl machdep.cpu.features | grep -wq SSE && echo “SSE available”  || echo “SSE not available”
```

Alternatively, CPUID offers a way to gather this information on bare-metal or in an OS-agnostic way. SSE is indicated by CPUID leaf 1, EDX bit 25:

```assembly
.text
.globl _is_sse_available
_is_sse_available:
    pushq   %rbx

    movq    $1, %rax
    cpuid
    movq    %rdx, %rax
    shrq    $25, %rax
    andq    $1, %rax

    popq    %rbx
    ret
```

Once you are satisfied that your CPU allows for SSE instructions, it’s time to dive in to the specifics of SSE!

## Registers

Since SSE introduces actual, new registers (in contrast with its predecessor), I think it’s useful to have a quick glance at them. SSE added eight, 128-bit registers named: `%xmm0, %xmm1, ..., %xmm7`. (Amusingly, `xmm` is the reverse of `mmx` which is the name of the MMX registers, I assume this is meant as a pun, but I couldn’t find a source confirming) In stark contrast with MMX, SSE does not allow for multiple data types. Each XMM register can hold four, 32-bit [single-precision floating points](https://en.m.wikipedia.org/wiki/Single-precision_floating-point_format), while MMX could hold different widths of integers.

```
%xmm0, %xmm1, ..., %xmm7:
*- - - - - - - - -*- - - - - - - - -*- - - - - - - - -*- - - - - - - - -*
| 32-bit SP float | 32-bit SP float | 32-bit SP float | 32-bit SP float |
*- - - - - - - - -*- - - - - - - - -*- - - - - - - - -*- - - - - - - - -*
|                            128-bit value                              |
*- - - - - - - - -*- - - - - - - - -*- - - - - - - - -*- - - - - - - - -*
```

In this figure, each line represents a data type that can be in the XMM register with SSE. I’ve put the “128-bit value” in the figure, since if you only load data into the register and not issue any floating point operation, then it can be potentially any unstructured data. However, when using floating points only the four, single-precision floating points are supported as data in the register. Unstructured data can potentially cause exceptions to happen.

To control the state of some operations, an additional control and status register is added, dubbed `MXCSR`. This register cannot be accessed using the `mov` family of instructions, rather SSE adds two new instructions that allow the register to be loaded and stored, `LDMXSCR` & `STMXSCR`. The figure shows its layout and then explains its usage within the SSE environment.


![The MXCSR register](https://thepracticaldev.s3.amazonaws.com/i/0v95lbtolwb47b0fgs7y.png)


Bits 0-5 in MXCSR are flags that show that a certain type of floating-point exception occurred, they are also sticky meaning that the user (or the OS) has to reset them manually after an exception, otherwise they’ll stay set forever. Bits 7-12 are masking bits, they can be used to used to stop the CPU from issuing an exception when certain conditions pertaining to the specific exception are met, in which case the processor will return a value (qNaN, sNaN, definite integer or one of the source operands; see [1] for more details).

For more information on the specific meanings of the registers, look at [1], Chapter 10.2.3.

# Instructions

Now that we have covered the registers introduced in the SSE extension, let’s have a look at what new instructions have Intel added and their implications. To utilize SSE to its fullest extent, the very first step to be taken is to move data into the new XMM registers, SSE offers a couple instructions, out of which the following (`movaps` & `movups`) are the most common:

```assembly
# Create a memory location with four single-prec floats
vector0: .dq 3.14, 2.71, 1.23, 4.56
scalar0: .dd 1234
vector1: .dq 3.62, 6.73, 8.41, 9.55

movaps vector0, %xmm0
movups vector1, %xmm1
```

`movaps` stands for **MOV**e **A**ligned **P**acked **S**ingle Precision Float, and `movups` stands for the same, but **U**naligned. The distinction between aligned and unaligned access is important, and generally developers should aim for aligned access whenever possible for better overall performance.

Now that we have managed to move data into an XMM register, let’s do something with it. A trivial example and one that we explored previously is some simple vector manipulation:

```assembly
# assuming vector0 and vector1 from the previous snippet

movaps vector0, %xmm0
movups vector1, %xmm1

addps %xmm0, %xmm1 # ADD Packed Single precision float
subps %xmm0, %xmm1 # undo previous operation
maxps %xmm0, %xmm1 
```

`maxps` is a very handy instruction: it compares each of the four single-precision floats in the XMM registers and then moves the larger float into the destination operand (it can be either a register like `%xmm1` or a 128-bit memory location). This instruction alone can save a large chunk of cycles by avoiding a  loop and many `cmp` and branch instructions.

An other interesting aspect of the SSE extensions are cacheability controls. The application programmer can now tell the CPU that some memory is *“non-temporal”*, that is it won’t be needed in the near future so do not pollute the cache with it, like so: 

```assembly
movntps %xmm0, vector0
```

The reverse (i.e., if the programmer knows that a certain memory location will be needed in the near future) can also be signaled to the processor using the `PREFETCH` family of instructions:

| Instruction | Pentium III | Pentium 4/Xeon | Temporal?
|:--|:--|:--|:--|
| `prefetch0` | L2 or L1 | L2 | Temporal |
| `prefetch1` | L2 | L2 | Temporal |
| `prefetch2` | L2 | L2 | Temporal |
| `prefetchnta` | L1 | L2 | Non-temporal |

## Conclusion

The next extension we will be looking at will be the SSE2 extension set that builds on the foundations of SSE and MMX to deliver better performance. Starting with the new installment, we will introduce benchmarks, too. In the meantime, have a look at a cache of examples in the [GitHub Repo for the series!](https://github.com/levex/x86-isa-extensions) Until next time!

## References

1: [Intel IA-32 Software Development Manual, Chapter 11.5.2: SIMD Floating-Point Exception Conditions](https://software.intel.com/en-us/articles/intel-sdm)
