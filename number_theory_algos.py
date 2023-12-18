"""Number Theory Algorithms

Implementations of common number theory algos to make life easier
Mostly relevant to RSA encryption scheme
"""
from typing import List


def euclidean_algo(a: int, b: int):
    """
    This function is an implementation of the Euclidean Algorithm to find GCD
    Prints all intermediate steps in LaTeX.
    Args:
    a -- first int arg
    b -- second int arg
    """
    # print intro
    print(f"First, find ({a}, {b})")
    gcd = []
    back = []
    # swap, as gcd(a, b) = gcd(b, a)
    if b > a:
        temp = b
        b = a
        a = temp
    # implementation of Euclidean algorithm
    print("\\begin{align*}")

    # Inv: a, b >= 0
    while b != 0:
        # gcd(a, b) = gcd(b, a % b)
        r = a % b
        # formatted printing fencepost
        if r > 0:
            print(f"{a} &= {b}({a // b}) + {r}\\\\")
            back.append(f"{r} = {a} - {b}({a // b})")
        else:
            print(f"{a} &= {b}({a // b}) + {r}")
            back.append(f"{r} = {a} - {b}({a // b})")
        gcd.append(f"({a}, {b})")
        a = b
        b = r
    # b = 0 iff gcd calls have terminated
    gcd.append(f"({a}, 0)")
    print("\\end{align*}")
    print(f"Thus, ${' = '.join(gcd)} = {a}$\n")


def mod_exponentiation(base: int, exponent: int, mod: int):
    """
    This function is an implementation of the 'fast' modular exponentiation algorithm.
    Prints all intermediate steps in LaTeX when computing (base^exponent) % mod.
    Args:
    base -- int base
    exponent -- int power
    mod -- int modulus
    """
    binary = "{0:b}".format(exponent)[::-1]
    mod_i_lst = []

    print(f"Let's calculate ${base}^{{{exponent}}}\\,(\\text{{mod }}{mod})$\n\n")

    print(
        """Note that we can break up the exponent to its corresponding 
            binary parts to make things easier."""
    )

    # print "broken up exponent" of base^exponent
    lst = [f"{base}^{{{2 ** i}}}" for i in range(len(binary)) if binary[i] == "1"]
    lst_str = "".join(lst)
    print(
        f"${base}^{{{exponent}}}\\,(\\text{{mod }}{mod}) = {lst_str} \\,(\\text{{mod }}{mod})$\n"
    )

    mod_i = base % mod  # initialize to 0th power mod
    print(
        f"${base}^1 \\,(\\text{{mod }}{mod}) = {base} \\,(\\text{{mod }}{mod}) = {mod_i}$\\\\"
    )
    mod_i_lst.insert(0, mod_i if binary[0] == "1" else -1)

    # get the rest of the powers
    for i in range(1, len(binary) - 1):
        print(
            f"${base}^{{{2 ** i}}} \\,(\\text{{mod }}{mod}) = \\left({base}^{{{2 ** (i - 1)}}} \\,(\\text{{mod }}{mod})\\right)^2\\,(\\text{{mod }}{mod}) = {mod_i}^2 \\,(\\text{{mod }}{mod}) = {mod_i * mod_i}\\,(\\text{{mod }}{mod}) = {mod_i * mod_i % mod}$\\\\"
        )
        mod_i = (mod_i * mod_i) % mod
        if binary[i] == "1":
            mod_i_lst.insert(0, mod_i)
        else:
            mod_i_lst.insert(0, -1)

    print(
        f"${base}^{{{2 ** (len(binary) - 1)}}} \\,(\\text{{mod }}{mod}) = \\left({base}^{{{2 ** (len(binary) - 2)}}} \\,(\\text{{mod }}{mod})\\right)^2\\,(\\text{{mod }}{mod}) = {mod_i}^2 \\,(\\text{{mod }}{mod}) = {mod_i * mod_i}\\,(\\text{{mod }}{mod}) = {mod_i * mod_i % mod}$"
    )
    mod_i_lst.insert(
        0, (mod_i * mod_i) % mod
    )  # guaranteed spot from binary string property

    # get the second non-zero in the list
    second = -1
    for i in range(1, len(mod_i_lst)):
        if mod_i_lst[i] > -1:
            second = i
            break

    if second == -1:
        print(
            f"\\boxed{{${base}^{exponent}\\,(\\text{{mod }}{mod}) = {mod_i_lst[0]}$}}"
        )
        return
    x_i = 0
    # now go multiply
    print(f"\nCalculating ${base}^{{{exponent}}}\\,(\\text{{mod }}{mod})$, we have: \n")

    ans = (mod_i_lst[second] * mod_i_lst[0]) % mod
    # LaTeX form of the multiplication step
    print(
        f"\n$({base}^{{{2 ** (len(binary) - 1)}}}\\,(\\text{{mod }}{mod}) \\cdot {base}^{{{2 ** (len(binary) - 1 - second)}}}\\,(\\text{{mod }}{mod}))\\,(\\text{{mod }}{mod}) = ({mod_i_lst[0]} \\cdot {mod_i_lst[second]})\\,(\\text{{mod }}{mod}) = ({mod_i_lst[second] * mod_i_lst[0]})\\,(\\text{{mod }}{mod}) = {ans} = x_0$\\\\"
    )
    for i in range(second + 1, len(mod_i_lst)):
        if mod_i_lst[i] > 0:
            before = ans
            ans = (ans * mod_i_lst[i]) % mod
            x_i += 1
            print(
                f"\n$(x_{x_i - 1} \\cdot (({base}^{{{2 ** (len(binary) - 1 - i)}}})\\,(\\text{{mod }}{mod}))) \\,(\\text{{mod }}{mod})= ({before} \\cdot {mod_i_lst[i]})\\,(\\text{{mod }}{mod}) = ({before * mod_i_lst[i]})\\,(\\text{{mod }}{mod}) = {ans} = x_{x_i}$\\\\"
            )
    print(f"$$\\boxed{{{base}^{{{exponent}}}\\,(\\text{{mod }}{mod}) = {ans}}}$$")


def base10_to_base2(input_base10: int) -> str:
    """
    Reinvent the wheel base-10 to base-2 conversion.
    Args:
    input_base10 -- base 10 number (non-negative)
    Return:
    binary string in base 2 representation of input_base10
    """
    quotient: int = input_base10 // 2
    remainder: int = input_base10 % 2
    # check if need to recurse
    if quotient == 0:
        return remainder
    return base10_to_base2(quotient) + remainder


# Exponential encryption functions


def exp_encrypt(message: int, e: int, p: int):
    """
    Encrypts message
    Args:
    message -- int number converted message block
    e -- exponentiation constant
    p -- int modulo constant
    """
    return (message**e) % p


def exp_decrypt(ciphertext: int, d: int, p: int):
    """
    Decrypts message
    Args:
    ciphertext -- int number converted cipher block
    """
    return f"{(ciphertext ** d) % p}".zfill(4)


def char_to_nums(input_str: str):
    """Encodes string input with char byte encodings in a list."""
    out = "".join([f"{i}".zfill(2) for i in input_str])
    n = 4
    return [int(out[i : i + n]) for i in range(0, len(out), n)]


# list input
def nums_to_char(num_list: List[int]):
    """Inverse op of char_to_nums(input). Undoes numerical encoding."""
    out = ""

    for i in num_list:
        token = i
        out += chr(int(token[:2]) + ord("a"))
        out += chr(int(token[2:]) + ord("a"))
    return out


def main():
    """Run defined algos."""
    # Euclidean algo
    euclidean_algo(6, 9)
    euclidean_algo(25, 40)
    euclidean_algo(14, 85)
    euclidean_algo(66, 561)
    euclidean_algo(66, 561)
    euclidean_algo(70, 1869)
    euclidean_algo(3145, 23001)
    euclidean_algo(3145, 23001)

    # Mod exponentiation
    mod_exponentiation(13, 6600, 6601)

    # Encryption algo
    encrypted = [1213, 902, 539, 1208, 1234, 1103, 1374]
    decrypted = []
    d = 797
    p = 2591

    for i in encrypted:
        decrypted.append(exp_decrypt(i, d, p))
    print(decrypted)
    print(nums_to_char(decrypted))


if __name__ == "__main__":
    main()
