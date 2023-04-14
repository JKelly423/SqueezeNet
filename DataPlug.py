import praw
import pandas as pd
import json
import requests
import time

class DataPlug:
    """
    DataPlug class. Used for data aquisition from reddit.

    :attributes: name: name of the user agent
    :attributes: reddit_raw_data: raw data from reddit
    :attributes: df: pandas dataframe
    :attributes: user_agent: user agent for reddit
    :attributes: client_id: client id for reddit
    :attributes: client_secret: client secret for reddit
    :attributes: priceDF: price dataframe of GME stock price
    """


    def get_data(self, subreddit, limit):
        """Get data from reddit.

        :params: subreddit: subreddit to get data from
        :params: limit: number of posts to get

        :returns: data: data from reddit
        """

        # Create instance of PRAW using the config file data now stored as attributes
        reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
        )

        self.reddit_raw_data = reddit.subreddit(subreddit).hot(limit=limit)
        return self.reddit_raw_data

    def data_to_pandas(self, data):
        """Convert data to pandas dataframe.

        :params: data: data to convert

        :returns: pandas dataframe
        """
        self.df = pd.DataFrame([x.__dict__ for x in data])
        return self.df

    def get_price_datafrane(self, filename='GME.csv'):
        """A funciton to get dataframe of price data from csv

        :params: filename: name of CSV file; defaults to 'GME.csv'
        :returns: pandas dataframe
        """
        self.priceDF = pd.read_csv(filename)
        return self.priceDF

    def __init__(self, name):
        """Initialize DataPlug class and load config

        :params: name: name of the user agent
        :returns: None
        """
        # Open and load config file into a config object
        try:
            cf = open('./configAPI.json', 'r')
            config = json.load(cf)
            cf.close()
        except FileNotFoundError:
            msg = "Sorry, the file ./config.json does not exist."
            print(msg)

        # Set the name of the net
        self.name = name
        # Set the data for the reddit instance
        self.user_agent = config['redditConfig']['user_agent']
        self.client_id = config['redditConfig']['client_id']
        self.client_secret = config['redditConfig']['client_secret']
