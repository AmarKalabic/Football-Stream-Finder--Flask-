from flask import Flask, request

app = Flask(__name__)
#app.debug = True
from flask import render_template

import urllib2

import praw
import re
import sys
import webbrowser

user_agent = ("Link Getter")
r = praw.Reddit(user_agent=user_agent)


def login():
    r.login('', '', disable_warning=True)
    #Enter REDDIT USERNAME AND REDDIT PASSWORD
    # NEEDED TO SEARCH FOR ALL THE LINKS


@app.route("/", methods=('GET', 'POST'))
def hello_world():
    global match_name
    global lista_title
    global lista_url
    global lista_streamlinks
    if request.method == 'POST':
        match_name = request.form['match_name']
        print "Submit clicked!"
    elif request.method == 'GET':
        match_name = ""
        print "Normal load!"

    lista_title = []
    lista_url = []
    lista_streamlinks = []

    subreddit = r.get_subreddit("soccerstreams")

    for submission in subreddit.get_hot(limit=12):
        if re.search(match_name, submission.title, re.IGNORECASE):
            if not submission.title.startswith("Mod Applications") and submission.title != "Ask general questions about streams here.":
               lista_title.append(submission.title)
               lista_url.append(submission.url)


               comments = submission.comments
               for comment in comments[1:3]:  # first comment is a bot moderator
                   comment = comment.body # prints top comments starting from 2nd top comment
                   urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', comment)
                   for i in urls:
                       lista_streamlinks.append(i)
    return render_template('getlink.html', match_name=match_name, lista_title=lista_title, lista_url=lista_url, lista_streamlinks=lista_streamlinks)

if __name__ == '__main__':
    app.run()