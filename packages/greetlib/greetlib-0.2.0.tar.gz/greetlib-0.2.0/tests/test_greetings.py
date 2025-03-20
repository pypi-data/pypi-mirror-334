# tests/test_greetings.py

import unittest
from greetlib.greetings import greet

class TestGreet(unittest.TestCase):

    def test_greet_english(self):
        self.assertEqual(greet("Alice"), "Hello, Alice!")

    def test_greet_spanish(self):
        self.assertEqual(greet("Alice", "es"), "Hola, Alice!")

    def test_greet_french(self):
        self.assertEqual(greet("Alice", "fr"), "Bonjour, Alice!")

    def test_greet_german(self):
        self.assertEqual(greet("Alice", "de"), "Hallo, Alice!")
        
    def test_greet_italian(self):  # New test case
        self.assertEqual(greet("Alice", "it"), "Ciao, Alice!")

    def test_greet_default_language(self):
        self.assertEqual(greet("Alice", "unknown"), "Hello, Alice!")

if __name__ == '__main__':
    unittest.main()
