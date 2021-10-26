import random


def chance(probability):
    if not 0 <= probability <= 1:
        raise ValueError(f"incorrect probability value: '{probability}'")

    return random.random() < probability


if __name__ == "__main__":
    for _ in range(10):
        print(chance(0.5))
