from nltk.sentiment import SentimentIntensityAnalyzer

def main(text: str = "Wow, NLTK is really powerful!"):
    return SentimentIntensityAnalyzer().polarity_scores(text)
