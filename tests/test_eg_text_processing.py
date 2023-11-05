import unittest
from experience_generator.utils import format_text

class TestFormatText(unittest.TestCase):

    def test_standardize_apostrophes(self):
        self.assertEqual(format_text("I'm"), "I’m")

    def test_remove_spaces_before_punctuation(self):
        test_cases = [
            ("Hello , world .", "Hello, world."),
            ("What ?", "What?"),
            ("Hey !", "Hey!"),
            ("It ’s", "It’s"),
            ("A ; B", "A; b"),
            ("Time :", "Time:")
        ]
        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(format_text(input_text), expected_output)

    def test_fix_dashes(self):
        self.assertEqual(format_text("A - B"), "A-b")

    def test_handle_contractions(self):
        test_cases = [
            ("you ’re", "You’re"),
            ("do n’t", "Don’t"),
            ("I ’m", "I’m"),
            ("they ’ll", "They’ll")
        ]
        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(format_text(input_text), expected_output)

    def test_capitalize_sentences(self):
        test_cases = [
            ("hello. world. how are you?", "Hello. World. How are you?"),
            ("hey! it’s me.", "Hey! It’s me.")
        ]
        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(format_text(input_text), expected_output)

    def test_capitalize_standalone_i(self):
        self.assertEqual(format_text("you and i."), "You and I.")

    def test_capitalize_ai(self):
        test_cases = [
            ("ai is great.", "AI is great."),
            ("The ai revolution.", "The AI revolution.")
        ]
        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(format_text(input_text), expected_output)

if __name__ == "__main__":
    unittest.main()

