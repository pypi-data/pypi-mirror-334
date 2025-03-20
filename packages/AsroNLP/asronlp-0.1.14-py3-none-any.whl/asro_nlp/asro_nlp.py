import os
import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from importlib import resources  # Menggunakan importlib.resources untuk akses sumber daya

class AsroNLP:
    def __init__(self):
        with resources.path('asro_nlp.data', 'stopwords.txt') as p:
            self.stopwords_path = str(p)
        self.initialize_paths()
        self.load_resources()

    def initialize_paths(self):
        base_dir = os.path.dirname(self.stopwords_path)
        self.normalization_path = os.path.join(base_dir, "kamuskatabaku.xlsx")
        self.news_dictionary_path = os.path.join(base_dir, "news_dictionary.txt")
        self.root_words_path = os.path.join(base_dir, "kata-dasar.txt")
        self.lexicon_positive_path = os.path.join(base_dir, "kamus_positive.xlsx")
        self.lexicon_negative_path = os.path.join(base_dir, "kamus_negative.xlsx")

    def load_resources(self):
        self.ensure_files_exist([
            self.stopwords_path,
            self.normalization_path,
            self.news_dictionary_path,
            self.root_words_path,
            self.lexicon_positive_path,
            self.lexicon_negative_path
        ])
        nltk.download('punkt', quiet=True)
        self.stopwords = self.load_stopwords()
        self.normalization_dict = self.load_excel_dict(self.normalization_path)
        self.lexicon_positive_dict = self.load_excel_dict(self.lexicon_positive_path)
        self.lexicon_negative_dict = self.load_excel_dict(self.lexicon_negative_path)
        self.news_media = self.load_news_media()

    def ensure_files_exist(self, files):
        missing_files = [file for file in files if not os.path.exists(file)]
        if missing_files:
            raise FileNotFoundError(f"Required file(s) not found: {', '.join(missing_files)}")

    def load_stopwords(self):
        with open(self.stopwords_path, "r", encoding="utf-8") as f:
            return set(f.read().splitlines())

    def load_excel_dict(self, path):
        df = pd.read_excel(path, header=None, engine='openpyxl')
        return dict(zip(df[0].str.lower(), df[1]))

    def load_news_media(self):
        with open(self.news_dictionary_path, "r", encoding="utf-8") as f:
            return set(self.normalize_media_name(line.strip()) for line in f.readlines())

    @staticmethod
    def normalize_media_name(name):
        name = re.sub(r"[^\w\d\s.]", '', name)
        name = re.sub(r"\s+", ' ', name)
        return name.lower()

    @staticmethod
    def clean_text(text):
        text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
        text = re.sub(r"\@\w+|\#", "", text)
        text = re.sub(r"\d+", "", text)
        text = re.sub(r"[^\w\s]", "", text)
        return text.strip()

    @staticmethod
    def tokenize_text(text):
        return word_tokenize(text.lower())

    def remove_stopwords(self, tokens):
        return [token for token in tokens if token not in self.stopwords and token.isalpha()]

    def normalize_text(self, tokens):
        return [self.normalization_dict.get(token, token) for token in tokens]

    def sentiment_analysis(self, tokens):
        score = 0
        positive_words = []
        negative_words = []
        for word in tokens:
            word = word.lower()
            if word in self.lexicon_positive_dict:
                score += self.lexicon_positive_dict[word]
                positive_words.append(word)
            if word in self.lexicon_negative_dict:
                score += self.lexicon_negative_dict[word]  # Adjust scoring for negatives
                negative_words.append(word)

        # Debug output to trace the computation
        print(f"Tokens: {tokens}")
        print(f"Score: {score}, Positive words: {positive_words}, Negative words: {negative_words}")

        # Determine sentiment based on adjusted scoring
        if score > 0:
            sentiment = 'Positive'
        elif score < 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'

        return {
            'Sentiment': sentiment,
            'Positive_Words': ', '.join(positive_words),
            'Negative_Words': ', '.join(negative_words)
        }


    def preprocess_and_analyze(self, input_path, output_path="output.xlsx"):
        try:
            df = pd.read_excel(input_path, engine='openpyxl')
            df = self.process_dataframe(df)
            df.to_excel(output_path, index=False, engine='openpyxl')
            print(f"Processed data saved to {output_path}")
        except Exception as e:
            print(f"Error processing data: {e}")

    def process_dataframe(self, df):
        if 'full_text' not in df.columns and 'comment' not in df.columns:
            raise ValueError("DataFrame does not contain a recognized text column ('full_text' or 'comment').")

        text_column = 'full_text' if 'full_text' in df.columns else 'comment'
        df['Cleaned_Text'] = df[text_column].apply(self.clean_text)
        df['Tokens'] = df['Cleaned_Text'].apply(self.tokenize_text)
        df['Filtered_Tokens'] = df['Tokens'].apply(self.remove_stopwords)
        df['Normalized_Text'] = df['Filtered_Tokens'].apply(self.normalize_text)
        df['Sentiment_Results'] = df['Normalized_Text'].apply(self.sentiment_analysis)
        df['Sentiment'] = df['Sentiment_Results'].apply(lambda x: x['Sentiment'])
        df['Positive_Words'] = df['Sentiment_Results'].apply(lambda x: x['Positive_Words'])
        df['Negative_Words'] = df['Sentiment_Results'].apply(lambda x: x['Negative_Words'])

        channel_title_column = 'channel_title' if 'channel_title' in df.columns else 'username' if 'username' in df.columns else None
        if channel_title_column is None:
            raise ValueError("DataFrame does not contain a recognized channel title column ('channel_title' or 'username').")
        df['Source_Type'] = df.apply(lambda x: self.detect_source_type(x[channel_title_column]), axis=1)

        df.drop('Sentiment_Results', axis=1, inplace=True)
        return df

    def detect_source_type(self, source_identifier):
        if not isinstance(source_identifier, str):
            return 'Individual'
        normalized_identifier = self.normalize_media_name(source_identifier)
        return 'Media' if any(media_name in normalized_identifier for media_name in self.news_media) else 'Individual'
