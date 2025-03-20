import unittest
from asro_nlp import AsroNLP

class TestAsroNLP(unittest.TestCase):

    def setUp(self):
        """Setup untuk setiap metode pengujian."""
        self.nlp = AsroNLP()

    def test_tokenize_text(self):
        """Tes fungsi tokenize_text."""
        text = "Ini adalah hari yang indah."
        tokens = self.nlp.tokenize_text(text)
        expected_tokens = ['ini', 'adalah', 'hari', 'yang', 'indah']
        self.assertEqual(tokens, expected_tokens)

    def test_remove_stopwords(self):
        """Tes fungsi remove_stopwords."""
        tokens = ['ini', 'adalah', 'hari', 'yang', 'sangat', 'indah']
        filtered_tokens = self.nlp.remove_stopwords(tokens)
        # Asumsikan 'adalah' dan 'yang' adalah stopwords
        expected_tokens = ['ini', 'hari', 'sangat', 'indah']
        self.assertEqual(filtered_tokens, expected_tokens)

    def test_sentiment_analysis(self):
        """Tes fungsi sentiment_analysis."""
        tokens = ['bahagia', 'menyenangkan', 'sedih']
        result = self.nlp.sentiment_analysis(tokens)
        self.assertIsNotNone(result)
        self.assertIn('Sentiment', result)

    def test_process_dataframe(self):
        """Tes fungsi process_dataframe dengan data fiktif."""
        import pandas as pd
        from io import StringIO

        data = StringIO("""
        full_text
        "Saya suka hari ini"
        "Saya benci hujan"
        """)
        df = pd.read_csv(data, sep=";")
        processed_df = self.nlp.process_dataframe(df)
        self.assertIsNotNone(processed_df)
        self.assertIn('Sentiment', processed_df.columns)

if __name__ == '__main__':
    unittest.main()
