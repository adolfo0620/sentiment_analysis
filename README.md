#Sentiment Analysis

View graphs depicting the positivity or negativity of words, phrases, and/or hashtag being talked about on twitter, tumblr, or reddit.  Or run your Gmail account through our sentiment analysis.  Or any block of text you'd like to measure the sentiment of! 

See live (here)[http://sa.718it.biz/]

## Setup

`git clone https://github.com/himleyb85/sentiment_analysis`

`cd sentiment_analysis`

`virutalenv venv`

`source venv/bin/activate`

`pip3 install -r requirements.txt`

`createdb twitters`

`sudo su postgres`

You should now be at the postgres user bash prompt

`psql`

You should now be in the psql prompt -> postgres=#

`CREATE ROLE bears WITH login password 'bears';`

`ALTER ROLE bears WITH superuser createdb createrole;`

`\q`

`exit`

To put the negative and positive words into the redis db, start the redis server

`redis-server`

then

`cd project/project`

then 

`python3 pos_neg_redis.py`

Put the app secret key and the databases information in a file named "local_settings" in your settings folder

Finally, you need to get the app key and app secret and store them in a file you must create in the twit app.  The file must be named keysecret.py, and the contents of the file must be thus:

`secrets = {'APP_KEY':"<app key here>","APP_SECRET":"<app key secret here>"}`

Should be good to go.  To start server,

`python3 manage.py runserver`

then direct your browser to http://127.0.0.1:8000
