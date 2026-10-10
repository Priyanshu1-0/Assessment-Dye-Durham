import unittest

from name_sorter.name import InvalidNameError, Name


class NameParseTests(unittest.TestCase):
    def test_last_word_is_last_name_and_the_rest_are_given_names(self) -> None:
        name = Name.parse("Hunter Uriah Mathew Clarke")

        self.assertEqual(name.given_names, ("Hunter", "Uriah", "Mathew"))
        self.assertEqual(name.last_name, "Clarke")

    def test_accepts_a_single_given_name(self) -> None:
        name = Name.parse("Leo Gardner")

        self.assertEqual(name.given_names, ("Leo",))
        self.assertEqual(name.last_name, "Gardner")

    def test_ignores_surrounding_whitespace_and_collapses_repeated_spaces(self) -> None:
        name = Name.parse("   Janet \t  Parsons  ")

        self.assertEqual(name.given_names, ("Janet",))
        self.assertEqual(name.last_name, "Parsons")

    def test_rejects_a_blank_line(self) -> None:
        with self.assertRaises(InvalidNameError):
            Name.parse("   ")

    def test_rejects_a_name_with_no_given_names(self) -> None:
        with self.assertRaises(InvalidNameError):
            Name.parse("Clarke")

    def test_rejects_a_name_with_more_than_three_given_names(self) -> None:
        with self.assertRaises(InvalidNameError):
            Name.parse("One Two Three Four Clarke")

    def test_error_explains_what_went_wrong_and_quotes_the_input(self) -> None:
        with self.assertRaises(InvalidNameError) as raised:
            Name.parse("Clarke")

        self.assertIn('"Clarke"', str(raised.exception))
        self.assertIn("between 1 and 3 given names", str(raised.exception))


class NameTests(unittest.TestCase):
    def test_cannot_be_constructed_in_an_invalid_state(self) -> None:
        with self.assertRaises(InvalidNameError):
            Name(given_names=(), last_name="Clarke")

    def test_is_immutable(self) -> None:
        name = Name.parse("Leo Gardner")

        with self.assertRaises(AttributeError):
            name.last_name = "Changed"  # type: ignore[misc]

    def test_str_joins_the_parts_with_single_spaces(self) -> None:
        self.assertEqual(str(Name.parse("  Adonis   Julius Archer ")), "Adonis Julius Archer")

    def test_equal_names_are_equal(self) -> None:
        self.assertEqual(Name.parse("Leo Gardner"), Name.parse("Leo Gardner"))
