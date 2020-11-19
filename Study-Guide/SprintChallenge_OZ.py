# Importing what I need 
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
import requests 
import openaq


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///help.sqlite3'
    # Initializing my db
    DB = SQLAlchemy()
    DB.init_app(app)
    

    #initializing my root page
    @app.route('/')
    def root():
        """Base view."""
        return query()

    class Record(DB.Model):
        ''' Creates the database ''' 
        datetime = DB.Column(DB.String(25))
        value = DB.Column(DB.Float, nullable=False)

        def __repr__(self):
            return '[Time {}]'.format(self.text)


        @app.route('/refresh')
        def refresh():
            """Pull fresh data from Open AQ and replace existing data."""
            DB.drop_all()
            DB.create_all()
            # TODO Get data from OpenAQ, make Record objects with it, and add to db
            # Using the query() function to get what I need -
            data = query()
            db_data = (Record.query.get(datetime) or 
                        Record(datetime=data['date'])
            # Adding the data into my
            DB.session.add(db_data)
            DB.session.commit()
            return 'Data refreshed!'



def query():
    '''goes into the API and grabs information needed'''
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    # Setting my i variable
    i=1
    lists = body['results'][0]['date']['utc'], body['results'][0]['value']
    for s in body: 
        li = {body['results'][i]['date']['utc'], body['results'][i]['value']}
        lists.update(li)
        i= i+1
        if i > 100:
            li

    return li

def condition():
    ''' This is going to just filter through my database running it with my flask shell'''
    Record.query.filter(value > 10).all()