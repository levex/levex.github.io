---
layout: post
title:  "waccOS - Part I"
date:   2017-03-05 12:00:00 +0000
categories: kernel waccos
---

Imperial College’s Computer Science undergraduates will be already familiar
with the language *WACC*. It is a While-like language that is part of the
mandatory 2nd-year Compilers course and the Integrated Laboratory coursework.
Basically, the goal is to create a compiler for the language *WACC* (for which
you are given a specification) in your language of choice in 4 weeks. After the
initial 4 weeks, you have 2 extra weeks to implement some extensions of your
own choice. Some suggested extensions range from adding fully recursive pair
types, dynamic typing, all the way to garbage collection and even static
analysis for dynamic types. However, there was one which we spotted fairly
early on. **Write an operating system.**

<!-- MORE -->

```
waccOS % cat /etc/release
waccOS 1.0
Kernel compiled via: WACC-04-HASKELL
AUTHORS: Levente Kurusa
         Atanas Gospodinov
         Daniel Zvara
```
To get a feel of the original (I say original, because obviously, we extended
it just enough to support an operating system) *WACC* language, here is a
Fibonacci sequence implementation:

```
begin
int fibonacci(int n) is
  if n <= 1 then
    return n
  else
    skip
  fi ;
  int f1 = call fibonacci(n - 1) ;
  int f2 = call fibonacci(n - 2) ;
  return f1 + f2
end

println "This calculates the nth fibonacci number recursively." ;
print "Please enter n (should not be too large): " ;
int n = 0;
read n ;
print "The input n is " ;
println n ;
print "The nth fibonacci number is " ;
int result = call fibonacci(n) ;
println  result
end
```

As one can see, the language uses `begin` and `end ` keywords instead of curly
brackets and also has no notion of ` void`, even requiring a special keyword
for calling functions, `call`. All function return values have to be assigned
to a local variable and the language has no notion of global variables. *WACC*
uses an implicit main function, sort of like what Python can do. It also uses
built-in functions like `print`, `read` to be able to address the outside
world. The language has been exclusively designed to be fairly easy to write a
compiler for. But not for low-level systems-level programming.

So, what did my team do? We built a fairly simple operating system for the
(in)famous *Raspberry Pi ARM* board. Given the freedom of writing our own
compiler and implementing any extensions for it, we decided we will implement
extensions that are low-level enough to support an operating system kernel. The
result? A C-like `WACC` with all the famous features you can guess, like
pointers, structures, and even inline assembly. This how some our code looks
like now:

```
int test_frame(uint32 a) is
  int f = a / 0x1000;
  int i = INDEX_BIT(f);
  int o = OFFSET_BIT(f);
  return (*(frames+i) & (1 << o));
end

bool check_n_frames_free(int start, int n) is
  for (uint32 j = 0; j < n; j++) do
    if (test_frame(start + 0x1000 * j) != 0) then
      return false;
    end
  end

  return true;
end
```

Before diving into the operating system we wrote, let’s talk about how we built
the compiler. We decided that the best language we can choose for writing our
compiler is Haskell, because of its excellent support for parsing and a
plethora of wonderful tools (that is, mostly type classes) to help us create
the compiler. Originally, people were supposed to be using the stack for every
local variable, however, we implemented a register allocator based on the
[Linear Scan Register
Allocation](http://web.cs.ucla.edu/~palsberg/course/cs132/linearscan.pdf)
algorithm devised by MIT and IBM computer scientists back in the 1990s. This
allowed us to avoid overusing the stack and made our resulting assembly code
just a bit more deterministic.

One of the first things we implemented in *waccOS* is a method to communicate
via the serial port so that we could save the time that we would otherwise need
to implement a full-blown terminal emulator with font rendering and all the
escape codes. Instead, we opted for implementing a driver for the *UART* that
exists as GPIO #14 and #15 on the board. However,  this was not as easy as it
sounds. We’ve hit two major obstacles, including a quite severe one. We
followed the specification of the *UART* closely and even tried copy/pasting
tutorial code, but for some reason, the *UART* console on my Linux box was not
displaying anything. Maybe it’s the *FTDI* chip we use? Maybe the cable is
damaged? Maybe the *Raspberry PI* is faulty? After countless days of debugging
without success, it struck me. Maybe, we should try reverting the boot firmware
to an older version! We reverted to a May 2016 version and surprise, it worked!
I’ll eventually write a separate blog post on this issue because the way we
debugged this issue and all those contradicting results that came in were
really amusing in retrospect.  

Second issue also constitutes a blog post. This time we spent a fair amount of
time figuring out that we needed to have our strings aligned to a 16-byte
boundary for our *UART* code to work. This taught us the lesson that ARM
unaligned/aligned access is a wonderful piece and is definitely worth a blog
post. For example, while on recent ARM processors most instructions support
unaligned access, `STM` and `LDM` (Store Multiple and Load Multiple,
respectively) do not, in fact, they result in undefined behavior! (Which
sometimes confused us, because it seemed to work every once in a while)

Anyway, after we got the *UART* working, we decided that we should write a very
simple, but interactive shell. This shell later formed a critical part as we
could both test our compiler’s new features and *waccOS*’s new features as well
with ease. For example, here is us testing the *ps* functionality which
basically tests the scheduler: 

{% include image center=1 name="sched_test.png" caption="the ps command in the interactive kernel shell" %}

Or here is us debugging the *ext2* driver:
{% include image center=1 name="ext2_driver.png" caption="ext2 driver outputting debug information about the volume" %}

Overall, this project has been massive fun. I plan to go over each important
feature of our operating system kernel and write a blog post on how they’ve
been built and the challenges we’ve faced. In the next part of this series I
will talk a little about ARM’s way of dealing with unaligned access since this
has proved to be a really important knowledge that anyone planning to do
bare-metal programming for ARM has to know.

*PS: The source code for the compiler is sadly not publicly available due to academic
integrity, however if you send me a message, I'll send you a zip. Meanwhile, the
OS is available [here](https://github.com/levex/wacc-os)
