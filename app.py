from flask import Flask, render_template, request
import sqlite3
import requests
from datetime import datetime
import pytz

app = Flask(__name__)

def get_news(query='news', everything=True):
    API_KEY = 'dc9f3b870377431690ceb87e6b3d2aff'
    if everything:
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}&pageSize=10"
    else:
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={API_KEY}&pageSize=10"
    response = requests.get(url)
    return response.json().get('articles', [])

@app.route('/', methods=['GET', 'POST'])
def home():
    # Newsletter form submission
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        conn = sqlite3.connect('news.db')
        conn.execute('INSERT INTO newsletter (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        conn.close()

    # Determine search & category
    search_query = request.args.get('q')
    category = request.args.get('category')
    view_more = request.args.get('view') == 'more'

    # Determine what to show
    if category:
        query = category
    elif search_query:
        query = search_query
    else:
        query = 'news'  # default homepage view

    # Fetch news data
    if category or search_query:
        # When searching or in category view, show relevant news
        top_news = get_news(query)
        trending_news = top_news[:3]
        latest_news = top_news[:5]
    else:
        # Homepage default layout
        latest_news = get_news('latest')
        trending_news = get_news('trending')
        top_news = get_news('top')

    # Show only 6 top news by default
    if not view_more:
        top_news = top_news[:6]

    # Current time
    india = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(india).strftime("%A, %b %d, %Y | %I:%M %p")

    return render_template('index.html',
                           current_time=current_time,
                           search_query=search_query or '',
                           category=category,
                           latest_news=latest_news,
                           trending_news=trending_news,
                           top_news=top_news)

if __name__ == '__main__':
    app.run(debug=True)
