import unittest
from experience_generator.utils import format_text  # Replace 'your_module' with the actual module name

class TestFormatText(unittest.TestCase):

    def test_basic_contractions(self):
        self.assertEqual(format_text("I 'm happy"), "I’m happy")
        self.assertEqual(format_text("You 're right"), "You’re right")
        self.assertEqual(format_text("He 's coming"), "He’s coming")
        self.assertEqual(format_text("She 's gone"), "She’s gone")
        self.assertEqual(format_text("It 's raining"), "It’s raining")
        self.assertEqual(format_text("We 're late"), "We’re late")
        self.assertEqual(format_text("They 're here"), "They’re here")

    def test_other_contractions(self):
        self.assertEqual(format_text("I 'll go"), "I’ll go")
        self.assertEqual(format_text("You 'll see"), "You’ll see")
        self.assertEqual(format_text("He 'll run"), "He’ll run")
        self.assertEqual(format_text("She 'll dance"), "She’ll dance")
        self.assertEqual(format_text("We 'll win"), "We’ll win")
        self.assertEqual(format_text("They 'll lose"), "They’ll lose")

        self.assertEqual(format_text("I 've seen"), "I’ve seen")
        self.assertEqual(format_text("You 've been"), "You’ve been")
        self.assertEqual(format_text("We 've done"), "We’ve done")
        self.assertEqual(format_text("They 've left"), "They’ve left")

        self.assertEqual(format_text("I 'd like"), "I’d like")
        self.assertEqual(format_text("You 'd prefer"), "You’d prefer")
        self.assertEqual(format_text("He 'd love"), "He’d love")
        self.assertEqual(format_text("She 'd hate"), "She’d hate")
        self.assertEqual(format_text("We 'd enjoy"), "We’d enjoy")
        self.assertEqual(format_text("They 'd despise"), "They’d despise")

    def test_negative_contractions(self):
        self.assertEqual(format_text("Isn 't it?"), "Isn’t it?")
        self.assertEqual(format_text("Aren 't they?"), "Aren’t they?")
        self.assertEqual(format_text("Wasn 't he?"), "Wasn’t he?")
        self.assertEqual(format_text("Weren 't we?"), "Weren’t we?")
        self.assertEqual(format_text("Haven 't you?"), "Haven’t you?")
        self.assertEqual(format_text("Hasn 't she?"), "Hasn’t she?")
        self.assertEqual(format_text("Hadn 't they?"), "Hadn’t they?")
        self.assertEqual(format_text("Won 't I?"), "Won’t I?")
        self.assertEqual(format_text("Wouldn 't you?"), "Wouldn’t you?")
        self.assertEqual(format_text("Don 't do it"), "Don’t do it")
        self.assertEqual(format_text("Doesn 't he?"), "Doesn’t he?")
        self.assertEqual(format_text("Didn 't they?"), "Didn’t they?")
        self.assertEqual(format_text("Can 't I?"), "Can’t I?")
        self.assertEqual(format_text("Couldn 't you?"), "Couldn’t you?")
        self.assertEqual(format_text("Shouldn 't we?"), "Shouldn’t we?")
        self.assertEqual(format_text("Mightn 't they?"), "Mightn’t they?")
        self.assertEqual(format_text("Mustn 't she?"), "Mustn’t she?")

    def test_mixed_sentence(self):
        self.assertEqual(format_text("I 'm happy and you 're right. He 's coming, isn 't he?"), "I’m happy and you’re right. He’s coming, isn’t he?")

if __name__ == "__main__":
    unittest.main()

