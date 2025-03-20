import pandas as pd
import re
import os

def normalize_media_name(name):
    """Normalize media names by removing spaces and special characters except '.', and converting to lowercase."""
    name = re.sub(r"[^\w\d\s.]", '', name)
    name = re.sub(r"\s+", '', name)
    return name.lower()

class AsroNLP:
    def __init__(self, base_path=None):
        """Initialize paths for data files and Leksionari Indonesia."""
        if base_path is None:
            base_path = os.path.dirname(os.path.abspath(__file__))

        self.stopwords_path = os.path.join(base_path, "data/stopwords.txt")
        self.normalization_path = os.path.join(base_path, "data/kamuskatabaku.xlsx")
        self.news_dictionary_path = os.path.join(base_path, "data/news_dictionary.txt")
        self.root_words_path = os.path.join(base_path, "data/kata-dasar.txt")
        self.leksionari_positive_path = os.path.join(base_path, "data/kamus_positive.xlsx")
        self.leksionari_negative_path = os.path.join(base_path, "data/kamus_negative.xlsx")

        self.load_resources()

    def load_resources(self):
        """Load necessary resources from files."""
        self.ensure_files_exist([
            self.stopwords_path,
            self.normalization_path,
            self.news_dictionary_path,
            self.root_words_path,
            self.leksionari_positive_path,
            self.leksionari_negative_path
        ])

        with open(self.stopwords_path, "r", encoding="utf-8") as f:
            self.stopwords = set(f.read().splitlines())

        self.normalization_dict = pd.read_excel(self.normalization_path, header=None, engine='openpyxl').set_index(0)[1].to_dict()
        self.leksionari_positive = pd.read_excel(self.leksionari_positive_path, engine='openpyxl').set_index(0)[1].to_dict()
        self.leksionari_negative = pd.read_excel(self.leksionari_negative_path, engine='openpyxl').set_index(0)[1].to_dict()

    def ensure_files_exist(self, files):
        """Check if all required files exist."""
        missing_files = [file for file in files if not os.path.exists(file)]
        if missing_files:
            raise FileNotFoundError(f"Required file(s) not found: {', '.join(missing_files)}")

    @staticmethod
    def clean_text(text):
        """Clean text by removing undesirable characters and numbers."""
        return re.sub(r"([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)|\d+|[^\w\s]|_", " ", text).strip()

    def tokenize_text(self, text):
        """Tokenize text using simple regex."""
        return re.findall(r'\b\w+\b', text.lower())

    def remove_stopwords(self, tokens):
        """Remove stopwords from a list of tokens."""
        return [token for token in tokens if token not in self.stopwords and token.isalpha()]

    def normalize_text(self, tokens):
        """Normalize tokens using a predefined dictionary."""
        return [self.normalization_dict.get(token, token) for token in tokens]

    def sentiment_analysis(self, tokens):
        """Perform sentiment analysis using predefined Leksionari Indonesia."""
        score = 0
        for word in tokens:
            score += self.leksionari_positive.get(word, 0)
            score -= self.leksionari_negative.get(word, 0)
        return 'Positive' if score > 0 else 'Negative' if score < 0 else 'Neutral'

    def preprocess_and_analyze(self, input_path, output_path="output.xlsx"):
        """Process text data and perform sentiment analysis."""
        try:
            df = pd.read_excel(input_path, engine='openpyxl')
            df["Cleaned_Text"] = df["Text"].apply(self.clean_text)
            df["Tokens"] = df["Cleaned_Text"].apply(self.tokenize_text)
            df["Filtered_Text"] = df["Tokens"].apply(self.remove_stopwords)
            df["Normalized_Text"] = df["Filtered_Text"].apply(self.normalize_text)
            df["Sentiment"] = df["Normalized_Text"].apply(self.sentiment_analysis)

            output_filename = output_path.replace('.xlsx', '_sentiment.xlsx')
            df.to_excel(output_filename, index=False, engine='openpyxl')
            print(f"Processed data saved to {output_filename}")
        except Exception as e:
            print(f"Failed to process data: {e}")
            return None

        return df

if __name__ == "__main__":
    # Example usage can be added here for direct execution
    pass
