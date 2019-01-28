---
layout: post
title: "Reading Notes of Build Your Own Lisp"
category: Reading
tags: c lisp interpreter
toc: true
---

Reading notes of [*Build Your Own Lisp*](http://www.buildyourownlisp.com).

## Chapter 4. An Interactive Prompt

The simplest version is using `fputs` to print the prompt and using `fgets` to get the input:

```c
#include <stdio.h>

static char input[2048];

int main(int argc, char** argv) {
  puts("Lispy Version 0.0.0.0.1");
  puts("Press Ctrl+c to Exit\n");

  while (1) {
    fputs("lispy> ", stdout);
    fgets(input, 2048, stdin);
    printf("No you're a %s", input);
  }

  return 0;
}
```

However, on the Linux or Mac platform, we are unable to move around on the line. We cannot delete and edit the input in case we make a mistake. The console handles the arrow keys to create these weird characters `^[[D` or `^[[C`.

One of the solutions is to use the library [editline](https://github.com/troglobit/editline).

For the elegance of code, we can also make a fake `readline` function and a fake `add_history` function on the Windows platform.

```c
static char buffer[2048];

char *readline(char *prompt)
{
    fputs(prompt, stdout);
    fgets(buffer, 2048, stdin);
    char *cpy = malloc(strlen(buffer)+1);
    strcpy(cpy, buffer);
    cpy[strlen(cpy)-1] = '\0';
    return cpy;
}

void add_history(char *unused) {}
```

The complete code: [`prompt.c`](https://github.com/shangchihh/buildyourownlisp/blob/master/prompt.c).
