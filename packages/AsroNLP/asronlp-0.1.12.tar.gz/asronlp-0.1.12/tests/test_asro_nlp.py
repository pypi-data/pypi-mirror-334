import unittest
from asro_nlp import AsroNLP

class TestAsroNLP(unittest.TestCase):
    def setUp(self):
        """Setup for each test"""
        self.nlp = AsroNLP()

    def test_instance_creation(self):
        """Test that an instance of AsroNLP can be created."""
        self.assertIsInstance(self.nlp, AsroNLP)

    def test_stopwords_loading(self):
        """Test that stopwords are loaded correctly."""
        stopwords = self.nlp.stopwords
        self.assertTrue(isinstance(stopwords, set))
        self.assertGreater(len(stopwords), 0)

    def test_sentiment_analysis(self):
        """Test basic functionality of sentiment analysis."""
        text = "This is a good day."
        tokens = self.nlp.tokenize_text(text)
        filtered_tokens = self.nlp.remove_stopwords(tokens)
        sentiment = self.nlp.sentiment_analysis(filtered_tokens)
        self.assertEqual(sentiment['Sentiment'], 'Positive')

    def test_missing_file_error(self):
        """Test that the correct exception is raised for a missing file."""
        with self.assertRaises(FileNotFoundError):
            self.nlp.load_excel_dict("path_that_does_not_exist.xlsx")

# Run the tests
if __name__ == '__main__':
    unittest.main()
