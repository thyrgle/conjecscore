from .utils import register_problem, parse_integer


def score(n: int):
    orbit = 0
    magnitude = n.bit_length()
    while n != 1:
        if n % 2 == 1:
            orbit += 1
            n = 3 * n + 1
        else:
            n = n // 2
    return int((orbit / magnitude) * 1000)


register_problem("collatz", score, "Collatz Orbits",
                 "collatz.j2", "highest", "collatz", parse_integer,
                 "collatz.svg", submission_type="text")
