
import pandas as pd
import json
import requests
import time
import re

class DataPlug:
    """
    DataPlug class. Used for data aquisition from reddit.

    :Attributes:
    * :name: name of the user agent
    * :reddit_raw_data: raw data from reddit
    * :df: pandas dataframe
    * :user_agent: user agent for reddit
    * :client_id: client id for reddit
    * :client_secret: client secret for reddit
    * :priceDF: price dataframe of GME stock price
    * :mergedDF: merged dataframe of reddit and price data
    """

# get data from reddit for a subreddit filtering by date using the pushshift api
    def get_data_pushshift(self, subreddit, limit, before, after):
        """Get data from reddit.

        :param subreddit: subreddit to get data from
        :param limit: number of posts to get
        :param before: time to get posts before
        :param after: time to get posts after

        :return: data from reddit
        :rtype: dict
        """
        url = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&size={limit}&before={before}&after={after}&aggs=author"
        r = requests.get(url)
        data = r.json()['data']
        return data

    # A function to convert epoch time to a readable date
    def get_date(self, epoch_time):
        """Convert epoch time to a readable date.

        :param epoch_time: time to convert

        :return: date: readable date
        :rtype: str
        """
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))
        return date

    # A function to convert readable date to epoch time
    def get_epoch(self, date):
        """Convert readable date to epoch time.

        :param date: date string to convert

        :return: epoch_time: epoch time
        :rtype: float
        """
        epoch_time = time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S'))
        return epoch_time

    def get_data(self, subreddit, limit):
        """Get data from reddit.

        :param subreddit: subreddit to get data from
        :param limit: number of posts to get

        :return: data: data from reddit
        :rtype: dict
        """

        pass
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

        :param data: data to convert

        :return: pandas dataframe
        :rtype: pandas dataframe
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

    def merge_dataframes(self):
        """Merge the price and reddit dataframes.

        :return: pandas dataframe
        :rtype: pandas dataframe
        """
        merged_df = self.priceDF.merge(self.df, how='inner', on=['timestamp'])


        self.mergedDF = merged_df
        return self.mergedDF

    def aggregate_reddit_posts_daily(self):

        """Aggregate reddit posts by date. Turns dataframe for each reddit post into one dataframe with average results across all posts for each day.


        :return: pandas dataframe of aggregated reddit posts
        :rtype: pandas dataframe
        """
        agg_func = {'title': list, 'score': 'mean', 'id': list, 'url': list, 'comms_num': 'mean', 'created': 'first', 'body': list}

        # Replace NaN values with 'NaN'
        self.df['body'] = self.df['body'].fillna('NaN')
        # Group by date and aggregate
        df_new = self.df.groupby(self.df['timestamp']).aggregate(agg_func)
        # Join lists of titles, ids, urls, and bodies into one string per date to perform sentiment analysis.
        df_new['title'] = df_new['title'].apply(lambda x: '||'.join(x))
        df_new['id'] = df_new['id'].apply(lambda x: '||'.join(x))
        df_new['url'] = df_new['url'].apply(lambda x: '||'.join(x))
        df_new['body'] = df_new['body'].apply(lambda x: '||'.join(x))

        self.df = df_new

        return self.df

    def new_aggregate_reddit_posts_daily(self):

        """Aggregate reddit posts by date. Returns dataframe for each reddit post into one dataframe with average results across all posts for each day.

        :return: Aggregated reddit posts daily
        :rtype: pandas dataframe
        """
        agg_func = {'title': list, 'score': 'mean', 'id': list, 'url': list, 'comms_num': 'mean', 'created': 'first', 'body': list}

        # Replace NaN values with 'NaN'
        self.df['body'] = self.df['body'].fillna('NaN')
        # Group by date and aggregate
        df_new = self.df.groupby(self.df['timestamp']).aggregate(agg_func)
        # Join lists of titles, ids, urls, and bodies into one string per date to perform sentiment analysis.
        df_new['title'] = df_new['title'].apply(lambda x: '||'.join(x))
        df_new['id'] = df_new['id'].apply(lambda x: '||'.join(x))
        df_new['url'] = df_new['url'].apply(lambda x: '||'.join(x))
        df_new['body'] = df_new['body'].apply(lambda x: '||'.join(x))

        self.df = df_new

        return self.df

    def get_reddit_dataframe(self, filename='./../data/reddit_wsb.csv'):
        """A funciton to get dataframe of price data from csv

        :param filename: name of CSV file; defaults to './../data/reddit_wsb.csv'
        :return: pandas dataframe of reddit data. Saved to *self.df* attribute.
        :rtype: pandas dataframe
        """
        self.df = pd.read_csv(filename)

        # Floor the datetime for each post to be only yyyy-mm-dd so it lines up with the price data.
        self.df['timestamp'] = self.df['timestamp'].astype('datetime64[ns]').dt.floor('D')

        return self.df

    def get_price_dataframe(self, filename='./../data/GME.csv'):
        """A funciton to get dataframe of price data from csv.

        :param filename: name of CSV file; defaults to './../data/GME.csv'
        :return: pandas dataframe of price data. Saved to *self.priceDF* attribute.
        :rtype: pandas dataframe
        """
        self.priceDF = pd.read_csv(filename)
        # Rename 'Date' column to 'timestamp' to match the price dataframe for merging
        self.priceDF.rename(columns={'Date':'timestamp'}, inplace=True)
        # Set date objects to be the same type as the reddit dataframe for merging
        self.priceDF['timestamp'] = self.priceDF['timestamp'].astype('datetime64[ns]').dt.floor('D')
        return self.priceDF

    def __init__(self, name):
        """Initialize DataPlug class and load config

        :param name: name of the network. Saved to *self.name* attribute.
        :return: None
        :rtype: None
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

        # Declare attributes
        self.priceDF = None
        self.df = None
        self.mergedDF = None
        self.reddit_raw_data = None

#%%
