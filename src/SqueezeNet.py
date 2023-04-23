import string
import nltk
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

# Kieran test
class SqueezeNet:
    """The main SqeezeNet class that uses all the modules in order to perform it's task"""

    #A function that removes words that are 1 character in length and user specified words
    def clean_text(self, text, custom_remove_words=None):
        """Given some text, return a list of clean words.

        :params: text: Text to clean up
        "params: custom_remove_words: A list of words to also remove

        :returns: filtered_text: Filters words that are 1-2 character in length and custom words
            """

        # Convert the custom remove words to lowercase
        if custom_remove_words is not None:
            custom_remove_words = [w.lower() for w in custom_remove_words]

        #Remove "||" and "NaN"
        text = text.replace("||", "")
        text = text.replace("NaN", "")

        # Remove words that are 1 or 2 characters in length
        words = text.split()
        words = [w for w in words if len(w) > 1]

        # Remove custom remove words
        if custom_remove_words is not None:
            words = [w for w in words if w.lower() not in custom_remove_words]
            # Remove words that are capitalized in the text but not in the original list
            words = [w for w in words if w.lower() not in [r.lower() for r in custom_remove_words] or w.islower()]

        # Join the words back into a single string
        cleaned_text = ' '.join(words)

        # Remove extra whitespace
        cleaned_text = re.sub('\s+', ' ', cleaned_text).strip()

        # Return the cleaned text
        return cleaned_text

    #A function to perform sentiment analysis on the dataframe with a given paramaters
    def sentiment_analysis(self, text):
        """A function to perform sentiment analysis with vaderSentiment

        :params: text: text to perform sentiment analysis on

        :returns: score: the sentiment score
        """
        custom_emoji_scores = {
            'rocket': 4.0,
            'gem stone': 4.0,
            'raising hands': 3.0,
            'bull': 3.5,
            'bear': -3.5,
            'toilet paper': -4,
            'fire': 3.0,
            'green': 2,
            'red': -2
        }
        #Create an instance of the sentiment analyzer
        analyzer = SentimentIntensityAnalyzer()

        # Update VADER's emoji sentiment scores with custom scores
        analyzer.lexicon.update(custom_emoji_scores)

        # Get the sentiment score
        score = analyzer.polarity_scores(text)

        # Return the sentiment score
        return score



    def __init__(self, name):
        """The constructor of the SqueezeNet class"""

        self.name = name
#%%
