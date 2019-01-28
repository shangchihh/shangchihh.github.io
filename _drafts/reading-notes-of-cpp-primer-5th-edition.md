---
layout: post
title: "Reading Notes of C++ Primer, 5th Edition"
assets: reading-notes-of-cpp-primer-5th-edition
category: Reading
tags: c++
toc: true
---

Reading notes of [*C++ Primer*, 5th Edition](https://www.oreilly.com/library/view/c-primer-fifth/9780133053043/).

## Part I: The Basics

### Chapter 2. Variables and Basic Types

#### 2.1. Primitive Built-in Types

The C++ standard has only state the minimum size of each built-in type:

{% include assets.html type="image" name="minimum-size.png" %}

#### 2.2. Variables

There are four ways to initialize a variable:

```c++
int units_sold = 0;
int units_sold = {0};
int units_sold{0};
int units_sold(0);
```

> The compiler will not let us list initialize (i.e. `{}`-initialization) variables of built-in type if the initializer might lead to the loss of information.

```c++
long double ld = 3.1415926536;
int a{ld}, b = {ld}; // error: narrowing conversion required
int c(ld), d = ld;   // ok: but value will be truncated
```

#### 2.4. `const` Qualifier