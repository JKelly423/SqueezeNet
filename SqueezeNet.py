from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# Kieran test
class SqueezeNet:
    """The main SqeezeNet class that uses all the modules in order to perform it's task"""

    # A function to perform sentiment analysis on the dataframe with a given paramaters
    def sentiment_analysis(self, text):
        """A function to perform sentiment analysis with vaderSentiment

        :params: text: text to perform sentiment analysis on

        :returns: score: the sentiment score
        """

        #Create an instance of the sentiment analyzer
        analyzer = SentimentIntensityAnalyzer()

        # Get the sentiment score
        score = analyzer.polarity_scores(text)

        # Return the sentiment score
        return score



    def __init__(self, name):
        """The constructor of the SqueezeNet class"""

        self.name = name