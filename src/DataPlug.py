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

# get data from reddit for a subreddit filtering by date using the pushshift api
    def get_data_pushshift(self, subreddit, limit, before, after):
        """Get data from reddit.

        :params: subreddit: subreddit to get data from
        :params: limit: number of posts to get
        :params: before: time to get posts before
        :params: after: time to get posts after

        :returns: data: data from reddit
        """
        url = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&size={limit}&before={before}&after={after}&aggs=author"
        r = requests.get(url)
        data = r.json()['data']
        return data

    # A function to convert epoch time to a readable date
    def get_date(self, epoch_time):
        """Convert epoch time to a readable date.

        :params: epoch_time: time to convert

        :returns: date: readable date string
        """
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))
        return date

    # A function to convert readable date to epoch time
    def get_epoch(self, date):
        """Convert readable date to epoch time.

        :params: date: date string to convert

        :returns: epoch_time: epoch time
        """
        epoch_time = time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S'))
        return epoch_time

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
        """Convert reddit data to pandas dataframe.

        :params: data: data to convert

        :returns: pandas dataframe
        """
        reddit_posts = []

        for item in range(0,len(data)):
            obj = json.dumps(data[item], indent=4)
            obj = json.loads(obj)
            post = {
                'title': obj["title"],
                'author': obj['author'],
                'score': obj['score'],
                'body': obj['selftext'],
                'gilded': obj['gilded'],
                'num_comments': obj['num_comments'],
                'num_crossposts': obj['num_crossposts'],
                'pinned': obj['pinned'],
                'stickied': obj['stickied'],
                'archived': obj['archived'],
                'is_video': obj['is_video'],
                'id': obj['id'],
                'permalink': obj['permalink'],
                'created_utc': obj['created_utc']
            }
            reddit_posts.append(post)

        self.df = pd.DataFrame(reddit_posts)
        return self.df

    def get_price_datafrane(self, filename='./../data/GME.csv'):
        """A funciton to get dataframe of price data from csv

        :params: filename: name of CSV file; defaults to './../data/GME.csv'
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
