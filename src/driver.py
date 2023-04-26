import pandas as pd

from DataPlug import DataPlug as dp
from SqueezeNet import SqueezeNet as sq

squeeze = sq("SqueezeNet")
dataPlug = dp("DataPlug")

df = pd.read_csv('../data/r_wallstreetbets_posts.csv')
# convert utc time to datetime
df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
df['timestamp'] = df['created_utc'].astype('datetime64[ns]').dt.floor('D')

df.drop('author', inplace=True, axis=1)
df.drop('created_utc', inplace=True, axis=1)
df.drop('id', inplace=True, axis=1)
df.drop('author_flair_text', inplace=True, axis=1)
df.drop('removed_by', inplace=True, axis=1)
df.drop('awarders', inplace=True, axis=1)
df.drop('full_link', inplace=True, axis=1)
df.drop('over_18', inplace=True, axis=1)
df.drop('total_awards_received', inplace=True, axis=1)

df['title'] = df['title'].apply(lambda x: str(x))


agg_func = {'title': list, 'score': 'mean', 'num_comments': 'mean'}

# Replace NaN values with 'NaN'
#df['total_awards_received'] = df['total_awards_received'].fillna(0)
# Group by date and aggregate
df_new = df.groupby(df['timestamp']).aggregate(agg_func)

# Join lists of titles, ids, urls, and bodies into one string per date to perform sentiment analysis.

df_new['title'] = df_new['title'].apply(lambda x: '||'.join(x))

dataPlug.df = df_new

dataPlug.get_price_dataframe()

# Merge the dataframes
dataPlug.merge_dataframes()

# Sentiment analysis
positive = []
negative = []
neutral = []
compound = []

import time

begin = time.time() # timer for entire process

for i in range(0, len(dataPlug.mergedDF['title'])):
    start = time.time() # timer for each iteration

    if i == 2131:
        positive.append(0)
        negative.append(0)
        neutral.append(0)
        compound.append(0)
        continue

    text = dataPlug.mergedDF['title'][i]
    clean_text = squeeze.clean_text(text)
    score = squeeze.sentiment_analysis(clean_text)
    # Add scores to array
    positive.append(score['pos'])
    negative.append(score['neg'])
    neutral.append(score['neu'])
    compound.append(score['compound'])



    end = time.time() # end timer for each iteration

    print(f"Completed {i} of {len(dataPlug.mergedDF['title'])} posts | {end - start:0.4f} seconds | {end - begin:0.4f} seconds total")

print(f"Sentiment analysis took {end - begin:0.4f} seconds total")

# Using DataFrame.insert() to add the sentiment columns to the dataframe
dataPlug.mergedDF.insert(8, "Compound_Sentiment", compound, True)
dataPlug.mergedDF.insert(8, "Negative_Sentiment", negative, True)
dataPlug.mergedDF.insert(8, "Neutral_Sentiment", neutral, True)
dataPlug.mergedDF.insert(8, "Positive_Sentiment", positive, True)
print('Done!')

# Drop the column with the weird data issue
dataPlug.mergedDF = dataPlug.mergedDF.drop(labels=2131, axis=0)

# Save the dataframe to a csv file
dataPlug.mergedDF.to_csv('../data/mergedDF.csv')
print(f'saved to ../data/mergedDF.csv')