---
layout: post
title:  "Pointer indirection: A journey into infinity"
date:   2017-06-09 04:06:10 +0000
categories: post pointer
---

A few months ago my colleague at Imperial College London showed me a piece of
code that was part of the mandatory second-year course on Operating Systems.
The code had around 5 levels of pointer indirection. That was unusual and it
got me thinking. What is absolute maximum of indirection of pointers that
compilers can handle?

<!-- MORE -->

But wait! What do we mean by “pointer indirection” ? Perhaps, this is best
explained by actual code:

```c
int value = 0;
int *ptr = &value;
printf("%d\n",  *ptr);
```

In this simple `C` code we can see that the pointer `ptr` has level `0` of
indirection. It directly points to the variable, `value`. However, the
following sample has level `1` of indirection:

```c
int value = 1;
int *ptr0 = &value;
int **ptr = &ptr0;
printf("%d\n", **ptr);
```
The pointer `ptr` here now points to another pointer that finally points to our
`value`. It *indirectly* points to our value, and thus has an indirection level
of `1`.

### Limits

Let’s have a look at the standard first. The [C standard] specifies that an
implementation shall be able to compile and execute a source with  “12 pointer,
\[…\] declarators \[…\] modifying a \[…\] type in a declaration“. That is, the
C standard requires implementations to support at least 12 levels of
indirection, but the upper bound is left to the implementations themselves.
They can decide to only support 13 levels, or they can decide to support up to
2.147 billion levels of indirection if they so choose. The usefulness of the
latter, or even of the former, is left as an exercise to the reader.

### Testing
The first compiler I tested was the default `cc` that is running on my Late
2016 MacBook Pro, which turns out to be:
```sh
$ cc --version
 Apple LLVM version 8.1.0 (clang-802.0.42)
 Target: x86_64-apple-darwin16.5.0
 Thread model: posix
 InstalledDir: /Library/Developer/CommandLineTools/usr/bin
```
… which is a simple Clang.
An other compiler that I will be using is `gcc-6` from Homebrew, that is:
```sh
$ gcc-6 --version
 gcc-6 (Homebrew gcc 6.2.0) 6.2.0
 Copyright (C) 2016 Free Software Foundation, Inc.
 This is free software; see the source for copying conditions.  There is NO
 warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```
.. which as expected is GCC 6.2.0

So, how do you actually test this? I quickly cooked together a simple (and
extremely naive) implementation that helps:
```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int
main(int argc, char **argv)
{
    int i, j, n = 0;
    FILE *fp;

    if (argc != 2) {
        printf("USAGE: %s INDIRECTION\n", argv[0]);
        return 1;
    }

    n = atoi(argv[1]);
    printf("Indirection: %d\n", n);

    fp = fopen("run.c", "w+");
    if (fp == NULL) {
        printf("Error creating \"run.c\"\n");
        return 2;
    }

    fprintf(fp, "#include <stdio.h>\n");
    fprintf(fp, "#include <stdlib.h>\n");
    fprintf(fp, "\n");
    fprintf(fp, "int main(int argc, char **argv) {\n");
    fprintf(fp, "    int i0 = %d;\n", n);
    for (i = 1; i < n; i ++) {
        fprintf(fp, "int ");
        for (j = 0; j < i; j ++)
            fprintf(fp, "*");
        fprintf(fp, "i%d = &i%d;\n", i, i - 1);
    }
    fprintf(fp, "    printf(\"%%d\", ");
    for (i = 1; i < n; i ++)
        fprintf(fp, "*");
    fprintf(fp, "i%d);\n", n - 1);
    fprintf(fp, "}\n");

    return 0;
}
```

Arguably not well optimized or anything, but it does the job of generating C
source code that contains the given number of indirection. In short, it
generates files of the sort:
```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    int i0 = 4;
int *i1 = &i0;
int **i2 = &i1;
int ***i3 = &i2;
    printf("%d", ***i3);
}
```
In this example the indirection level is `3`.

So, let’s test this previous snippet with the two compilers:
```sh
$ cc run.c 
$ ./a.out
4
$ gcc-6 run.c
$ ./a.out
4
```
As expected by the standard, this is supported. Let’s try with a larger number,
say 1000, but this time also check how long each compilation takes.
```sh
$ ./generator 1000
Indirection: 1000
$ time cc run.c -o run-cc-1000
0.18 real         0.13 user         0.03 sys
$ time gcc-6 run.c -o run-gcc6-1000
1.88 real         1.52 user         0.26 sys
$ ./run-cc-1000
1000
$ ./run-gcc6-1000
1000
```

As we can see, both have compiled and executed successfully, but interestingly
GCC 6.2.0 took a lot longer than the Clang compiler. Let’s continue on and test
at indirection level 10000:
```sh
$ ./generator 10000
Indirection: 10000
$ cc run.c -o run-cc-10000
cc run.c -o run-cc-10000
 clang: error: unable to execute command: Illegal instruction: 4
 clang: error: clang frontend command failed due to signal (use -v to see invocation)
 Apple LLVM version 8.1.0 (clang-802.0.42)
 Target: x86_64-apple-darwin16.5.0
 Thread model: posix
 InstalledDir: /Library/Developer/CommandLineTools/usr/bin
 clang: note: diagnostic msg: PLEASE submit a bug report to http://developer.apple.com/bugreporter/ and include the crash backtrace, preprocessed source, and associated run script.
 clang: note: diagnostic msg:
 ********************
 
 PLEASE ATTACH THE FOLLOWING FILES TO THE BUG REPORT:
 Preprocessed source(s) and associated run script(s) are located at:
 clang: note: diagnostic msg: /var/folders/25/5ggbk47j2038sjfz9m6ckt1h0000gn/T/run-71b506.c
 clang: note: diagnostic msg: /var/folders/25/5ggbk47j2038sjfz9m6ckt1h0000gn/T/run-71b506.sh
 clang: note: diagnostic msg: /var/folders/25/5ggbk47j2038sjfz9m6ckt1h0000gn/T/run-71b506.crash
 clang: note: diagnostic msg:
 
 ********************
```
What just happened. Looks like clang crashed on an illegal instruction (SIGILL).
However, after looking at the crash trace and building upstream, the real source
of the bug is that the code causes a stack overflow. Clang (the LLVM frontend)
crashes in `clang/lib/Parse/ParseDecl.cpp` in function `ParseDeclaratorInternal`.
The function seems to call itself recursively to parse the `*` tokens, and
the stack is too small. Too bad. Eventually, I should/will file a bug report.

GCC on the other hand managed to compile it, but it took an awful lot of time:
```sh
$ time gcc-6 run.c -o run-gcc6-10000
2419.57 real      2152.83 user        35.52 sys
```
Woah! That is indeed a lot of time, around 40 minutes.
Let’s use binary search and find what is the pointer indirection that clang can
handle. We know it worked for `n0` = 1,000 and it failed at `nF` = 10,000.
Naturally, the next step is to test at `n1` = 4,500. Generating the file with
4,500 levels of indirection and then firing up clang yields the following:

```
clang: error: unable to execute command: Illegal instruction: 4
```

Next step, `n2` = 2,750, yielding an empty string. Wow, the compilation
succeeded! Now we know the fault happens between 2,750 and 4,500 levels of
indirection. Next try is at `n3` = 3,625. Once again, we get an empty string,
compilation succeeded and we get the expected result when ran. Next step, `n4`
= 4,062. After bisecting, I got the result of `nf` = 3,872. clang (at least the
version my MacBook Pro is running) seems to support **up to 3,872 levels of
pointer indirection**.

Interesting? Not sure. Useful? Hopefully not. Fun?
Absolutely.
