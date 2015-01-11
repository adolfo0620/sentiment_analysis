## Apps

1. Sentiment Analysis API

2. Twitter Mod

3. Basic text input Mod

4. Gmod

5. Users/UI


### Setup

`git clone https://github.com/himleyb85/sentiment_analysis`

`cd sentiment_analysis`

`virutalenv venv'

`pip3 install -r requirements.txt`

`createdb twitters'

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

`cd project/`

then 

`python3 pos_neg_redis.py`


Should be good to go.  To start server,

`python3 manage.py runserver'

then direct your browser to http://127.0.0.1:8000


### API
accepts block of text

Uses the lists of positive and negative words from [here](http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#lexicon)

### Twitter

more retweeted tweets should have more weight

be able to search by hashtag, account, or just words by themselves

will use D3 to display the setiment

to start, thinking pie chart for total sentiment, positive score, and negative score

line graph, charting change in sentiment over time if given date imputs (i.e., tweet dates)

chart ranking most used adjectives

scattered plot points of other popular hashtags associated 