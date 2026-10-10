import unittest

from name_sorter.name import Name
from name_sorter.ordering import by_last_name_then_given_names


def key(text: str) -> tuple[str, tuple[str, ...]]:
    return by_last_name_then_given_names(Name.parse(text))


class ByLastNameThenGivenNamesTests(unittest.TestCase):
    def test_orders_by_last_name_before_anything_else(self) -> None:
        self.assertLess(key("Zoe Adams"), key("Aaron Brown"))

    def test_breaks_last_name_ties_using_the_first_given_name(self) -> None:
        self.assertLess(key("Adam Smith"), key("Zoe Smith"))

    def test_then_moves_on_to_the_second_and_third_given_names(self) -> None:
        self.assertLess(key("Adam Bob Smith"), key("Adam Carl Smith"))
        self.assertLess(key("Adam Bob Carl Smith"), key("Adam Bob Dave Smith"))

    def test_puts_a_name_with_fewer_given_names_first_when_the_shared_ones_match(self) -> None:
        self.assertLess(key("Leo Gardner"), key("Leo Alan Gardner"))

    def test_ignores_letter_case(self) -> None:
        self.assertEqual(key("adam smith"), key("Adam Smith"))
        self.assertLess(key("adam smith"), key("Adam Smyth"))

    def test_identical_names_have_identical_keys(self) -> None:
        self.assertEqual(key("Marin Alvarez"), key("Marin Alvarez"))
