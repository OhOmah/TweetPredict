''' SQLAlchemy'''
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    '''Twitter Users'''
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    # Tweet IDs are odrdinal ints, so can be used to fetch only more recent
    newest_tweet_id = db.Column(db.BigInteger)
    
    def __repr__(self):
        return '[User {}]'.format(self.name)

class Tweet(db.Model):
    ''' Tweets and their embeddings from basilica.'''
    id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.Unicode(300)) # Allows for full tweet + link
    embedding = db.Column(db.PickleType, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), 
                        nullable=False)
    user = db.relationship('User', backref=db.backref('tweets', 
    lazy=True))

    def __repr__(self):
        return '[Tweet {}]'.format(self.text)




    