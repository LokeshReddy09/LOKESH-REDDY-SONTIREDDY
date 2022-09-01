Non-Linear Solvers
Contents:
1 Newton’s Method
1.1 Refining the Pseudocode
1.2 Where is the Code?
1.3 Now We are Ready!
1.4 Cleaning Up The Implementation
1 Newton’s Method

We are going to start with my favorite solver, Newton’s Method. Out of the four methods we will discuss, this one has the shortest pseudocode.

    Compute xn+1=xn−f(xn)df(xn)

until |xn+1−xn|≤eps

 

One of my recurring sidebars this semester has been “It is just notation.” While there is a lot of notation here, it is all based on things we have seen before.

If we look at the pieces:

    xn+1

- next guess for a solution
xn
- current guess for a solution
f
- function for which a solution is desired
df
or f′ - derivative of f
eps

    - tolerance

Notice the requirements?

    We must have both f

and its derivative df
.
df(xn)

    must be non-zero.

1.1 Refining the Pseudocode

Our starting pseudocode was:

    Compute xn+1=xn−f(xn)df(xn)

until |xn+1−xn|≤eps

While this code is complete, it is not something we can immediately start coding. Let us start by a slight change in notation.

    while |xn+1−xn|>eps

:

        xn+1=xn−f(xn)df(xn)

This needs to be something we can write in code. Mathematical notation is usually difficult to preserve in formal code. Let us preemptively adjust our notation.

while abs(x_np1 - x_n) > eps:
    x_np1 = x_n - (f(x_n) / df(x_n))

Let us clarify our inputs by making this a proper function.

def newtons_method(f, df, eps):

    while abs(x_np1 - x_n) > eps:
        x_np1 = x_n - (f(x_n) / df(x_n))

It is now clear that f
, df, and eps are arguments passed in when newtons_method is invoked. Both x_n and x_np1 are function local variables. This also brings up an issue. Where is our initial guess for xn

?

def newtons_method(f, df, x_n, eps):

    while abs(x_np1 - x_n) > eps:
        x_np1 = x_n - (f(x_n) / df(x_n))

That is much better.
1.2 Where is the Code?

You are probably definitely surprised that I have not started writing C++, Python, or Rust code yet. Why am I not ready, yet?

    x_np1 needs a better name.
    What if |xn−xpn1|>eps

is never false?
What if df(xn)
is small?
xn

    needs to be updated.

These can all be addressed quickly. Let us start by addressing 1 and 4:

def newtons_method(f, df, x_n, eps):

    while abs(x_np1 - x_n) > eps:
        next_x_n = x_n - (f(x_n) / df(x_n))

        x_n = next_x_n

We are now left with two problems:

    x_np1 needs a better name.
    What if |xn−xpn1|>eps

is never false?
What if df(xn)
is small?
xn

    needs to be updated.

These two problems are both solved with a loop counter.

MAX_ITERATIONS = 100

def newtons_method(f, df, x_n, eps):

    n = 0

    while abs(x_np1 - x_n) > eps:
        next_x_n = x_n - (f(x_n) / df(x_n))

        x_n = next_x_n
        n = n + 1

        if n >= MAX_ITERATIONS:
            break

    return x_n

Yes, I did silently add the missing return statement. Did you notice it was missing?
1.3 Now We are Ready!

I am going to implement this code in Python 3 (3.7 to be exact). Let us make a quick draft.
newtons_method_1.py

Notice how I used a direct translation of the pseudocode newtons_method function? Sometimes we can get away with a transliteration.

The tolerance, eps is now an argument to newtons_method (albeit one with a default argument value). This is something I usually define and use throughout a codebase.

Let us make some quick improvements.
newtons_method_2.py

I added the number of iterations as a return value. Python allows us to return multiple values as a tuple

    return n, x_n

and unpack the result

        num_iterations, solution_newton = newtons_method(f, df, initial_guess)

Now if I run the code with

./newtons_method_2.py 2

the output includes the number of iterations.

x = 1.0000 | f(x) = 0.0000 | 5 iterations

This is a reasonable implementation.
1.4 Cleaning Up The Implementation

It is now time to add type hints.
newtons_method_3.py

Let us add some docstrings in the Google/Sphinx style.
newtons_method_4.py

If we run pylint using python -m pylint newtons_method_4.py, we receive a few warnings:

************* Module newtons_method_4
newtons_method_4.py:1:0: C0111: Missing module docstring (missing-docstring)
newtons_method_4.py:13:0: C0103: Argument name "f" doesn't conform to snake_case naming style (invalid-name)
newtons_method_4.py:13:0: C0103: Argument name "df" doesn't conform to snake_case naming style (invalid-name)
newtons_method_4.py:31:4: C0103: Variable name "n" doesn't conform to snake_case naming style (invalid-name)
newtons_method_4.py:35:8: C0103: Variable name "n" doesn't conform to snake_case naming style (invalid-name)
newtons_method_4.py:43:0: C0111: Missing function docstring (missing-docstring)
newtons_method_4.py:57:4: C0103: Function name "f" doesn't conform to snake_case naming style (invalid-name)
newtons_method_4.py:57:4: C0103: Argument name "x" doesn't conform to snake_case naming style (invalid-name)
newtons_method_4.py:60:4: C0103: Function name "df" doesn't conform to snake_case naming style (invalid-name)
newtons_method_4.py:60:4: C0103: Argument name "x" doesn't conform to snake_case naming style (invalid-name)
newtons_method_4.py:6:0: W0611: Unused import typing (unused-import)
newtons_method_4.py:7:0: W0611: Unused Fraction imported from fractions (unused-import)

------------------------------------------------------------------
Your code has been rated at 6.76/10 (previous run: 6.76/10, +0.00)

In this case we can ignore the warnings dealing with x, n, f, and df. Why? We are sticking with the mathematical notation from the original pseudocode. That leaves us with:

newtons_method_4.py:1:0: C0111: Missing module docstring (missing-docstring)
newtons_method_4.py:43:0: C0111: Missing function docstring (missing-docstring)
newtons_method_4.py:6:0: W0611: Unused import typing (unused-import)
newtons_method_4.py:7:0: W0611: Unused Fraction imported from fractions (unused-import)

Since this is a quick example, we can forgo a module docstring. That leaves us with a docstring for main and a few unused imports.
newtons_method_5.py

We are left with one more warning:

newtons_method_5.py:6:0: W0611: Unused Fraction imported from fractions (unused-import)

So far we have been using the float data type (i.e., finite precision). Let us switch to the Python fractions library.
newtons_method_6.py

That leaves us with

x = 1.0000000469590518 | f(x) = 9.391810573688986e-08 | 5 iterations

That is worse than before! Since are using fractions, rounding error propagates differently. This can be solved by tweaking

EPSILON = Fraction(1, 10**6)

