import praw
import pandas as pd

class DataPlug:
    """DataPlug class. Used for data aquisition from reddit.

    :attributes: name: name of the user agent
    :attributes: reddit_raw_data: raw data from reddit
    :attributes: df: pandas dataframe
    """

    def get_data(self, subreddit, limit):
        """Get data from reddit.

        :params: subreddit: subreddit to get data from
        :params: limit: number of posts to get

        :returns: data: data from reddit
        """
        self.reddit_raw_data = praw.Reddit(user_agent=self.name).get_subreddit(subreddit).get_hot(limit=limit)
        return self.reddit_raw_data

    def data_to_pandas(self, data):
        """Convert data to pandas dataframe.

        :params: data: data to convert

        :returns: pandas dataframe
        """
        self.df = pd.DataFrame([x.__dict__ for x in data])
        return self.df

    def __init__(self, name):
        """Initialize DataPlug class.

        :params: name: name of the user agent
        :returns: None
        """
        self.name = name