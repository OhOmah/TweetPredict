''' Stores all the logic that will be used to grab data from twitter''' 
import tweepy, basilica
from .models import db, Tweet, User

TWITTER_USERS = ['calebhicks', 'elonmusk', 'rrherr', 'SteveMartinToGo', 
                'alyankovic', 'nasa', 'sadserver', 'jkhowland', 'austen', 
                'common_squirrel','KenJennings', 'conanobrien']
# TODO don't check this in! Use environmnet variables
TWITTER_AUTH = tweepy.OAuthHandler(
    'kiWdOYld4U0LJuyCmufzBrMSc', # API Key
    'QtRnIMA78bEYKF5g3N1DrULf6jUekxWo1nKjfO0XbX5RZi8knG' #secret key
)

TWITTER = tweepy.API(TWITTER_AUTH)
BASILICA = basilica.Connection('44877c0c-8083-3988-133a-b0062767dc96')

def add_or_update_user(username):
    '''Add or update a use and their tweets, etc, error if user doesn't exist.'''
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id) or
                    User(id=twitter_user.id, name=username))
        db.session.add(db_user)
        # We want as many recent non-retweet/reply statuses as we can get
        # 200 is a twitter api limit we'll usually see less due to exclusions
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False,
            tweet_mode='extended', since_id=db_user.newest_tweet_id)
        
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            embedding = BASILICA.embed_sentence(tweet.full_text,
                                                model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300],
                            embedding=embedding)
            db_user.tweets.append(db_tweet)
            db.session.add(db_tweet)
    except Exception as e:
        print('Error processing {} in {}'.format(username, e))
        raise e
    else:
        db.session.commit()

def add_users(users=TWITTER_USERS):
    '''Add/update a list of users.'''
    for user in users:
        add_or_update_user(user)

def update_all_users():
    '''Updates all existing users'''
    for user in User.query.all():
        add_or_update_user(user.name)