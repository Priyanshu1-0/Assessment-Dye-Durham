import unittest
from collections import Counter

from name_sorter.ordering import by_last_name_then_given_names
from name_sorter.sorter import NameSorter
from tests.helpers import EXAMPLE_SORTED, EXAMPLE_UNSORTED, as_strings, parse_all


class NameSorterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sorter = NameSorter(by_last_name_then_given_names)

    def test_sorts_the_example_from_the_assessment_into_the_expected_order(self) -> None:
        sorted_names = self.sorter.sort(parse_all(EXAMPLE_UNSORTED))

        self.assertEqual(as_strings(sorted_names), EXAMPLE_SORTED)

    def test_leaves_the_input_untouched(self) -> None:
        unsorted = parse_all(["Zoe Young", "Adam Abbott"])
        snapshot = list(unsorted)

        self.sorter.sort(unsorted)

        self.assertEqual(unsorted, snapshot)

    def test_returns_an_empty_list_for_an_empty_list(self) -> None:
        self.assertEqual(self.sorter.sort([]), [])

    def test_keeps_equivalent_names_in_their_original_order(self) -> None:
        unsorted = parse_all(["adam smith", "Adam Smith", "ADAM SMITH"])

        sorted_names = self.sorter.sort(unsorted)

        self.assertEqual(as_strings(sorted_names), ["adam smith", "Adam Smith", "ADAM SMITH"])

    def test_defers_entirely_to_the_key_it_is_given(self) -> None:
        by_last_name_length_descending = lambda name: -len(name.last_name)  # noqa: E731
        unsorted = parse_all(["A Li", "B Anderson", "C Smith"])

        sorted_names = NameSorter(by_last_name_length_descending).sort(unsorted)

        self.assertEqual(as_strings(sorted_names), ["B Anderson", "C Smith", "A Li"])


class NameSorterAtScaleTests(unittest.TestCase):
    """The assessment is run against a thousand names; so are we.

    With a generated list there is no hand-written expected output, so these
    tests check the *properties* a correct sort must have instead.
    """

    def setUp(self) -> None:
        lines = [f"Given{i} Last{i % 20}" for i in range(1000)]
        lines[0] = "Ada smith"
        lines[1] = "Zoe Smith"
        self.unsorted = parse_all(lines)
        self.sorted = NameSorter(by_last_name_then_given_names).sort(self.unsorted)

    def test_output_is_a_permutation_of_the_input(self) -> None:
        self.assertEqual(len(self.sorted), 1000)
        self.assertEqual(Counter(self.sorted), Counter(self.unsorted))

    def test_last_names_never_go_backwards(self) -> None:
        last_names = [name.last_name.casefold() for name in self.sorted]

        self.assertEqual(last_names, sorted(last_names))

    def test_within_a_last_name_given_names_never_go_backwards(self) -> None:
        for earlier, later in zip(self.sorted, self.sorted[1:]):
            if earlier.last_name.casefold() != later.last_name.casefold():
                continue
            with self.subTest(earlier=str(earlier), later=str(later)):
                self.assertLessEqual(
                    [g.casefold() for g in earlier.given_names],
                    [g.casefold() for g in later.given_names],
                )

    def test_tricky_last_names_are_grouped_regardless_of_case(self) -> None:
        # "Smith" and "smith" must end up as one contiguous block.
        positions = [i for i, name in enumerate(self.sorted) if name.last_name.casefold() == "smith"]

        self.assertTrue(positions, "expected some Smiths in the generated data")
        self.assertEqual(positions, list(range(positions[0], positions[-1] + 1)))
