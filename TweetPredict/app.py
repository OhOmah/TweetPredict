# Main app/routig file for TwitOff!

# import flask
from os import getenv
from flask import Flask, render_template, request
from .models import db, User
from .predict import predict_user
from .twitter import add_or_update_user, update_all_users

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/')
    def root():
        # Rendering template that we created passing home to template 
        return render_template('base.html', title='Home',
                                users=User.query.all())

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} Successfully added!'.format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {} in {}".format(name, e)
            tweets=[]
        return render_template('user.html', title=name, tweets=tweets,
                                message=message)
    
    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'],
                            request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a use to themselves!'
        else:
            prediction = predict_user(user1, user2,
                                    request.values['tweet_text'])
            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user1
            )
        return render_template('prediction.html', title='Prediction',
                                message=message)
    
    @app.route('/reset')
    def reset():
        db.drop_all() # Reset the data base
        db.create_all()
        return render_template('base.html', title = 'Reset Database')

    @app.route('/update')
    def view_users():
        update_all_users()
        return render_template('base.html', users=User.query.all(), 
                                title = 'Database Updated')
    
    return app