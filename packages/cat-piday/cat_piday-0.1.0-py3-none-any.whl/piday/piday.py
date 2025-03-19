import click
import time
from tqdm import tqdm
from termcolor import colored
import math

def points(n: int):
    for m in range(n, 0, -1):
        x = (n**2 - m**2) / (m**2 + n**2)
        y = 2 * m * n / (m**2 + n**2)
        yield x, y

def get_bounds(n: int):
    low_darbu = 0
    high_darbu = 0
    x_prev = 0
    y_prev = 1
    for x, y in tqdm(points(n), total=n):
        low_darbu += (x - x_prev) * y
        high_darbu += (x - x_prev) * y_prev
        x_prev = x
        y_prev = y
    return low_darbu, high_darbu

@click.command()
@click.option('--n', default=1000000, help='Number of points to use.')
def main(n: int):
    """Estimate Pi using the Monte Carlo method."""
    current_time = time.time()
    low, high = get_bounds(n)
    print(f"Time taken: {time.time() - current_time}")

    low *= 4
    high *= 4
    pi = math.pi
    computed_pi = (low + high) / 2

    low_str = f"{low:.15f}"
    high_str = f"{high:.15f}"
    for theoretical_diff, (low_digit, high_digit) in enumerate(zip(low_str, high_str)):
        if low_digit != high_digit:
            break
        else:
            theoretical_diff += 1

    print(f"\npi is between: {colored(low_str[:theoretical_diff], 'green')}{colored(low_str[theoretical_diff:], 'red')} and {colored(high_str[:theoretical_diff], 'green')}{colored(high_str[theoretical_diff:], 'red')}")

    pi_str = str(pi)
    computed_pi_str = f"{computed_pi:.15f}"
    for real_diff, (pi_digit, computed_pi_digit) in enumerate(zip(pi_str, computed_pi_str)):
        if pi_digit != computed_pi_digit:
            break
        else:
            real_diff += 1

    print(f"\nApproximation: {colored(computed_pi_str[:theoretical_diff], 'green')}{colored(computed_pi_str[theoretical_diff:real_diff], 'yellow')}{colored(computed_pi_str[real_diff:], 'red')}")
    print(f"true value   : {pi:.15f}")
    print(f"Error        : {abs(pi - (low + high) / 2):.4e}")

if __name__ == '__main__':
    main()