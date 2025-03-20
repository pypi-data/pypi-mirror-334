import argparse
from functools import partial
from itertools import chain, combinations
from typing import Callable, Iterable, Iterator, Optional


def map_and_join(numbers: Iterable) -> str:
    return "".join(map(str, numbers))


def calculate_fake_hex(word: str) -> Iterator[int]:
    hexA = 10
    for ch in word.strip().upper():
        yield (ord(ch) - ord("A") + hexA)


def calculate_digital_root(number: int) -> Iterator[int]:
    total = sum(map(int, str(number)))
    while len(str(total)) > 1:
        total = sum(map(int, str(total)))
    yield total


def _calculate_reverse_digital_root(
    digital_root: int,
    *,
    min_length: int,
    max_length: int,
    without: Iterable[int]
) -> Iterator[tuple[int, ...]]:
    for i in range(min_length, max_length + 1):
        for comb in combinations(range(1, 10), i):
            comb_str = "".join(map(str, comb))

            if any((
                str(x) in comb_str
                for x in without
            )):
                continue

            if next(calculate_digital_root(int(comb_str))) == digital_root:
                yield comb


def calculate_reverse_digital_root(
    digital_roots: list[int],
    min_length: int,
    max_length: int,
    without: Optional[list[int]] = None,
) -> Iterator[tuple[int, ...] | dict[int, tuple[int, ...]]]:

    if not without:
        without = []

    if len(digital_roots) == 1:
        yield from _calculate_reverse_digital_root(
            digital_roots[0],
            min_length=min_length,
            max_length=max_length,
            without=without
        )
        return

    # complementary digital roots

    available_numbers: str = map_and_join(
        i
        for i in range(1, 10)
        if i not in without
    )
    if 2 * len(digital_roots) > len(available_numbers):
        raise ValueError(
            "Cannot calculate combinations for digital_roots that "
            "amount to more than half of the available_numbers"
        )

    calculate_compl_rev_digital_root = partial(
        _calculate_reverse_digital_root,
        min_length=2,
    )

    # The largest combination for the first digital_root is limited by the available
    # set and the requested digital_roots.
    # 
    # The minimum length of each combination is 2.
    # If the pool of numbers for the combinations is X and the user requested
    # N digital roots, the largest combination cannot be longer than
    # the available pool minus N-1 * minimum length --> X - 2 * (N - 1)
    #
    # eg:
    # X = 8, N = 3 --> 8 - 2 * (3 - 1) = 8 - 2 * 2 = 4 --> 12 34 5678
    # X = 9, N = 4 --> 9 - 2 * (4 - 1) = 9 - 2 * 3 = 3 --> 12 34 56 789
    max_length_first_combination = len(available_numbers) - 2 * (len(digital_roots) - 1)

    def recursive_search(
        index: int,
        current_without: list[int],
        current_combs: list[tuple[int, ...]]
    ) -> Iterator[dict[int, tuple[int, ...]]]:
        # Base case: we have a combination for each digital root.
        if index == len(digital_roots):
            # Flatten the current combinations and check against available_numbers
            combined = tuple(chain.from_iterable(current_combs))
            if map_and_join(sorted(combined)) == available_numbers:
                yield {digital_roots[i]: current_combs[i] for i in range(len(digital_roots))}
            return

        # For the first digital root, use the precomputed max_length_first_combination;
        # for later ones, adjust based on the number of numbers already used.
        if index == 0:
            max_length_value = max(2, max_length_first_combination)
        else:
            used_length = sum(len(comb) for comb in current_combs)
            max_length_value = max(2, len(available_numbers) - used_length)

        # Generate valid combinations for the current digital root
        for comb in calculate_compl_rev_digital_root(
            digital_roots[index],
            without=current_without,
            max_length=max_length_value,
        ):
            new_without = list(set(current_without) | set(comb))
            yield from recursive_search(index + 1, new_without, current_combs + [comb])

    yield from recursive_search(0, without, [])


def cli_entrypoint():
    parser = argparse.ArgumentParser(
        "nonary",
        description="CLI tool for the 'Zero Escape: The Nonary Games' game",
    )
    subparser = parser.add_subparsers()

    fake_hex = subparser.add_parser(
        "fake_hex",
        help=(
            "Regular Hexadecimal stops at F(15). "
            "Fake Hexadecimal continues forever --> G - 16, H - 17, I - 18.\n"
            "You can think of this as a simple encoding for the Alphabet where A starts at 10."
        )
    )
    fake_hex.set_defaults(fn=calculate_fake_hex)
    fake_hex.add_argument(
        "word",
        help="The word to convert into fake hexadecimal"
    )

    digital_root = subparser.add_parser(
        "digital_root",
        help="Calculates the digital root for a given number"
    )
    digital_root.set_defaults(fn=calculate_digital_root)
    digital_root.add_argument(
        "number",
        type=int,
        help="The number to calculate the digital root for"
    )

    reverse_digital_root = subparser.add_parser(
        "reverse_digital_root",
        help="Generates all the possible combinations of numbers that reach a given digital root"
    )
    reverse_digital_root.set_defaults(fn=calculate_reverse_digital_root)
    reverse_digital_root.add_argument(
        "digital_roots",
        nargs="*",
        type=int,
        help="List of digital roots the combinations need to reach"
    )
    reverse_digital_root.add_argument(
        "-x", "--without", 
        nargs="*",
        type=int,
        help="List of numbers to not use to calculate combinations",
    )
    reverse_digital_root.add_argument(
        "-l", "--min-length",
        default=2,
        type=int,
        help=(
            "The smallest length a combination can have. "
            "If digital_roots length is > 1, this param will be ignored."
        ),
    )
    reverse_digital_root.add_argument(
        "-L", "--max-length",
        default=9,
        type=int,
        help=(
            "The biggest length a combination can have. "
            "If digital_roots length is > 1, this param will be ignored."
        ),
    )

    args = vars(parser.parse_args())
    fn: Optional[Callable[[], Iterator]] = args.pop("fn", None)

    if not fn:
        parser.print_help()
        exit(0)
    
    try:
        for res in fn(**args):
            print(res)
    except Exception as e:
        print(e)
        exit(-1)
